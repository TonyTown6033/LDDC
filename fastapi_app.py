#!/usr/bin/env python3
"""
LDDC FastAPI 精简版
提供歌词搜索和下载的API接口
"""
import sys
import os
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# 添加LDDC模块路径
sys.path.insert(0, os.path.abspath('.'))

try:
    from LDDC.common.models import SongInfo, Source, SearchType, LyricsFormat
    from LDDC.core.api.lyrics import search, get_lyrics
    from LDDC.core.converter.lrc import lrc_converter
except ImportError as e:
    print(f"导入LDDC模块失败: {e}")
    sys.exit(1)

app = FastAPI(
    title="LDDC API",
    description="LDDC 歌词下载服务 API",
    version="1.0.0"
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 数据模型
class SearchRequest(BaseModel):
    keyword: str
    source: str = "QM"  # QM, KG, NE, LRCLIB
    search_type: str = "SONG"  # SONG, ALBUM, ARTIST
    page: int = 1

class SongInfoResponse(BaseModel):
    id: str
    title: str
    artist: str
    album: str
    duration: int
    source: str

class SearchResponse(BaseModel):
    results: List[SongInfoResponse]
    total: int

class LyricsRequest(BaseModel):
    song_id: str
    title: str
    artist: str
    album: str
    duration: int
    source: str

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
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return {"message": "LDDC API 服务正在运行", "version": "1.0.0"}

@app.post("/search", response_model=SearchResponse)
async def search_lyrics(request: SearchRequest):
    """搜索歌曲"""
    try:
        # 验证参数
        if request.source not in SOURCE_MAP:
            raise HTTPException(status_code=400, detail=f"不支持的音源: {request.source}")
        
        if request.search_type not in SEARCH_TYPE_MAP:
            raise HTTPException(status_code=400, detail=f"不支持的搜索类型: {request.search_type}")
        
        # 执行搜索
        source = SOURCE_MAP[request.source]
        search_type = SEARCH_TYPE_MAP[request.search_type]
        
        results = search(source, request.keyword, search_type, request.page)
        
        # 转换结果
        song_list = []
        for song in results:
            song_info = SongInfoResponse(
                id=song.id or "",
                title=song.title or "",
                artist=str(song.artist) if song.artist else "",
                album=song.album or "",
                duration=song.duration or 0,
                source=request.source
            )
            song_list.append(song_info)
        
        return SearchResponse(results=song_list, total=len(song_list))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

@app.post("/lyrics", response_class=PlainTextResponse)
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
        lyrics = get_lyrics(song_info)
        
        if not lyrics:
            raise HTTPException(status_code=404, detail="未找到歌词")
        
        # 转换为LRC格式
        lrc_content = lrc_converter(lyrics.tags, lyrics, LyricsFormat.LINEBYLINELRC, {}, ["orig"])
        
        if not lrc_content:
            raise HTTPException(status_code=404, detail="歌词转换失败")
        
        return lrc_content
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下载歌词失败: {str(e)}")

@app.get("/search_simple")
async def search_simple(
    keyword: str = Query(..., description="搜索关键词"),
    source: str = Query("QM", description="音源 (QM/KG/NE/LRCLIB)"),
    page: int = Query(1, description="页码")
):
    """简化的搜索接口"""
    request = SearchRequest(keyword=keyword, source=source, page=page)
    return await search_lyrics(request)

@app.get("/lyrics_simple")
async def lyrics_simple(
    song_id: str,
    title: str,
    artist: str,
    album: str = "",
    source: str = "QM"
):
    """简化的歌词下载接口"""
    request = LyricsRequest(
        song_id=song_id,
        title=title,
        artist=artist,
        album=album,
        duration=0,
        source=source
    )
    return await download_lyrics(request)

if __name__ == "__main__":
    print("启动 LDDC FastAPI 服务...")
    uvicorn.run(app, host="0.0.0.0", port=8000)