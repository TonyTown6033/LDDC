# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only

"""日志记录器（FastAPI版本，不依赖PySide6）"""

import io
import logging
import os
import sys
import time
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING, Filter, LogRecord

from .args import args
from .config_fastapi import cfg
from .paths import log_dir

log_file = log_dir / f'{time.strftime("%Y.%m.%d", time.localtime())}.log'
log_file.parent.mkdir(parents=True, exist_ok=True)


def str2log_level(level: str) -> int:
    match level:
        case "NOTSET":
            return NOTSET
        case "DEBUG":
            return DEBUG
        case "INFO":
            return INFO
        case "WARNING":
            return WARNING
        case "ERROR":
            return ERROR
        case "CRITICAL":
            return CRITICAL
        case _:
            msg = f"Invalid log level: {level}"
            raise ValueError(msg)


class Logger:
    def __init__(self) -> None:
        self.logger = logging.getLogger("LDDC")
        self.logger.setLevel(DEBUG)
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(DEBUG)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(INFO)
        
        # 创建格式器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # 设置初始日志级别
        self.set_level(cfg.get("log_level", "INFO"))

    def set_level(self, level: int | str) -> None:
        if isinstance(level, str):
            level = str2log_level(level)
        
        self.logger.setLevel(level)
        
        # 更新所有处理器的级别
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                handler.setLevel(max(level, INFO))  # 控制台至少显示INFO级别
            else:
                handler.setLevel(level)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)

    def critical(self, msg: str) -> None:
        self.logger.critical(msg)

    def exception(self, msg: str) -> None:
        self.logger.exception(msg)


logger = Logger()


def get_logger() -> Logger:
    """获取日志记录器实例"""
    return logger