# LDDC PySide6 到 FastAPI 迁移指南

本指南将帮助您从基于PySide6的桌面应用版本迁移到基于FastAPI的Web服务版本。

## 概述

LDDC现在提供两种运行模式：

1. **传统桌面应用模式**：基于PySide6的GUI应用程序
2. **FastAPI Web服务模式**：基于FastAPI的RESTful API服务

## 主要变化

### 架构变化

| 组件 | PySide6版本 | FastAPI版本 | 说明 |
|------|-------------|-------------|------|
| 信号系统 | `QObject.Signal` | `threading.Event` + 回调 | 使用标准库线程事件和回调函数 |
| 线程管理 | `QThread`, `QRunnable` | `asyncio`, `ThreadPoolExecutor` | 异步处理和线程池 |
| 事件循环 | `QEventLoop` | `asyncio.EventLoop` | 异步事件循环 |
| 配置管理 | `QObject` + `Signal` | 标准类 + 回调 | 简化的配置管理 |
| 日志系统 | `QLoggingCategory` | `logging` | 标准Python日志 |
| 翻译系统 | `QTranslator` | 自定义翻译类 | 简化的翻译实现 |

### 文件结构

```
LDDC/
├── common/
│   ├── config.py              # PySide6版本
│   ├── config_fastapi.py      # FastAPI版本
│   ├── logger.py              # PySide6版本
│   ├── logger_fastapi.py      # FastAPI版本
│   ├── task_manager.py        # PySide6版本
│   ├── task_manager_fastapi.py # FastAPI版本
│   └── ...
├── core/
│   ├── auto_fetch.py          # PySide6版本
│   ├── auto_fetch_fastapi.py  # FastAPI版本
│   ├── song_info.py           # PySide6版本
│   ├── song_info_fastapi.py   # FastAPI版本
│   └── ...
├── __main__.py                # 桌面应用入口
└── __main___fastapi.py        # Web服务入口
```

## 代码迁移示例

### 1. 信号和槽机制

**PySide6版本：**
```python
from PySide6.QtCore import QObject, Signal

class MyClass(QObject):
    data_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.data_changed.connect(self.on_data_changed)
    
    def on_data_changed(self, data):
        print(f"Data changed: {data}")
    
    def update_data(self, new_data):
        self.data_changed.emit(new_data)
```

**FastAPI版本：**
```python
import threading
from typing import Callable, List

class MyClass:
    def __init__(self):
        self.data_changed_callbacks: List[Callable[[str], None]] = []
        self._lock = threading.Lock()
    
    def connect_data_changed(self, callback: Callable[[str], None]):
        with self._lock:
            self.data_changed_callbacks.append(callback)
    
    def emit_data_changed(self, data: str):
        with self._lock:
            for callback in self.data_changed_callbacks:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Callback error: {e}")
    
    def update_data(self, new_data: str):
        self.emit_data_changed(new_data)

# 使用示例
my_obj = MyClass()
my_obj.connect_data_changed(lambda data: print(f"Data changed: {data}"))
```

### 2. 线程管理

**PySide6版本：**
```python
from PySide6.QtCore import QRunnable, QThreadPool

class WorkerTask(QRunnable):
    def run(self):
        # 执行任务
        result = self.do_work()
        # 发射信号通知完成
        self.finished.emit(result)

# 使用
task = WorkerTask()
QThreadPool.globalInstance().start(task)
```

**FastAPI版本：**
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Any

class TaskManager:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def run_task(self, task_func: Callable, callback: Callable[[Any], None] = None):
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(self.executor, task_func)
            if callback:
                callback(result)
            return result
        except Exception as e:
            if callback:
                callback(None, e)
            raise

# 使用示例
async def main():
    task_manager = TaskManager()
    
    def my_task():
        # 执行任务
        return "task result"
    
    def on_complete(result, error=None):
        if error:
            print(f"Task failed: {error}")
        else:
            print(f"Task completed: {result}")
    
    await task_manager.run_task(my_task, on_complete)
```

### 3. 事件循环

**PySide6版本：**
```python
from PySide6.QtCore import QEventLoop, QTimer

def wait_for_result():
    loop = QEventLoop()
    timer = QTimer()
    timer.timeout.connect(loop.quit)
    timer.start(5000)  # 5秒超时
    
    # 等待结果或超时
    loop.exec()
```

**FastAPI版本：**
```python
import asyncio

async def wait_for_result():
    try:
        # 等待结果，5秒超时
        result = await asyncio.wait_for(get_result(), timeout=5.0)
        return result
    except asyncio.TimeoutError:
        print("Operation timed out")
        return None

