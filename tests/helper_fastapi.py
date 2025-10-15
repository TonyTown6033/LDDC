# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only
import json
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class Point:
    """简单的点类（替代QPoint）"""
    
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False


class MockFileDialog:
    """模拟文件对话框"""
    
    @staticmethod
    def get_open_file_name(
        parent=None,
        caption: str = "",
        directory: str = "",
        filter_str: str = "",
    ) -> tuple[str, str]:
        """模拟获取打开文件名"""
        # 在测试环境中返回预设的文件路径
        return "/tmp/test_file.txt", "Text Files (*.txt)"
    
    @staticmethod
    def get_save_file_name(
        parent=None,
        caption: str = "",
        directory: str = "",
        filter_str: str = "",
    ) -> tuple[str, str]:
        """模拟获取保存文件名"""
        # 在测试环境中返回预设的文件路径
        return "/tmp/save_file.txt", "Text Files (*.txt)"
    
    @staticmethod
    def get_existing_directory(
        parent=None,
        caption: str = "",
        directory: str = "",
    ) -> str:
        """模拟获取现有目录"""
        # 在测试环境中返回临时目录
        return tempfile.gettempdir()


class MockMessageBox:
    """模拟消息框"""
    
    # 消息框按钮常量
    OK = "OK"
    CANCEL = "Cancel"
    YES = "Yes"
    NO = "No"
    APPLY = "Apply"
    CLOSE = "Close"
    
    # 消息框图标常量
    INFORMATION = "Information"
    WARNING = "Warning"
    CRITICAL = "Critical"
    QUESTION = "Question"
    
    @staticmethod
    def information(
        parent=None,
        title: str = "",
        text: str = "",
        buttons=None,
        default_button=None,
    ) -> str:
        """显示信息消息框"""
        print(f"INFO: {title} - {text}")
        return MockMessageBox.OK
    
    @staticmethod
    def warning(
        parent=None,
        title: str = "",
        text: str = "",
        buttons=None,
        default_button=None,
    ) -> str:
        """显示警告消息框"""
        print(f"WARNING: {title} - {text}")
        return MockMessageBox.OK
    
    @staticmethod
    def critical(
        parent=None,
        title: str = "",
        text: str = "",
        buttons=None,
        default_button=None,
    ) -> str:
        """显示错误消息框"""
        print(f"ERROR: {title} - {text}")
        return MockMessageBox.OK
    
    @staticmethod
    def question(
        parent=None,
        title: str = "",
        text: str = "",
        buttons=None,
        default_button=None,
    ) -> str:
        """显示问题消息框"""
        print(f"QUESTION: {title} - {text}")
        return MockMessageBox.YES


class MockWidget:
    """模拟窗口部件"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.visible = False
        self.enabled = True
        self.geometry_rect = (0, 0, 100, 100)  # x, y, width, height
    
    def show(self):
        """显示窗口部件"""
        self.visible = True
    
    def hide(self):
        """隐藏窗口部件"""
        self.visible = False
    
    def is_visible(self) -> bool:
        """检查是否可见"""
        return self.visible
    
    def set_enabled(self, enabled: bool):
        """设置是否启用"""
        self.enabled = enabled
    
    def is_enabled(self) -> bool:
        """检查是否启用"""
        return self.enabled
    
    def set_geometry(self, x: int, y: int, width: int, height: int):
        """设置几何形状"""
        self.geometry_rect = (x, y, width, height)
    
    def geometry(self) -> tuple[int, int, int, int]:
        """获取几何形状"""
        return self.geometry_rect


class MockApplication:
    """模拟应用程序"""
    
    def __init__(self):
        self.widgets = []
        self.running = False
    
    def exec(self) -> int:
        """执行应用程序"""
        self.running = True
        return 0
    
    def quit(self):
        """退出应用程序"""
        self.running = False
    
    def add_widget(self, widget: MockWidget):
        """添加窗口部件"""
        self.widgets.append(widget)
    
    def remove_widget(self, widget: MockWidget):
        """移除窗口部件"""
        if widget in self.widgets:
            self.widgets.remove(widget)


def create_temp_directory() -> Path:
    """创建临时目录"""
    temp_dir = Path(tempfile.mkdtemp())
    return temp_dir


def create_temp_file(
    content: str = "",
    suffix: str = ".txt",
    directory: Optional[Path] = None,
) -> Path:
    """创建临时文件"""
    if directory is None:
        directory = create_temp_directory()
    
    temp_file = directory / f"temp{suffix}"
    temp_file.write_text(content, encoding="utf-8")
    return temp_file


def create_test_audio_file(file_path: Path) -> Path:
    """创建测试音频文件"""
    # 创建一个简单的MP3文件头
    with open(file_path, "wb") as f:
        # ID3v2 header
        f.write(b"ID3\x03\x00\x00\x00\x00\x00\x00")
        # 简单的音频数据
        f.write(b"\xff\xfb\x90\x00" * 100)
    return file_path


def create_test_lyrics_file(file_path: Path, lyrics_content: str = None) -> Path:
    """创建测试歌词文件"""
    if lyrics_content is None:
        lyrics_content = """[00:00.00]测试歌词
