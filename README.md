# LDDC

中文 | [English](./README_en.md) | [日本語](./README_ja.md)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/015f636391584ffc82790ff7038da5ca)](https://app.codacy.com/gh/chenmozhijin/LDDC/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/chenmozhijin/LDDC/total)](https://github.com/chenmozhijin/LDDC/releases/latest)
[![Static Badge](https://img.shields.io/badge/Python-3.10%2B-brightgreen)](https://www.python.org/downloads/)
[![Static Badge](https://img.shields.io/badge/License-GPLv3-blue)](https://github.com/chenmozhijin/LDDC/blob/main/LICENSE)
[![release](https://img.shields.io/github/v/release/chenmozhijin/LDDC?color=blue)](https://github.com/chenmozhijin/LDDC/releases/latest)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

LDDC是一个简单易用的精准歌词(逐字歌词)下载匹配工具。现已支持**FastAPI Web服务**运行模式，并提供容器化部署方案。

## 🚀 新特性：FastAPI Web服务

LDDC现在支持作为FastAPI Web服务运行，提供RESTful API接口：

- 🌐 **Web API接口**：通过HTTP API调用所有歌词搜索和匹配功能
- 🔄 **异步处理**：基于asyncio的高性能异步处理
- 📊 **实时状态**：WebSocket支持实时状态更新和进度反馈
- 🐳 **容器化部署**：支持Docker容器化部署
- 🔧 **灵活集成**：可轻松集成到其他应用和服务中

## 主要特性（Web）

- 🌐 Web API：通过 HTTP API 提供歌词搜索、下载、格式转换能力
- 🐳 容器化部署：提供 Dockerfile，支持一键构建与运行
- 🔎 多平台搜索：QQ音乐、酷狗音乐、网易云，支持 Lrclib
- 📝 多格式输出：逐字LRC、逐行LRC、增强LRC、SRT、ASS
- 🔁 翻译支持：Bing/Google/OpenAI兼容API（可选）
- 📈 健康检查：`GET /health` 返回服务状态

<!-- 预览与桌面应用相关内容已移除，README 仅保留 Web 服务说明 -->

## 使用方法（Web）

### 本地运行（uv）

#### 安装依赖

```bash
uv venv
uv sync
```

#### 启动 Web 服务

```bash
# 使用默认配置启动
uv run -m LDDC.__main___fastapi

# 或指定端口和主机
uv run uvicorn LDDC.api.main:app --host 0.0.0.0 --port 8000

浏览器访问 `http://localhost:8000/`（静态前端）或 `http://localhost:8000/docs`（交互式 API 文档）。

#### Docker 部署与操作

使用项目根目录的 `Dockerfile` 构建并运行：

```bash
# 构建镜像
docker build -t lddc-fastapi:latest .

# 启动容器（映射 8000 端口）
docker run -d --name lddc-fastapi -p 8000:8000 lddc-fastapi:latest

# 查看健康状态与日志
curl http://localhost:8000/health
docker logs -f lddc-fastapi

# 停止并清理
docker stop lddc-fastapi && docker rm lddc-fastapi
```

容器入口为 `LDDC.api.main:app`，首页会自动挂载静态前端（如存在 `static/` 目录）。

##### 使用已发布镜像（GHCR）

已在 GitHub Container Registry 发布多架构镜像（支持 `linux/amd64` 和 `linux/arm64`）。

- 拉取最新版本：

```bash
docker pull ghcr.io/chenmozhijin/lddc-fastapi:latest
```

- 拉取指定发布版本（请在 Releases 查看 `vX.Y.Z` 标签）：

```bash
docker pull ghcr.io/chenmozhijin/lddc-fastapi:vX.Y.Z
```

- 直接运行已发布镜像：

```bash
docker run -d \
  --name lddc \
  -p 8000:8000 \
  ghcr.io/chenmozhijin/lddc-fastapi:latest

# 验证服务
curl http://localhost:8000/health
# 浏览器访问 http://localhost:8000/ 与 http://localhost:8000/docs
```

- 使用 Docker Compose（可覆盖镜像引用）：

项目根目录提供 `docker-compose.yml`，支持环境变量 `IMAGE_REF`：

```bash
# 指定镜像（可选）
echo IMAGE_REF=ghcr.io/chenmozhijin/lddc-fastapi:latest > .env

# 以后台方式启动
docker compose up -d

# 查看状态与日志
docker compose ps
docker compose logs -f
```

Compose 默认映射 `8000:8000`，并设置 `restart: unless-stopped`，适合长期运行。
```

#### API 使用示例

```python
import httpx

# 搜索（POST /api/search）
resp = httpx.post("http://localhost:8000/api/search", json={
    "keyword": "周杰伦 晴天",
    "source": "QM",            # 可选: QM/KG/NE/LRCLIB
    "search_type": "SONG",     # 可选: SONG/ALBUM/ARTIST
    "page": 1
})
data = resp.json()
song = data["results"][0]

# 下载歌词（POST /api/lyrics），返回 LRC 文本
lr = httpx.post("http://localhost:8000/api/lyrics", json={
    "song_id": song["id"],
    "title": song["title"],
    "artist": song["artist"],
    "album": song.get("album", ""),
    "duration": song.get("duration", 0),
    "source": song["source"]
})
print(lr.text)
```

<!-- 桌面应用相关内容已移除，详见原仓库 Wiki -->

## 项目结构

```
LDDC/
├── api/                  # FastAPI 应用
├── common/               # 通用模块（含 FastAPI 兼容实现）
├── core/                 # 核心功能（含 FastAPI 兼容实现）
├── static/               # 前端静态资源（如存在则挂载到 / ）
├── __main___fastapi.py   # 本地启动入口
├── Dockerfile            # 容器入口：LDDC.api.main:app
└── requirements.txt      # 依赖
```

## 感谢

部分功能实现参考了以下项目:

### 歌词解密

[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=WXRIW&repo=QQMusicDecoder)](https://github.com/WXRIW/QQMusicDecoder)
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=jixunmoe&repo=qmc-decode)](https://github.com/jixunmoe/qmc-decode)
