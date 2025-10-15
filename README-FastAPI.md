# LDDC FastAPI 精简版

基于 LDDC 核心功能的 FastAPI Web API 服务，提供歌词搜索和下载功能。

## 功能特性

- 🔍 **歌词搜索**: 支持多个音乐平台搜索歌曲
- 📥 **歌词下载**: 获取并转换歌词为 LRC 格式
- 🌐 **RESTful API**: 标准的 HTTP API 接口
- 📖 **自动文档**: 内置 Swagger UI 文档

## 支持的音乐平台

- **QM**: QQ音乐
- **KG**: 酷狗音乐  
- **NE**: 网易云音乐
- **LRCLIB**: LrcLib

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements-fastapi.txt
```

### 2. 启动服务

```bash
python fastapi_app.py
```

服务将在 `http://localhost:8000` 启动。

### 3. 访问文档

打开浏览器访问 `http://localhost:8000/docs` 查看 API 文档。

## API 接口

### 搜索歌曲

**POST** `/search`

```json
{
  "keyword": "周杰伦 晴天",
  "source": "QM",
  "search_type": "SONG",
  "page": 1
}
```

**GET** `/search_simple?keyword=周杰伦 晴天&source=QM`

### 下载歌词

**POST** `/lyrics`

```json
{
  "song_id": "001JZ1GY0Ja18Y",
  "title": "晴天",
  "artist": "周杰伦",
  "album": "叶惠美",
  "duration": 269,
  "source": "QM"
}
```

**GET** `/lyrics_simple?song_id=001JZ1GY0Ja18Y&title=晴天&artist=周杰伦&source=QM`

## 使用示例

### Python 客户端

```python
import requests

# 搜索歌曲
response = requests.post("http://localhost:8000/search", json={
    "keyword": "周杰伦 晴天",
    "source": "QM"
})
results = response.json()

# 下载歌词
if results["results"]:
    song = results["results"][0]
    lyrics_response = requests.post("http://localhost:8000/lyrics", json=song)
    lrc_content = lyrics_response.text
    print(lrc_content)
```

### curl 命令

```bash
# 搜索
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "周杰伦 晴天", "source": "QM"}'

# 下载歌词
curl "http://localhost:8000/lyrics_simple?song_id=001JZ1GY0Ja18Y&title=晴天&artist=周杰伦&source=QM"
```

## 部署

### Docker 部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements-fastapi.txt .
RUN pip install -r requirements-fastapi.txt

COPY . .
EXPOSE 8000

CMD ["python", "fastapi_app.py"]
```

### 生产环境

```bash
# 使用 gunicorn
pip install gunicorn
gunicorn fastapi_app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 注意事项

- 本项目基于 LDDC 核心功能，需要完整的 LDDC 项目环境
- 请遵守各音乐平台的使用条款
- 仅供个人学习和研究使用

## 许可证

本项目遵循 GPL-3.0 许可证。