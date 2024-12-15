# LDDC

[中文](./README.md) | English | [日本語](./README_ja.md)

> Accurate Lyrics (verbatim lyrics) Download, Decryption, and Conversion

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/015f636391584ffc82790ff7038da5ca)](https://app.codacy.com/gh/chenmozhijin/LDDC/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/chenmozhijin/LDDC/total)](https://github.com/chenmozhijin/LDDC/releases/latest)
[![Static Badge](https://img.shields.io/badge/Python-3.10%2B-brightgreen)](https://www.python.org/downloads/)
[![Static Badge](https://img.shields.io/badge/License-GPLv3-blue)](https://github.com/chenmozhijin/LDDC/blob/main/LICENSE)
[![release](https://img.shields.io/github/v/release/chenmozhijin/LDDC?color=blue)](https://github.com/chenmozhijin/LDDC/releases/latest)

## Features

- [x] Search for singles, albums, and playlists on QQ Music, Kugou Music, and NetEase Cloud Music
- [x] Drag the song to the search interface to automatically search and match the lyrics
- [x] One-click match lyrics for local song files
- [x] One-click download of lyrics for entire albums and playlists
- [x] Support for saving in multiple formats (verbatim lrc,line by line lrc,Enhanced LRC, srt, ass)
- [x] Double-click to preview lyrics and save directly
- [x] Merge lyrics of various types (original, translated, romanized) at will
- [x] Save path with various placeholders for arbitrary combinations
- [x] Support for opening locally encrypted lyrics
- [x] Multi-platform support
- [x] Desktop Lyrics (currently only supports foobar2000: [foo_lddc](https://github.com/chenmozhijin/foo_lddc))
    1. Multi-threaded automatic search to quickly match lyrics (most lyrics are in word-for-word style)
    2. Supports displaying lyrics in karaoke style
    3. Supports displaying the original text, translation, and romanization in separate lines
    4. Supports fade in/out effects, and automatically matches the screen refresh rate to ensure smoothness
    5. Supports manual selection of lyrics through a window similar to the search interface
    6. Caches characters to achieve low resource usage
    7. Supports custom gradient colors for characters

## Preview

### Drag songs to quickly match lyrics

![gif](img/drop.gif)

### Search interface

![image](img/en_1.jpg)

### Open the lyrics/local matching/settings interface

![image](img/en_2.jpg)

### Desktop Lyrics

![image](img/en_3.jpg)
![gif](img/desktop_lyrics.gif)

## Usage

See [LDDC User Guide](https://github.com/chenmozhijin/LDDC/wiki)

## Acknowledgments

Some functionalities are implemented with reference to the following projects:

### Lyrics Decryption

[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=WXRIW&repo=QQMusicDecoder)](https://github.com/WXRIW/QQMusicDecoder)
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=jixunmoe&repo=qmc-decode)](https://github.com/jixunmoe/qmc-decode)

### Music Platform APIs

[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=MCQTSS&repo=MCQTSS_QQMusic)](https://github.com/MCQTSS/MCQTSS_QQMusic)