async def get_result():
    # 模拟异步操作
    await asyncio.sleep(2)
    return "result"
```

### 4. 配置管理

**PySide6版本：**
```python
from PySide6.QtCore import QObject, Signal

class Config(QObject):
    config_changed = Signal(str, object)
    
    def __init__(self):
        super().__init__()
        self.data = {}
    
    def set_value(self, key: str, value):
        self.data[key] = value
        self.config_changed.emit(key, value)
```

**FastAPI版本：**
```python
import threading
from typing import Any, Callable, Dict, List

class Config:
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.change_callbacks: List[Callable[[str, Any], None]] = []
        self._lock = threading.Lock()
    
    def connect_changed(self, callback: Callable[[str, Any], None]):
        with self._lock:
            self.change_callbacks.append(callback)
    
    def set_value(self, key: str, value: Any):
        with self._lock:
            self.data[key] = value
            for callback in self.change_callbacks:
                try:
                    callback(key, value)
                except Exception as e:
                    print(f"Config callback error: {e}")
```

## API接口设计

### RESTful API端点

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class SearchRequest(BaseModel):
    title: str
    artist: str = ""
    album: str = ""
    sources: List[str] = ["netease", "qq", "kugou"]

class SearchResponse(BaseModel):
    results: List[dict]
    total: int

@app.post("/api/search", response_model=SearchResponse)
async def search_lyrics(request: SearchRequest):
    # 使用FastAPI版本的搜索功能
    from LDDC.core.auto_fetch_fastapi import search_lyrics
    
    results = await search_lyrics(
        title=request.title,
        artist=request.artist,
        album=request.album,
        sources=request.sources
    )
    
    return SearchResponse(results=results, total=len(results))
```

### WebSocket支持

```python
from fastapi import WebSocket
import json

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "search":
                # 处理搜索请求
                results = await handle_search(message["data"])
                await websocket.send_text(json.dumps({
                    "type": "search_result",
                    "data": results
                }))
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
```

## 部署指南

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python -m LDDC.__main___fastapi

# 或使用uvicorn
uvicorn LDDC.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker部署

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "LDDC.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生产环境

```bash
# 使用gunicorn + uvicorn workers
gunicorn LDDC.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 测试迁移

### 单元测试

```python
import pytest
from LDDC.common.config_fastapi import Config

def test_config():
    config = Config()
    
    # 测试回调
    called = []
    def on_change(key, value):
        called.append((key, value))
    
    config.connect_changed(on_change)
    config.set_value("test_key", "test_value")
    
    assert called == [("test_key", "test_value")]
```

### API测试

```python
from fastapi.testclient import TestClient
from LDDC.api.main import app

client = TestClient(app)

def test_search_api():
    response = client.post("/api/search", json={
        "title": "测试歌曲",
        "artist": "测试艺术家"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total" in data
```

## 性能优化

### 异步处理

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncLyricsProcessor:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=8)
    
    async def process_multiple_songs(self, songs):
        tasks = []
        for song in songs:
            task = asyncio.create_task(self.process_song(song))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    async def process_song(self, song):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor, 
            self._sync_process_song, 
            song
        )
```

### 缓存策略

```python
from functools import lru_cache
import diskcache

# 内存缓存
@lru_cache(maxsize=1000)
def get_cached_lyrics(song_id: str):
    return fetch_lyrics_from_api(song_id)

# 磁盘缓存
cache = diskcache.Cache('/tmp/lddc_cache')

def get_lyrics_with_disk_cache(song_id: str):
    if song_id in cache:
        return cache[song_id]
    
    lyrics = fetch_lyrics_from_api(song_id)
    cache[song_id] = lyrics
    return lyrics
```

## 故障排除

### 常见问题

1. **导入错误**：确保使用`*_fastapi.py`版本的模块
2. **异步问题**：在异步函数中使用`await`关键字
3. **线程安全**：使用`threading.Lock`保护共享资源
4. **性能问题**：合理使用线程池和异步处理

### 调试技巧

```python
import logging

# 启用详细日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 在关键位置添加日志
logger.debug(f"Processing song: {song.title}")
logger.info(f"Search completed: {len(results)} results")
logger.error(f"Failed to fetch lyrics: {error}")
```

## 总结

FastAPI版本提供了以下优势：

1. **更好的性能**：异步处理和并发支持
2. **标准化API**：RESTful接口和OpenAPI文档
3. **容器化友好**：易于Docker部署
4. **更少依赖**：移除了重量级的Qt依赖
5. **更好的测试**：标准的Python测试工具

通过本指南，您应该能够成功地将代码从PySide6版本迁移到FastAPI版本。如有问题，请参考具体的`*_fastapi.py`文件实现。