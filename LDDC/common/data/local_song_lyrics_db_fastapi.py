# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only
import sqlite3
import threading
from pathlib import Path
from typing import Any, Callable, Optional

from ..models import LyricInfo, SongInfo


class LocalSongLyricsDB:
    """本地歌曲歌词数据库（FastAPI版本，不依赖Qt）"""

    def __init__(self, db_path: Path) -> None:
        """初始化数据库

        :param db_path: 数据库文件路径
        """
        self.db_path = db_path
        self._lock = threading.Lock()
        self._callbacks: list[Callable[[], None]] = []
        self._init_db()

    def _init_db(self) -> None:
        """初始化数据库表"""
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                # 创建歌曲表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS songs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        artist TEXT NOT NULL,
                        album TEXT,
                        duration INTEGER,
                        file_path TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # 创建歌词表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS lyrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        song_id INTEGER NOT NULL,
                        content TEXT NOT NULL,
                        format TEXT,
                        language TEXT,
                        source TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (song_id) REFERENCES songs (id) ON DELETE CASCADE
                    )
                """)
                
                # 创建索引
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_songs_title_artist ON songs (title, artist)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_lyrics_song_id ON lyrics (song_id)")
                
                conn.commit()
            finally:
                conn.close()

    def connect_changed(self, callback: Callable[[], None]) -> None:
        """连接数据变更回调

        :param callback: 回调函数
        """
        with self._lock:
            if callback not in self._callbacks:
                self._callbacks.append(callback)

    def disconnect_changed(self, callback: Callable[[], None]) -> None:
        """断开数据变更回调

        :param callback: 回调函数
        """
        with self._lock:
            if callback in self._callbacks:
                self._callbacks.remove(callback)

    def _emit_changed(self) -> None:
        """触发数据变更信号"""
        with self._lock:
            for callback in self._callbacks:
                try:
                    callback()
                except Exception:
                    # 忽略回调中的异常
                    pass

    def add_song(self, song_info: SongInfo) -> int:
        """添加歌曲

        :param song_info: 歌曲信息
        :return: 歌曲ID
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO songs (title, artist, album, duration, file_path)
                    VALUES (?, ?, ?, ?, ?)
                """, (song_info.title, song_info.artist, song_info.album, 
                      song_info.duration, song_info.file_path))
                song_id = cursor.lastrowid
                conn.commit()
                self._emit_changed()
                return song_id
            finally:
                conn.close()

    def add_lyrics(self, song_id: int, lyric_info: LyricInfo) -> int:
        """添加歌词

        :param song_id: 歌曲ID
        :param lyric_info: 歌词信息
        :return: 歌词ID
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO lyrics (song_id, content, format, language, source)
                    VALUES (?, ?, ?, ?, ?)
                """, (song_id, lyric_info.content, lyric_info.format,
                      lyric_info.language, lyric_info.source))
                lyric_id = cursor.lastrowid
                conn.commit()
                self._emit_changed()
                return lyric_id
            finally:
                conn.close()

    def get_song_by_id(self, song_id: int) -> Optional[SongInfo]:
        """根据ID获取歌曲

        :param song_id: 歌曲ID
        :return: 歌曲信息
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
                row = cursor.fetchone()
                if row:
                    return SongInfo(
                        title=row[1],
                        artist=row[2],
                        album=row[3],
                        duration=row[4],
                        file_path=row[5]
                    )
                return None
            finally:
                conn.close()

    def get_lyrics_by_song_id(self, song_id: int) -> list[LyricInfo]:
        """根据歌曲ID获取歌词

        :param song_id: 歌曲ID
        :return: 歌词列表
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM lyrics WHERE song_id = ?", (song_id,))
                rows = cursor.fetchall()
                lyrics = []
                for row in rows:
                    lyrics.append(LyricInfo(
                        content=row[2],
                        format=row[3],
                        language=row[4],
                        source=row[5]
                    ))
                return lyrics
            finally:
                conn.close()

    def search_songs(self, title: Optional[str] = None, artist: Optional[str] = None) -> list[tuple[int, SongInfo]]:
        """搜索歌曲

        :param title: 歌曲标题（可选）
        :param artist: 艺术家（可选）
        :return: 歌曲ID和信息的元组列表
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                query = "SELECT * FROM songs WHERE 1=1"
                params = []
                
                if title:
                    query += " AND title LIKE ?"
                    params.append(f"%{title}%")
                
                if artist:
                    query += " AND artist LIKE ?"
                    params.append(f"%{artist}%")
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                results = []
                for row in rows:
                    song_info = SongInfo(
                        title=row[1],
                        artist=row[2],
                        album=row[3],
                        duration=row[4],
                        file_path=row[5]
                    )
                    results.append((row[0], song_info))
                
                return results
            finally:
                conn.close()

    def update_song(self, song_id: int, song_info: SongInfo) -> bool:
        """更新歌曲信息

        :param song_id: 歌曲ID
        :param song_info: 新的歌曲信息
        :return: 是否更新成功
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE songs 
                    SET title = ?, artist = ?, album = ?, duration = ?, file_path = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (song_info.title, song_info.artist, song_info.album,
                      song_info.duration, song_info.file_path, song_id))
                
                success = cursor.rowcount > 0
                if success:
                    conn.commit()
                    self._emit_changed()
                return success
            finally:
                conn.close()

    def delete_song(self, song_id: int) -> bool:
        """删除歌曲（及其相关歌词）

        :param song_id: 歌曲ID
        :return: 是否删除成功
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                # 由于外键约束，删除歌曲会自动删除相关歌词
                cursor.execute("DELETE FROM songs WHERE id = ?", (song_id,))
                
                success = cursor.rowcount > 0
                if success:
                    conn.commit()
                    self._emit_changed()
                return success
            finally:
                conn.close()

    def delete_lyrics(self, lyric_id: int) -> bool:
        """删除歌词

        :param lyric_id: 歌词ID
        :return: 是否删除成功
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM lyrics WHERE id = ?", (lyric_id,))
                
                success = cursor.rowcount > 0
                if success:
                    conn.commit()
                    self._emit_changed()
                return success
            finally:
                conn.close()

    def get_all_songs(self) -> list[tuple[int, SongInfo]]:
        """获取所有歌曲

        :return: 歌曲ID和信息的元组列表
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM songs ORDER BY created_at DESC")
                rows = cursor.fetchall()
                
                results = []
                for row in rows:
                    song_info = SongInfo(
                        title=row[1],
                        artist=row[2],
                        album=row[3],
                        duration=row[4],
                        file_path=row[5]
                    )
                    results.append((row[0], song_info))
                
                return results
            finally:
                conn.close()

    def clear_all(self) -> None:
        """清空所有数据"""
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM lyrics")
                cursor.execute("DELETE FROM songs")
                conn.commit()
                self._emit_changed()
            finally:
                conn.close()

    def get_stats(self) -> dict[str, int]:
        """获取数据库统计信息

        :return: 统计信息字典
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM songs")
                song_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM lyrics")
                lyric_count = cursor.fetchone()[0]
                
                return {
                    "songs": song_count,
                    "lyrics": lyric_count
                }
            finally:
                conn.close()