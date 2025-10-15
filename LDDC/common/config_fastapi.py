# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only

"""数据管理模块

这个模块提供了:
- 配置文件管理（FastAPI版本，不依赖PySide6）
"""

import json
from threading import Lock
from typing import Any, Callable

from LDDC.common.paths import config_dir, default_save_lyrics_dir


class ConfigSignal:
    """简化的信号类，不依赖Qt"""
    
    def __init__(self):
        self.callbacks = []
    
    def connect(self, callback: Callable):
        """连接回调函数"""
        self.callbacks.append(callback)
    
    def emit(self, *args):
        """发射信号"""
        for callback in self.callbacks:
            try:
                callback(*args)
            except Exception as e:
                print(f"Error in signal callback: {e}")


class Config(dict):
    """LDDC的配置管理类（FastAPI版本）

    1. 使用Lock保证线程安全
    2. 使用方法类似字典
    3. 使用json格式存储配置文件
    注意: 用于Lock导致这个类并不高效,不应该在需要高性能的地方使用
    """

    def __init__(self) -> None:
        self.lock = None
        self.config_path = config_dir / "config.json"
        self.lyrics_changed = ConfigSignal()  # 在歌词相关配置改变时发出信号
        self.desktop_lyrics_changed = ConfigSignal()  # 在桌面歌词相关配置改变时发出信号

        self.default_cfg = {
            "lyrics_file_name_fmt": "%<artist> - %<title> (%<id>)",
            "default_save_path": str(default_save_lyrics_dir),
            "ID3_version": "v2.3",

            "multi_search_sources": ["QM", "KG", "NE"],

            "langs_order": ["roma", "orig", "ts"],
            "skip_inst_lyrics": True,
            "auto_select": True,
            "add_end_timestamp_line": False,

            "save_mode": 0,
            "lyrics_format": 1,
            "lrc_ms": False,
            "lrc_offset": 0,

            "language": "auto",

            "desktop_lyrics_enabled": False,
            "desktop_lyrics_font_family": "Microsoft YaHei",
            "desktop_lyrics_font_size": 48,
            "desktop_lyrics_font_color": "#FFFFFF",
            "desktop_lyrics_font_stroke_color": "#000000",
            "desktop_lyrics_font_stroke_width": 2,
            "desktop_lyrics_background_color": "#80000000",
            "desktop_lyrics_background_radius": 10,
            "desktop_lyrics_background_margin": 10,
            "desktop_lyrics_position_x": 100,
            "desktop_lyrics_position_y": 100,
            "desktop_lyrics_width": 800,
            "desktop_lyrics_height": 100,
            "desktop_lyrics_always_on_top": True,
            "desktop_lyrics_click_through": False,
            "desktop_lyrics_auto_hide": True,
            "desktop_lyrics_hide_timeout": 3000,

            "translate_source": "BING",
            "translate_target_language": "SIMPLIFIED_CHINESE",
            "translate_api_key": "",
            "translate_api_base": "",

            "log_level": "INFO",
            "check_update": True,
            "auto_update": False,
        }

        super().__init__(self.default_cfg)
        self.lock = Lock()
        self.load()

    def load(self) -> None:
        """加载配置文件"""
        with self.lock:
            if self.config_path.exists():
                try:
                    with open(self.config_path, encoding="utf-8") as f:
                        data = json.load(f)
                    self.update(data)
                except (json.JSONDecodeError, OSError) as e:
                    print(f"Failed to load config: {e}")

    def save(self) -> None:
        """保存配置文件"""
        with self.lock:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                with open(self.config_path, "w", encoding="utf-8") as f:
                    json.dump(dict(self), f, ensure_ascii=False, indent=2)
            except OSError as e:
                print(f"Failed to save config: {e}")

    def __setitem__(self, key: str, value: Any) -> None:
        with self.lock:
            super().__setitem__(key, value)
            self.save()
            
            # 发射相应的信号
            lyrics_related_keys = [
                "lyrics_file_name_fmt", "default_save_path", "ID3_version",
                "multi_search_sources", "langs_order", "skip_inst_lyrics",
                "auto_select", "add_end_timestamp_line", "save_mode",
                "lyrics_format", "lrc_ms", "lrc_offset"
            ]
            
            desktop_lyrics_related_keys = [
                "desktop_lyrics_enabled", "desktop_lyrics_font_family",
                "desktop_lyrics_font_size", "desktop_lyrics_font_color",
                "desktop_lyrics_font_stroke_color", "desktop_lyrics_font_stroke_width",
                "desktop_lyrics_background_color", "desktop_lyrics_background_radius",
                "desktop_lyrics_background_margin", "desktop_lyrics_position_x",
                "desktop_lyrics_position_y", "desktop_lyrics_width",
                "desktop_lyrics_height", "desktop_lyrics_always_on_top",
                "desktop_lyrics_click_through", "desktop_lyrics_auto_hide",
                "desktop_lyrics_hide_timeout"
            ]
            
            if key in lyrics_related_keys:
                self.lyrics_changed.emit((key, value))
            
            if key in desktop_lyrics_related_keys:
                self.desktop_lyrics_changed.emit((key, value))

    def get(self, key: str, default: Any = None) -> Any:
        with self.lock:
            return super().get(key, default)

    def __getitem__(self, key: str) -> Any:
        with self.lock:
            return super().__getitem__(key)

    def __contains__(self, key: str) -> bool:
        with self.lock:
            return super().__contains__(key)

    def keys(self):
        with self.lock:
            return super().keys()

    def values(self):
        with self.lock:
            return super().values()

    def items(self):
        with self.lock:
            return super().items()


cfg = Config()