# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only
import locale
import os
from pathlib import Path
from typing import Optional


class Translator:
    """简化的翻译器（FastAPI版本，不依赖Qt）"""
    
    def __init__(self) -> None:
        self._translations: dict[str, dict[str, str]] = {}
        self._current_language = "en"
    
    def load_translation(self, language: str, translation_file: Path) -> bool:
        """加载翻译文件
        
        :param language: 语言代码
        :param translation_file: 翻译文件路径
        :return: 是否加载成功
        """
        try:
            if translation_file.exists():
                # 这里可以实现具体的翻译文件加载逻辑
                # 例如加载JSON或其他格式的翻译文件
                self._translations[language] = {}
                return True
        except Exception:
            pass
        return False
    
    def set_language(self, language: str) -> None:
        """设置当前语言
        
        :param language: 语言代码
        """
        self._current_language = language
    
    def tr(self, text: str, context: Optional[str] = None) -> str:
        """翻译文本
        
        :param text: 要翻译的文本
        :param context: 上下文（可选）
        :return: 翻译后的文本
        """
        if self._current_language in self._translations:
            translations = self._translations[self._current_language]
            key = f"{context}.{text}" if context else text
            return translations.get(key, text)
        return text


def get_system_language() -> str:
    """获取系统语言
    
    :return: 语言代码
    """
    try:
        # 尝试从环境变量获取语言设置
        lang = os.environ.get('LANG', '')
        if lang:
            # 提取语言代码（例如从 'zh_CN.UTF-8' 提取 'zh'）
            return lang.split('_')[0].split('.')[0]
        
        # 使用locale模块获取系统默认语言
        system_locale = locale.getdefaultlocale()[0]
        if system_locale:
            return system_locale.split('_')[0]
    except Exception:
        pass
    
    # 默认返回英语
    return "en"


def load_translation(app_name: str, language: str, translation_dir: Path) -> bool:
    """加载应用程序翻译
    
    :param app_name: 应用程序名称
    :param language: 语言代码
    :param translation_dir: 翻译文件目录
    :return: 是否加载成功
    """
    try:
        translation_file = translation_dir / f"{app_name}_{language}.json"
        if translation_file.exists():
            # 这里可以实现具体的翻译文件加载逻辑
            return True
    except Exception:
        pass
    return False


# 全局翻译器实例
_translator = Translator()


def get_translator() -> Translator:
    """获取全局翻译器实例
    
    :return: 翻译器实例
    """
    return _translator


def tr(text: str, context: Optional[str] = None) -> str:
    """全局翻译函数
    
    :param text: 要翻译的文本
    :param context: 上下文（可选）
    :return: 翻译后的文本
    """
    return _translator.tr(text, context)


def set_language(language: str) -> None:
    """设置全局语言
    
    :param language: 语言代码
    """
    _translator.set_language(language)


def init_translation(app_name: str, translation_dir: Optional[Path] = None) -> None:
    """初始化翻译系统
    
    :param app_name: 应用程序名称
    :param translation_dir: 翻译文件目录（可选）
    """
    # 获取系统语言
    system_lang = get_system_language()
    
    # 设置当前语言
    set_language(system_lang)
    
    # 如果提供了翻译目录，尝试加载翻译文件
    if translation_dir and translation_dir.exists():
        load_translation(app_name, system_lang, translation_dir)