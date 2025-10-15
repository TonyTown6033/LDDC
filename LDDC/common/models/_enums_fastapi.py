# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only
from enum import Enum
from typing import TYPE_CHECKING

# 移除PySide6依赖，使用标准库替代
if TYPE_CHECKING:
    # 仅在类型检查时导入，避免运行时依赖
    pass


class Direction(Enum):
    """方向枚举"""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class SearchType(Enum):
    """搜索类型枚举"""
    TITLE = "title"
    ARTIST = "artist"
    ALBUM = "album"
    LYRICS = "lyrics"


class LyricsFormat(Enum):
    """歌词格式枚举"""
    VERBATIM = "verbatim"
    LRC = "lrc"
    ENHANCED_LRC = "enhanced_lrc"
    SRT = "srt"
    ASS = "ass"


class LyricsType(Enum):
    """歌词类型枚举"""
    ORIGINAL = "original"
    TRANSLATED = "translated"
    ROMANIZED = "romanized"


class QrcType(Enum):
    """QRC类型枚举"""
    WORD = "word"
    SYLLABLE = "syllable"


class Source(Enum):
    """来源枚举"""
    NETEASE = "netease"
    QQ = "qq"
    KUGOU = "kugou"
    KUWO = "kuwo"
    MIGU = "migu"
    LOCAL = "local"


class TranslateSource(Enum):
    """翻译来源枚举"""
    GOOGLE = "google"
    BAIDU = "baidu"
    YOUDAO = "youdao"
    DEEPL = "deepl"


class TranslateTargetLanguage(Enum):
    """翻译目标语言枚举"""
    ZH_CN = "zh-cn"
    ZH_TW = "zh-tw"
    EN = "en"
    JA = "ja"
    KO = "ko"
    FR = "fr"
    DE = "de"
    ES = "es"
    RU = "ru"


class Language(Enum):
    """语言枚举"""
    ZH_CN = "zh_CN"
    ZH_TW = "zh_TW"
    EN = "en"
    JA = "ja"
    KO = "ko"
    FR = "fr"
    DE = "de"
    ES = "es"
    RU = "ru"
    AUTO = "auto"

    @classmethod
    def get_system_language(cls) -> "Language":
        """获取系统语言"""
        import locale
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                if system_locale.startswith('zh_CN'):
                    return cls.ZH_CN
                elif system_locale.startswith('zh_TW') or system_locale.startswith('zh_HK'):
                    return cls.ZH_TW
                elif system_locale.startswith('en'):
                    return cls.EN
                elif system_locale.startswith('ja'):
                    return cls.JA
                elif system_locale.startswith('ko'):
                    return cls.KO
                elif system_locale.startswith('fr'):
                    return cls.FR
                elif system_locale.startswith('de'):
                    return cls.DE
                elif system_locale.startswith('es'):
                    return cls.ES
                elif system_locale.startswith('ru'):
                    return cls.RU
        except Exception:
            pass
        return cls.EN  # 默认返回英语


class SongListType(Enum):
    """歌曲列表类型枚举"""
    PLAYLIST = "playlist"
    ALBUM = "album"
    ARTIST = "artist"
    SEARCH = "search"


class FileNameMode(Enum):
    """文件名模式枚举"""
    TITLE = "title"
    ARTIST_TITLE = "artist_title"
    TITLE_ARTIST = "title_artist"
    CUSTOM = "custom"


class SaveMode(Enum):
    """保存模式枚举"""
    OVERWRITE = "overwrite"
    SKIP = "skip"
    RENAME = "rename"
    ASK = "ask"


# 为了保持向后兼容性，提供一个简单的翻译函数
def tr(text: str) -> str:
    """简单的翻译函数（替代QCoreApplication.translate）"""
    # 这里可以集成实际的翻译逻辑
    # 目前只是返回原文本
    return text


# 为枚举添加翻译支持
def get_enum_display_name(enum_value: Enum) -> str:
    """获取枚举的显示名称"""
    display_names = {
        # Direction
        Direction.UP: tr("向上"),
        Direction.DOWN: tr("向下"),
        Direction.LEFT: tr("向左"),
        Direction.RIGHT: tr("向右"),
        
        # SearchType
        SearchType.TITLE: tr("标题"),
        SearchType.ARTIST: tr("艺术家"),
        SearchType.ALBUM: tr("专辑"),
        SearchType.LYRICS: tr("歌词"),
        
        # LyricsFormat
        LyricsFormat.VERBATIM: tr("纯文本"),
        LyricsFormat.LRC: tr("LRC"),
        LyricsFormat.ENHANCED_LRC: tr("增强LRC"),
        LyricsFormat.SRT: tr("SRT"),
        LyricsFormat.ASS: tr("ASS"),
        
        # LyricsType
        LyricsType.ORIGINAL: tr("原文"),
        LyricsType.TRANSLATED: tr("翻译"),
        LyricsType.ROMANIZED: tr("音译"),
        
        # Source
        Source.NETEASE: tr("网易云音乐"),
        Source.QQ: tr("QQ音乐"),
        Source.KUGOU: tr("酷狗音乐"),
        Source.KUWO: tr("酷我音乐"),
        Source.MIGU: tr("咪咕音乐"),
        Source.LOCAL: tr("本地"),
        
        # Language
        Language.ZH_CN: tr("简体中文"),
        Language.ZH_TW: tr("繁体中文"),
        Language.EN: tr("English"),
        Language.JA: tr("日本語"),
        Language.KO: tr("한국어"),
        Language.FR: tr("Français"),
        Language.DE: tr("Deutsch"),
        Language.ES: tr("Español"),
        Language.RU: tr("Русский"),
        Language.AUTO: tr("自动"),
    }
    
    return display_names.get(enum_value, str(enum_value.value))