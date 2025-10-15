# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only
import re
import struct
from collections.abc import Callable
from pathlib import Path
from typing import Literal, overload

from mutagen import File, FileType, MutagenError  # type: ignore[reportPrivateImportUsage] mutagen中的File被误定义为私有 quodlibet/mutagen#647
from mutagen.apev2 import APEv2
from mutagen.asf import ASFTags
from mutagen.flac import VCommentDict  # type: ignore[reportPrivateImportUsage]
from mutagen.id3 import ID3, SYLT, USLT  # type: ignore[reportPrivateImportUsage]
from mutagen.mp4 import MP4Tags

from LDDC.common.data.config_fastapi import get_config
from LDDC.common.exceptions_fastapi import DropError, FileTypeError, GetSongInfoError
from LDDC.common.logger_fastapi import get_logger
from LDDC.common.models import Artist, Lyrics, SongInfo, Source
from LDDC.core.parser.cue import parse_cue

logger = get_logger(__name__)

AUDIO_FORMATS = [
    "3g2",
    "aac",
    "aif",
    "ape",
    "apev2",
    "dff",
    "dsf",
    "flac",
    "m4a",
    "m4b",
    "mid",
    "mp3",
    "mp4",
    "mpc",
    "ofr",
    "ofs",
    "ogg",
    "oggflac",
    "oggtheora",
    "opus",
    "spx",
    "tak",
    "tta",
    "wav",
    "wma",
    "wv",
]


def get_audio_file_infos(file_path: Path) -> list[SongInfo]:
    """获取音频文件信息

    :param file_path: 音频文件路径
    :return: 歌曲信息列表
    """
    if not file_path.exists():
        msg = f"文件不存在: {file_path}"
        raise FileNotFoundError(msg)

    if file_path.suffix.lower().lstrip('.') not in AUDIO_FORMATS:
        msg = f"不支持的音频格式: {file_path.suffix}"
        raise FileTypeError(msg)

    try:
        # 使用mutagen获取音频文件信息
        audio_file = File(file_path)
        if audio_file is None:
            msg = f"无法读取音频文件: {file_path}"
            raise GetSongInfoError(msg)

        # 提取基本信息
        title = None
        artist = None
        album = None
        duration = None

        if hasattr(audio_file, 'info') and audio_file.info:
            duration = int(audio_file.info.length * 1000) if audio_file.info.length else None

        # 提取标签信息
        if audio_file.tags:
            # 处理不同格式的标签
            if isinstance(audio_file.tags, ID3):
                title = str(audio_file.tags.get('TIT2', [''])[0]) if audio_file.tags.get('TIT2') else None
                artist = str(audio_file.tags.get('TPE1', [''])[0]) if audio_file.tags.get('TPE1') else None
                album = str(audio_file.tags.get('TALB', [''])[0]) if audio_file.tags.get('TALB') else None
            elif isinstance(audio_file.tags, (VCommentDict, APEv2)):
                title = audio_file.tags.get('TITLE', [None])[0] if audio_file.tags.get('TITLE') else None
                artist = audio_file.tags.get('ARTIST', [None])[0] if audio_file.tags.get('ARTIST') else None
                album = audio_file.tags.get('ALBUM', [None])[0] if audio_file.tags.get('ALBUM') else None
            elif isinstance(audio_file.tags, MP4Tags):
                title = audio_file.tags.get('\xa9nam', [None])[0] if audio_file.tags.get('\xa9nam') else None
                artist = audio_file.tags.get('\xa9ART', [None])[0] if audio_file.tags.get('\xa9ART') else None
                album = audio_file.tags.get('\xa9alb', [None])[0] if audio_file.tags.get('\xa9alb') else None
            elif isinstance(audio_file.tags, ASFTags):
                title = str(audio_file.tags.get('Title', [''])[0]) if audio_file.tags.get('Title') else None
                artist = str(audio_file.tags.get('Author', [''])[0]) if audio_file.tags.get('Author') else None
                album = str(audio_file.tags.get('AlbumTitle', [''])[0]) if audio_file.tags.get('AlbumTitle') else None

        # 如果没有标题，使用文件名
        if not title:
            title = file_path.stem

        # 创建艺术家对象
        artist_obj = Artist(artist) if artist else None

        # 创建歌曲信息对象
        song_info = SongInfo(
            title=title,
            artist=artist_obj,
            album=album,
            duration=duration,
            path=file_path
        )

        return [song_info]

    except Exception as e:
        msg = f"获取音频文件信息时发生错误: {e}"
        raise GetSongInfoError(msg) from e


