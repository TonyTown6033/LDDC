# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only

import httpx

from LDDC.common.data.cache import cache
from LDDC.common.config_fastapi import cfg
from LDDC.common.exceptions import TranslateError
from LDDC.common.models import Lyrics, LyricsData, TranslateTargetLanguage
from LDDC.common.version import __version__

from .models import BaseTranslator

lang_map = {
    TranslateTargetLanguage.SIMPLIFIED_CHINESE: "简体中文",
    TranslateTargetLanguage.TRADITIONAL_CHINESE: "繁体中文",
    TranslateTargetLanguage.ENGLISH: "English",
    TranslateTargetLanguage.JAPANESE: "日本語",
    TranslateTargetLanguage.KOREAN: "한국어",
    TranslateTargetLanguage.SPANISH: "Español",
    TranslateTargetLanguage.FRENCH: "Français",
    TranslateTargetLanguage.GERMAN: "Deutsch",
    TranslateTargetLanguage.PORTUGUESE: "Português",
    TranslateTargetLanguage.RUSSIAN: "Русский",
}


class OpenAITranslator(BaseTranslator):
    def is_available(self) -> bool:
        return cfg["openai_api_key"].strip() and cfg["openai_model"].strip() and cfg["openai_base_url"].strip()

    def translate_lyrics(self, lyrics: Lyrics) -> LyricsData:
        if not self.is_available():
            msg = "OpenAI API不可用。请检查您的配置。"
            raise TranslateError(msg)

        target_lang = lang_map[TranslateTargetLanguage[cfg["translate_target_lang"]]]
        base_url = cfg["openai_base_url"]
        api_key = cfg["openai_api_key"]
        model = cfg["openai_model"]

        texts = self.get_orig_lines(lyrics)  # 获取原始歌词行列表
        cache_key = (__version__, "openai", target_lang, tuple(texts).__hash__(), base_url, model)
        if cache_key in cache:
            return cache[cache_key]  # type: ignore[reportReturnType]
        orig_lines = "\n".join(f"{i + 1:02d}|{text}" for i, text in enumerate(texts))  # 格式化原始歌词行

        prompt = """You are a professional lyric translator with exceptional skills in preserving meaning, rhythm, and emotional nuance.
Translate the following lyrics into {target_lang} while maintaining:

1.  **Semantic Fidelity :** Translate the explicit and implicit meanings with the utmost accuracy. The core message and intent must be perfectly preserved.
2.  **Emotional and Stylistic Consistency :** Retain the original's tone (e.g., melancholic, joyful, sarcastic), imagery, and literary devices. The translation should evoke the same feelings as the original.
3.  **Natural Phrasing :** The translated lyrics must read as natural, idiomatic {target_lang}. Avoid literal, awkward, or machine-like phrasing. The goal is clarity and elegance, not necessarily singability.
4.  **Contextual Awareness :** Retain proper nouns, specific cultural references, and unique terms. Only adapt them if they are completely incomprehensible or culturally inappropriate in the target language.

**Input Format**
```
01|Original line 1
02|Original line 2
...
```

**Requirements**
- Translate line-by-line while maintaining original numbering
- Never combine or split lines
- Keep special symbols/formatting (e.g., ~, *, etc.)
- Retain proper nouns/terms unless culturally inappropriate
- Output only translated content in specified format

**Output Format**
```
01|Translated line 1
02|Translated line 2
...
```

**Current Task**
Translate these lyrics to {target_lang}:
```
{orig_lines}
```

Begin your translation now, responding ONLY with the formatted translated lyrics.""".replace("{orig_lines}", orig_lines).replace("{target_lang}", target_lang)  # noqa: E501

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"LDDC/{__version__}",
            "Accept-Charset": "utf-8",
            "Accept-Encoding": "gzip, deflate, br",
        }
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt},
            ],
            "stream": False,
        }
        if "siliconflow" in base_url:
            data["enable_thinking"] = False
        if "openrouter" in base_url:
            data["reasoning"] = {"max_tokens": 0}

        response = httpx.post(f"{base_url}/chat/completions", headers=headers, json=data, timeout=120)
        response.raise_for_status()
        response_json = response.json()
        content = response_json["choices"][0]["message"]["content"]
        content: str
        content = content.strip()
        if content.startswith("```"):
            content = content[3:].strip()  # Remove leading
        if content.endswith("```"):
            content = content[:-3].strip()  # Remove trailing
        content = content.strip()

        # 解析模型输出(index|trans)
        lines = [line for line in content.split("\n") if "|" in line]

        if len(lines) != len(texts):
            msg = f"模型输出的行数与输入的行数不匹配, 输入行数: {len(texts)}, 输出行数: {len(lines)}"
            raise ValueError(msg)

        trans_data = self.texts2data([line.split("|", 1)[1] for line in lines], lyrics)  # 将解析后的数据存储到texts2data中

        cache.set(cache_key, trans_data, expire=14400)
        return trans_data
