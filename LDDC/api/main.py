# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only

"""LDDC FastAPI主应用"""

import asyncio
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

from LDDC.common.models._enums import Source, SearchType, LyricsFormat
from LDDC.common.models._info import SongInfo
from LDDC.core.api.lyrics import search, get_lyrics
from LDDC.core.converter.lrc import lrc_converter
from LDDC.common.logger_fastapi import get_logger

logger = get_logger()

app = FastAPI(
    title="LDDC API",
    description="LDDC 歌词下载服务 API",
    version="1.0.0"
)

# 挂载静态文件
static_dir = Path(__file__).parent.parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# 数据模型
class SearchRequest(BaseModel):
    keyword: str
    source: str = "QM"
    search_type: str = "SONG"
    page: int = 1

class LyricsRequest(BaseModel):
    song_id: str
    title: str
    artist: str
    album: str = ""
    duration: int = 0
    source: str = "QM"

# 源映射
SOURCE_MAP = {
    "QM": Source.QM,
    "KG": Source.KG, 
    "NE": Source.NE,
    "LRCLIB": Source.LRCLIB
}

SEARCH_TYPE_MAP = {
    "SONG": SearchType.SONG,
    "ALBUM": SearchType.ALBUM,
    "ARTIST": SearchType.ARTIST
}

@app.get("/", response_class=HTMLResponse)
async def root():
    """前端页面"""
    try:
        html_file = static_dir / "index.html"
        if html_file.exists():
            with open(html_file, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"读取前端页面失败: {e}")
    
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>LDDC API</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>LDDC API 服务</h1>
        <p>服务正在运行</p>
        <p><a href="/docs">查看API文档</a></p>
    </body>
    </html>
    """)

@app.post("/api/search")
async def search_lyrics(request: SearchRequest):
    """搜索歌词"""
    try:
        # 验证音源
        if request.source not in SOURCE_MAP:
            raise HTTPException(status_code=400, detail=f"不支持的音源: {request.source}")
        
        # 验证搜索类型
        if request.search_type not in SEARCH_TYPE_MAP:
            raise HTTPException(status_code=400, detail=f"不支持的搜索类型: {request.search_type}")
        
        source = SOURCE_MAP[request.source]
        search_type = SEARCH_TYPE_MAP[request.search_type]
        
        # 执行搜索
        logger.info(f"搜索参数: source={source}, keyword={request.keyword}, search_type={search_type}, page={request.page}")
        results = await asyncio.to_thread(
            search,
            source,
            request.keyword,
            search_type,
            request.page
        )
        
        if not results:
            return {"results": [], "total": 0}
        
        # 转换结果格式
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "title": result.title,
                "artist": result.artist,
                "album": result.album,
                "duration": result.duration,
                "source": result.source.name
            })
        
        return {"results": formatted_results, "total": len(formatted_results)}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"搜索失败: {e}")
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

@app.post("/api/lyrics", response_class=PlainTextResponse)
async def download_lyrics(request: LyricsRequest):
    """下载歌词并返回LRC格式"""
    try:
        # 验证音源
        if request.source not in SOURCE_MAP:
            raise HTTPException(status_code=400, detail=f"不支持的音源: {request.source}")
        
        # 创建SongInfo对象
        source = SOURCE_MAP[request.source]
        song_info = SongInfo(
            id=request.song_id,
            title=request.title,
            artist=request.artist,
            album=request.album,
            duration=request.duration,
            source=source
        )
        
        # 获取歌词
        lyrics = await asyncio.to_thread(get_lyrics, song_info)
        
        if not lyrics:
            raise HTTPException(status_code=404, detail="未找到歌词")
        
        # 转换为LRC格式
        lrc_content = lrc_converter(
            lyrics.tags, 
            lyrics, 
            LyricsFormat.LINEBYLINELRC, 
            {}, 
            ["orig"]
        )
        
        if not lrc_content:
            raise HTTPException(status_code=404, detail="歌词转换失败")
        
        return lrc_content
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"下载歌词失败: {e}")
        raise HTTPException(status_code=500, detail=f"下载歌词失败: {str(e)}")

@app.get("/api/search")
async def search_simple(
    keyword: str = Query(..., description="搜索关键词"),
    source: str = Query("QM", description="音源 (QM/KG/NE/LRCLIB)"),
    search_type: str = Query("SONG", description="搜索类型 (SONG/ALBUM/ARTIST)"),
    page: int = Query(1, description="页码")
):
    """简化的搜索接口"""
    request = SearchRequest(
        keyword=keyword, 
        source=source, 
        search_type=search_type,
        page=page
    )
    return await search_lyrics(request)

@app.get("/api/lyrics")
async def lyrics_simple(
    song_id: str = Query(..., description="歌曲ID"),
    title: str = Query(..., description="歌曲标题"),
    artist: str = Query(..., description="艺术家"),
    album: str = Query("", description="专辑"),
    duration: int = Query(0, description="时长(秒)"),
    source: str = Query("QM", description="音源")
):
    """简化的歌词下载接口"""
    request = LyricsRequest(
        song_id=song_id,
        title=title,
        artist=artist,
        album=album,
        duration=duration,
        source=source
    )
    return await download_lyrics(request)

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok", "message": "LDDC API服务正常运行"}