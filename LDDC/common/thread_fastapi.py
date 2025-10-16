# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only
from collections.abc import Callable, Iterable
from functools import partial, wraps
from threading import Event, Lock, Thread
from typing import Any
import concurrent.futures
import threading

from .logger_fastapi import logger
from .models import P, T

exit_event = Event()


def is_exited() -> bool:
    return exit_event.is_set()


def set_exited() -> None:
    exit_event.set()


# 使用标准库的ThreadPoolExecutor替代QThreadPool
threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=8)


def in_main_thread(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    """在主线程中执行函数（FastAPI版本简化实现）"""
    return func(*args, **kwargs)


class SignalEmitter:
    """简化的信号发射器，不依赖Qt"""
    def __init__(self):
        self.success_callbacks = []
        self.error_callbacks = []
    
    def connect_success(self, callback: Callable):
        self.success_callbacks.append(callback)
    
    def connect_error(self, callback: Callable):
        self.error_callbacks.append(callback)
    
    def emit_success(self, result):
        for callback in self.success_callbacks:
            try:
                callback(result)
            except Exception as e:
                logger.error(f"Error in success callback: {e}")
    
    def emit_error(self, error):
        for callback in self.error_callbacks:
            try:
                callback(error)
            except Exception as e:
                logger.error(f"Error in error callback: {e}")


class TaskRunnable:
    def __init__(self, func: Callable[..., T], emitter: SignalEmitter) -> None:
        self.func = func
        self.emitter = emitter

    def run(self) -> None:
        try:
            result = self.func()
            self.emitter.emit_success(result)
        except Exception as e:
            logger.error(f"Task failed: {e}")
            self.emitter.emit_error(e)


def in_other_thread(
    func: Callable[..., T],  # 要执行的函数
    callback: Callable[[T], Any] | Iterable[Callable[[T], Any]] | None,  # 成功时的回调
    error_handling: Callable[[Exception], Any] | Iterable[Callable[[Exception], Any]] | None,  # 错误处理
    *args: Any,  # func 的位置参数
    **kwargs: Any,  # func 的关键字参数
) -> None:
    """在其他线程中执行函数"""
    emitter = SignalEmitter()
    
    # 连接回调函数
    if callback:
        if callable(callback):
            emitter.connect_success(callback)
        else:
            for cb in callback:
                emitter.connect_success(cb)
    
    if error_handling:
        if callable(error_handling):
            emitter.connect_error(error_handling)
        else:
            for eh in error_handling:
                emitter.connect_error(eh)
    
    # 创建任务
    task = TaskRunnable(partial(func, *args, **kwargs), emitter)
    
    # 提交到线程池
    threadpool.submit(task.run)


def cross_thread_func(func: Callable[P, T]) -> Callable[P, None | T]:
    """跨线程函数装饰器（简化版本）"""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None | T:
        if threading.current_thread() is threading.main_thread():
            return func(*args, **kwargs)
        else:
            # 在非主线程中，直接执行
            return func(*args, **kwargs)
    return wrapper