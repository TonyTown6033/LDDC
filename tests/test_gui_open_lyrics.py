# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only

import os

import pytest
from PySide6.QtWidgets import QFileDialog
from pytestqt.qtbot import QtBot

from LDDC.utils.enum import LyricsFormat

from .helper import grab, screenshot_path, select_file, verify_lyrics


def change_preview_format(qtbot: QtBot, lyrics_format: LyricsFormat) -> None:
    from LDDC.view.main_window import main_window

    if main_window.open_lyrics_widget.lyricsformat_comboBox.currentIndex() != lyrics_format.value:
        orig_text = main_window.open_lyrics_widget.plainTextEdit.toPlainText()
        main_window.open_lyrics_widget.lyricsformat_comboBox.setCurrentIndex(lyrics_format.value)

        def check_preview_result() -> bool:
            return bool(len(main_window.open_lyrics_widget.plainTextEdit.toPlainText()) > 20 and
                        main_window.open_lyrics_widget.plainTextEdit.toPlainText() != orig_text)

        qtbot.waitUntil(check_preview_result)
        qtbot.wait(20)


def test_gui_open_lyrics(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> None:
    from LDDC.view.main_window import main_window

    main_window.show()
    main_window.set_current_widget(2)
    qtbot.wait(300)  # 等待窗口加载完成
    grab(main_window, os.path.join(screenshot_path, "open_lyrics"))

    files = {
        "qrc": "铃木木乃美 (鈴木このみ) - アスタロア (Asterlore)"
        " - 278 - PCゲーム『Summer Pockets REFLECTION BLUE』オープニングテーマ「アスタロア」 (Asterlore)_qm.qrc",
        "krc": "鈴木このみ - アスタロア (Asterlore).krc",
    }
    monkeypatch.setattr(QFileDialog, "open", lambda *args, **kwargs: None)  # noqa: ARG005
    for file_format, name in files.items():
        path = os.path.join(os.path.dirname(__file__), "data", name)
        main_window.open_lyrics_widget.open_pushButton.click()
        select_file(main_window.open_lyrics_widget, path)
        qtbot.wait(150)
        grab(main_window, os.path.join(screenshot_path, f"open_lyrics_{file_format}"))
        main_window.open_lyrics_widget.convert_pushButton.click()
        qtbot.wait(40)
        for lyrics_format in [LyricsFormat.VERBATIMLRC, LyricsFormat.LINEBYLINELRC, LyricsFormat.ENHANCEDLRC, LyricsFormat.ASS, LyricsFormat.SRT]:
            change_preview_format(qtbot, lyrics_format)
            if lyrics_format in [LyricsFormat.VERBATIMLRC, LyricsFormat.LINEBYLINELRC, LyricsFormat.ENHANCEDLRC]:
                verify_lyrics(main_window.open_lyrics_widget.plainTextEdit.toPlainText())
            qtbot.wait(40)
            grab(main_window, os.path.join(screenshot_path, f"open_lyrics_{file_format}_{lyrics_format.name.lower()}"))
        qtbot.wait(150)
