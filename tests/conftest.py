# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only
import os
import sys
import tempfile
from pathlib import Path
from typing import Generator

import pytest

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from LDDC.common.config_fastapi import Config, cfg
from LDDC.common.logger_fastapi import get_logger
from LDDC.common.translator_fastapi import Translator


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment() -> Generator[None, None, None]:
    """设置测试环境"""
    # 创建临时目录用于测试
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # 设置环境变量
        os.environ["LDDC_TEST_MODE"] = "1"
        os.environ["LDDC_CONFIG_DIR"] = str(temp_path / "config")
        os.environ["LDDC_CACHE_DIR"] = str(temp_path / "cache")
        os.environ["LDDC_LOG_DIR"] = str(temp_path / "logs")
        
        # 创建必要的目录
        (temp_path / "config").mkdir(exist_ok=True)
        (temp_path / "cache").mkdir(exist_ok=True)
        (temp_path / "logs").mkdir(exist_ok=True)
        
        yield
        
        # 清理环境变量
        for key in ["LDDC_TEST_MODE", "LDDC_CONFIG_DIR", "LDDC_CACHE_DIR", "LDDC_LOG_DIR"]:
            os.environ.pop(key, None)


@pytest.fixture
def config() -> Config:
    """获取测试配置"""
    return cfg


@pytest.fixture
def logger():
    """获取测试日志器"""
    return get_logger("test")


@pytest.fixture
def translator() -> Translator:
    """获取测试翻译器"""
    return Translator()


@pytest.fixture
def temp_audio_file(tmp_path: Path) -> Path:
    """创建临时音频文件用于测试"""
    audio_file = tmp_path / "test.mp3"
    # 创建一个简单的MP3文件头（用于测试）
    with open(audio_file, "wb") as f:
        # 写入简单的MP3文件头
        f.write(b"ID3\x03\x00\x00\x00\x00\x00\x00")
    return audio_file


@pytest.fixture
def temp_lyrics_file(tmp_path: Path) -> Path:
    """创建临时歌词文件用于测试"""
    lyrics_file = tmp_path / "test.lrc"
    lyrics_content = """[00:00.00]测试歌词
[00:05.00]这是第一行
[00:10.00]这是第二行
[00:15.00]测试结束
"""
    lyrics_file.write_text(lyrics_content, encoding="utf-8")
    return lyrics_file


@pytest.fixture
def sample_song_info():
    """创建示例歌曲信息"""
    from LDDC.common.models import Artist, SongInfo
    
    return SongInfo(
        title="测试歌曲",
        artist=Artist("测试艺术家"),
        album="测试专辑",
        duration=180000,  # 3分钟
    )


@pytest.fixture
def sample_lyrics():
    """创建示例歌词"""
    from LDDC.common.models import Lyrics, LyricsLine
    
    lines = [
        LyricsLine(start_time=0, text="测试歌词"),
        LyricsLine(start_time=5000, text="这是第一行"),
        LyricsLine(start_time=10000, text="这是第二行"),
        LyricsLine(start_time=15000, text="测试结束"),
    ]
    
    return Lyrics(lines=lines)


class MockTaskManager:
    """模拟任务管理器"""
    
    def __init__(self):
        self.tasks = []
    
    def add_task(self, task, callback=None):
        """添加任务"""
        self.tasks.append((task, callback))
        # 立即执行任务（用于测试）
        try:
            result = task()
            if callback:
                callback(result)
        except Exception as e:
            if callback:
                callback(None, e)
    
    def clear_tasks(self):
        """清空任务"""
        self.tasks.clear()


@pytest.fixture
def mock_task_manager():
    """获取模拟任务管理器"""
    return MockTaskManager()


class MockSignalEmitter:
    """模拟信号发射器"""
    
    def __init__(self):
        self.callbacks = {}
    
    def connect(self, signal_name: str, callback):
        """连接信号"""
        if signal_name not in self.callbacks:
            self.callbacks[signal_name] = []
        self.callbacks[signal_name].append(callback)
    
    def emit(self, signal_name: str, *args, **kwargs):
        """发射信号"""
        if signal_name in self.callbacks:
            for callback in self.callbacks[signal_name]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    print(f"Signal callback error: {e}")
    
    def disconnect(self, signal_name: str, callback=None):
        """断开信号"""
        if signal_name in self.callbacks:
            if callback:
                try:
                    self.callbacks[signal_name].remove(callback)
                except ValueError:
                    pass
            else:
                self.callbacks[signal_name].clear()


@pytest.fixture
def mock_signal_emitter():
    """获取模拟信号发射器"""
    return MockSignalEmitter()


# 测试标记
pytest_plugins = []

# 慢速测试标记
def pytest_configure(config):
    """配置pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """修改测试项目"""
    # 为没有标记的测试添加unit标记
    for item in items:
        if not any(mark.name in ["slow", "integration", "unit"] for mark in item.iter_markers()):
            item.add_marker(pytest.mark.unit)