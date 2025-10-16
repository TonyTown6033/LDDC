# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only
import contextlib
from abc import abstractmethod
from collections.abc import Callable, Iterable
from functools import partial, reduce
from threading import Lock, RLock
from typing import Any, Generic, final
from weakref import WeakKeyDictionary

from .logger_fastapi import logger
from .models import P, T
from .thread_fastapi import in_other_thread, is_exited, threadpool


class TaskManager:
    def __init__(self, parent_childs: dict[str, list[str]], task_callback: dict[str, Callable[[], None]] | None = None) -> None:
        """任务管理器,用于管理任务.

        Args:
            parent_childs (dict[str, list[str]]): 任务类型和子任务类型的映射.
            task_callback (dict[str, Callable[[str, int], None]]): 任务完成时的回调函数.

        """
        for childs in parent_childs.values():
            for child in childs:
                if child not in parent_childs:
                    msg = f"{child} is not in parent_map"
                    raise ValueError(msg)

        self.tasks: dict[str, set[int]] = {task_type: set() for task_type in parent_childs}
        self.parent_childs: dict[str, list[str]] = parent_childs
        self.task_callback: dict[str, Callable[[], None]] = task_callback if task_callback is not None else {}

        self.main_id: int = 0  # 用来保证任务id唯一
        self.lock = RLock()

    def set_callback(self, task_type: str, callback: Callable[[], None]) -> None:
        """设置任务完成时的回调函数."""
        with self.lock:
            self.task_callback[task_type] = callback

    def set_task(self, task_type: str, childs: Iterable[str] = ()) -> None:
        """设置任务."""
        with self.lock:
            self.tasks[task_type] = set()
            self.parent_childs[task_type] = list(childs)

    def add_task(self, task_type: str) -> int:
        """添加任务."""
        with self.lock:
            self.main_id += 1
            self.tasks[task_type].add(self.main_id)
            return self.main_id

    def remove_task(self, task_type: str, task_id: int) -> None:
        """移除任务."""
        with self.lock:
            self.tasks[task_type].discard(task_id)
            self._check_task_complete(task_type)

    def _check_task_complete(self, task_type: str) -> None:
        """检查任务是否完成."""
        if not self.tasks[task_type]:
            # 检查子任务是否完成
            for child in self.parent_childs[task_type]:
                if self.tasks[child]:
                    return
            # 任务完成，调用回调函数
            if task_type in self.task_callback:
                self.task_callback[task_type]()

    def is_task_running(self, task_type: str) -> bool:
        """检查任务是否正在运行."""
        with self.lock:
            if self.tasks[task_type]:
                return True
            for child in self.parent_childs[task_type]:
                if self.tasks[child]:
                    return True
            return False

    def get_task_count(self, task_type: str) -> int:
        """获取任务数量."""
        with self.lock:
            count = len(self.tasks[task_type])
            for child in self.parent_childs[task_type]:
                count += len(self.tasks[child])
            return count


class BaseTask(Generic[P, T]):
    """基础任务类"""
    
    def __init__(self, task_manager: TaskManager, task_type: str) -> None:
        self.task_manager = task_manager
        self.task_type = task_type
        self.task_id = task_manager.add_task(task_type)

    @abstractmethod
    def run(self, *args: P.args, **kwargs: P.kwargs) -> T:
        """执行任务"""
        pass

    def finish(self) -> None:
        """完成任务"""
        self.task_manager.remove_task(self.task_type, self.task_id)

    @final
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        try:
            result = self.run(*args, **kwargs)
            return result
        finally:
            self.finish()


class AsyncTask(BaseTask[P, T]):
    """异步任务类"""
    
    def __init__(
        self,
        task_manager: TaskManager,
        task_type: str,
        func: Callable[P, T],
        callback: Callable[[T], Any] | None = None,
        error_callback: Callable[[Exception], Any] | None = None,
    ) -> None:
        super().__init__(task_manager, task_type)
        self.func = func
        self.callback = callback
        self.error_callback = error_callback

    def run(self, *args: P.args, **kwargs: P.kwargs) -> T:
        """执行任务"""
        return self.func(*args, **kwargs)

    def start(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """启动异步任务"""
        def success_callback(result: T) -> None:
            if self.callback:
                self.callback(result)
            self.finish()

        def error_callback(error: Exception) -> None:
            if self.error_callback:
                self.error_callback(error)
            self.finish()

        in_other_thread(
            self.func,
            success_callback,
            error_callback,
            *args,
            **kwargs
        )


# 全局任务管理器实例
default_task_manager = TaskManager({})