[00:05.00]这是第一行
[00:10.00]这是第二行
[00:15.00]测试结束
"""
    file_path.write_text(lyrics_content, encoding="utf-8")
    return file_path


def create_test_config_file(file_path: Path, config_data: Dict[str, Any] = None) -> Path:
    """创建测试配置文件"""
    if config_data is None:
        config_data = {
            "language": "zh_CN",
            "theme": "light",
            "auto_save": True,
            "sources": ["netease", "qq", "kugou"],
        }
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)
    
    return file_path


def simulate_user_input(input_text: str) -> str:
    """模拟用户输入"""
    print(f"Simulated user input: {input_text}")
    return input_text


def simulate_file_drop(file_paths: List[Union[str, Path]]) -> List[Path]:
    """模拟文件拖拽"""
    paths = [Path(p) for p in file_paths]
    print(f"Simulated file drop: {[str(p) for p in paths]}")
    return paths


def wait_for_condition(
    condition_func,
    timeout: float = 5.0,
    interval: float = 0.1,
) -> bool:
    """等待条件满足"""
    import time
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(interval)
    return False


class TestDataManager:
    """测试数据管理器"""
    
    def __init__(self, temp_dir: Path):
        self.temp_dir = temp_dir
        self.created_files = []
        self.created_dirs = []
    
    def create_file(self, relative_path: str, content: str = "") -> Path:
        """创建文件"""
        file_path = self.temp_dir / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        self.created_files.append(file_path)
        return file_path
    
    def create_directory(self, relative_path: str) -> Path:
        """创建目录"""
        dir_path = self.temp_dir / relative_path
        dir_path.mkdir(parents=True, exist_ok=True)
        self.created_dirs.append(dir_path)
        return dir_path
    
    def cleanup(self):
        """清理创建的文件和目录"""
        for file_path in self.created_files:
            if file_path.exists():
                file_path.unlink()
        
        for dir_path in reversed(self.created_dirs):
            if dir_path.exists() and not any(dir_path.iterdir()):
                dir_path.rmdir()
        
        self.created_files.clear()
        self.created_dirs.clear()


def assert_file_exists(file_path: Union[str, Path], message: str = ""):
    """断言文件存在"""
    path = Path(file_path)
    assert path.exists(), f"File does not exist: {path}. {message}"


def assert_file_not_exists(file_path: Union[str, Path], message: str = ""):
    """断言文件不存在"""
    path = Path(file_path)
    assert not path.exists(), f"File should not exist: {path}. {message}"


def assert_directory_exists(dir_path: Union[str, Path], message: str = ""):
    """断言目录存在"""
    path = Path(dir_path)
    assert path.exists() and path.is_dir(), f"Directory does not exist: {path}. {message}"


def assert_file_content_equals(
    file_path: Union[str, Path],
    expected_content: str,
    message: str = "",
):
    """断言文件内容相等"""
    path = Path(file_path)
    assert_file_exists(path)
    actual_content = path.read_text(encoding="utf-8")
    assert actual_content == expected_content, f"File content mismatch: {path}. {message}"


def assert_json_file_equals(
    file_path: Union[str, Path],
    expected_data: Dict[str, Any],
    message: str = "",
):
    """断言JSON文件内容相等"""
    path = Path(file_path)
    assert_file_exists(path)
    with open(path, "r", encoding="utf-8") as f:
        actual_data = json.load(f)
    assert actual_data == expected_data, f"JSON file content mismatch: {path}. {message}"