def has_lyrics(file_path: Path | str) -> bool:
    """检查音频文件是否包含歌词

    :param file_path: 音频文件路径
    :return: 是否包含歌词
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not file_path.exists():
        return False

    try:
        audio_file = File(file_path)
        if audio_file is None or not audio_file.tags:
            return False

        # 检查不同格式的歌词标签
        if isinstance(audio_file.tags, ID3):
            # 检查USLT（非同步歌词）和SYLT（同步歌词）标签
            return bool(audio_file.tags.getall('USLT') or audio_file.tags.getall('SYLT'))
        elif isinstance(audio_file.tags, (VCommentDict, APEv2)):
            # 检查LYRICS标签
            return bool(audio_file.tags.get('LYRICS'))
        elif isinstance(audio_file.tags, MP4Tags):
            # 检查\xa9lyr标签
            return bool(audio_file.tags.get('\xa9lyr'))
        elif isinstance(audio_file.tags, ASFTags):
            # 检查WM/Lyrics标签
            return bool(audio_file.tags.get('WM/Lyrics'))

    except Exception:
        pass

    return False


class FileDropInfo:
    """简化的文件拖拽信息类（替代QMimeData）"""
    
    def __init__(self, file_paths: list[str | Path]):
        """初始化文件拖拽信息
        
        :param file_paths: 文件路径列表
        """
        self.file_paths = [Path(p) for p in file_paths]
    
    def has_urls(self) -> bool:
        """检查是否有URL"""
        return bool(self.file_paths)
    
    def urls(self) -> list[Path]:
        """获取URL列表"""
        return self.file_paths


@overload
def parse_drop_infos(
    drop_info: FileDropInfo,
    first: Literal[True] = True,
    progress: Callable[[str, int, int], None] | None = None,
    running: Callable[[], bool] | None = None,
) -> SongInfo: ...


@overload
def parse_drop_infos(
    drop_info: FileDropInfo,
    first: Literal[False] = False,
    progress: Callable[[str, int, int], None] | None = None,
    running: Callable[[], bool] | None = None,
) -> list[SongInfo]: ...


def parse_drop_infos(
    drop_info: FileDropInfo,
    first: bool = True,
    progress: Callable[[str, int, int], None] | None = None,
    running: Callable[[], bool] | None = None,
) -> list[SongInfo] | SongInfo:
    """解析拖拽的文件（FastAPI版本）

    :param drop_info: 文件拖拽信息
    :param first: 是否只获取第一个文件
    :param progress: 进度回调函数
    :param running: 是否正在运行
    :return: 解析后的文件信息
    """
    if not drop_info.has_urls():
        msg = "没有可处理的文件"
        raise DropError(msg)

    paths = drop_info.urls()
    all_song_infos: list[SongInfo] = []

    for i, path in enumerate(paths):
        if running and not running():
            break

        if progress:
            progress(f"处理文件: {path.name}", i, len(paths))

        try:
            if path.is_file():
                # 处理单个文件
                if path.suffix.lower().lstrip('.') in AUDIO_FORMATS:
                    song_infos = get_audio_file_infos(path)
                    all_song_infos.extend(song_infos)
                elif path.suffix.lower() == '.cue':
                    # 处理CUE文件
                    try:
                        cue_infos = parse_cue(path)
                        all_song_infos.extend(cue_infos)
                    except Exception as e:
                        logger.warning(f"解析CUE文件失败: {path}, 错误: {e}")
            elif path.is_dir():
                # 处理目录
                for audio_format in AUDIO_FORMATS:
                    for audio_file in path.rglob(f"*.{audio_format}"):
                        if running and not running():
                            break
                        try:
                            song_infos = get_audio_file_infos(audio_file)
                            all_song_infos.extend(song_infos)
                        except Exception as e:
                            logger.warning(f"处理音频文件失败: {audio_file}, 错误: {e}")

        except Exception as e:
            logger.error(f"处理路径失败: {path}, 错误: {e}")

        if first and all_song_infos:
            break

    if not all_song_infos:
        msg = "没有找到有效的音频文件"
        raise DropError(msg)

    return all_song_infos[0] if first else all_song_infos


def parse_file_paths(
    file_paths: list[str | Path],
    first: bool = True,
    progress: Callable[[str, int, int], None] | None = None,
    running: Callable[[], bool] | None = None,
) -> list[SongInfo] | SongInfo:
    """解析文件路径列表

    :param file_paths: 文件路径列表
    :param first: 是否只获取第一个文件
    :param progress: 进度回调函数
    :param running: 是否正在运行
    :return: 解析后的文件信息
    """
    drop_info = FileDropInfo(file_paths)
    return parse_drop_infos(drop_info, first, progress, running)