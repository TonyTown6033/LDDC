# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only
import asyncio
import time
from collections.abc import Iterable
from functools import reduce
from typing import Literal, overload

from LDDC.common.exceptions_fastapi import AutoFetchUnknownError, LDDCError, LyricsNotFoundError, NotEnoughInfoError
from LDDC.common.logger_fastapi import get_logger
from LDDC.common.models import APIResultList, Language, LyricInfo, Lyrics, LyricsType, SearchInfo, SearchType, SongInfo, Source
from LDDC.common.task_manager_fastapi import TaskManager
from LDDC.core.algorithm import calculate_artist_score, calculate_title_score, text_difference
from LDDC.core.api.lyrics import get_lyrics, search

logger = get_logger(__name__)


@overload
def auto_fetch(
    info: SongInfo,
    min_score: float = 60,
    sources: Iterable[Source] = (Source.QM, Source.KG, Source.NE),
    return_search_results: bool = False,
) -> Lyrics: ...


@overload
def auto_fetch(
    info: SongInfo,
    min_score: float = 60,
    sources: Iterable[Source] = (Source.QM, Source.KG, Source.NE),
    return_search_results: bool = True,
) -> tuple[Lyrics, APIResultList[SongInfo]]: ...


def auto_fetch(
    info: SongInfo,
    min_score: float = 55,
    sources: Iterable[Source] = (Source.QM, Source.KG, Source.NE),
    return_search_results: bool = False,
) -> Lyrics | tuple[Lyrics, APIResultList[SongInfo]]:
    """自动获取歌词（FastAPI版本，使用asyncio替代Qt事件循环）"""
    keywords: dict[Literal["artist-title", "title", "file_name"], str] = {}
    if info.title and info.title.strip():
        if info.artist:
            keywords["artist-title"] = info.artist_title()
        keywords["title"] = info.title
    elif info.path:
        keywords["file_name"] = info.path.stem
    else:
        msg = f"没有足够的信息用于搜索: {info}"
        raise NotEnoughInfoError(msg)

    search_results: dict[SongInfo, APIResultList[SongInfo]] = {}  # 每个源只保留一个
    songs_score: dict[SongInfo, float] = {}  # 歌曲匹配分数映射
    lyrics_results: dict[SongInfo, Lyrics] = {}  # 成功获取的歌词
    errors: list[Exception] = []  # 错误收集

    # 使用asyncio替代Qt事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    taskmanger = TaskManager(
        parent_childs={
            "search": [],
            "get_lyrics": [],
        },
    )

    def check_return() -> None:  # 检查是否所有任务都已完成
        if taskmanger.is_finished("search") and taskmanger.is_finished("get_lyrics"):
            # 停止事件循环
            for task in asyncio.all_tasks(loop):
                task.cancel()

    taskmanger.set_callback("search", check_return)
    taskmanger.set_callback("get_lyrics", check_return)

    def search_callback(results: APIResultList[SongInfo]) -> None:
        if not isinstance(results.info, SearchInfo):
            msg = "results.info is not SearchInfo"
            raise TypeError(msg)

        # 基于时长和元数据的分数计算
        result_score: list[tuple[float, SongInfo]] = []
        for result in results:
            if info.duration and abs((info.duration or -4) - (result.duration or -8)) > 4000:  # 忽略时长相差超过4秒的搜索结果
                continue
            if not info.duration:
                logger.warning("没有获取到 %s 的时长, 跳过时长匹配检查", info.artist_title())

            if results.info.keyword in (keywords.get("artist-title"), keywords.get("title")):  # results.info一定是SearchInfo
                # 根据 标题、艺术家、专辑 计算得分
                title_score = calculate_title_score(info.title or "", result.title or "")
                album_score = max(text_difference(info.album.lower(), result.album.lower()) * 100, 0) if info.album and result.album else None
                artist_score = calculate_artist_score(str(info.artist), str(result.artist)) if info.artist and result.artist else None

                if artist_score is not None:
                    if album_score is not None:
                        score = max(title_score * 0.5 + artist_score * 0.5, title_score * 0.5 + artist_score * 0.35 + album_score * 0.15)
                    else:
                        score = title_score * 0.5 + artist_score * 0.5
                elif album_score:
                    score = max(title_score * 0.7 + album_score * 0.3, title_score * 0.8)
                else:
                    score = title_score

                if title_score < 30:
                    score = max(0, score - 35)
            else:
                # 根据 文件名 计算得分
                score = max(
                    text_difference(keywords["file_name"], result.title or "") * 100,
                    text_difference(keywords["file_name"], f"{result.artist!s} - {result.title}") * 100,
                    text_difference(keywords["file_name"], f"{result.title} - {result.artist!s}") * 100,
                )

            if score > min_score:
                result_score.append((score, result))

        # 结果排序和处理
        result_score = sorted(result_score, key=lambda x: x[0], reverse=True)
        if result_score:

            def _get_lyrics(index: int) -> None:
                """递归获取歌词,失败时尝试下一个候选"""
                score, info = result_score[index]
                songs_score[info] = score
                search_results[info] = APIResultList(
                    [info, *[song_info for song_info in results if song_info != info]],
                    results.info,
                    ranges=results.source_ranges,
                )
                if index != 0:
                    search_results.pop(result_score[index - 1][1])

                taskmanger.new_multithreaded_task(
                    "get_lyrics",
                    get_lyrics,
                    lambda lyrics: lyrics_results.__setitem__(result_score[index][1], lyrics),
                    lambda e: _get_lyrics(index + 1)
                    if isinstance(e, LyricsNotFoundError) and 0 <= index < 2 and len(result_score) > 1 + index  # 最多尝试获取两个结果
                    else errors.append(e),
                    info,
                )

            _get_lyrics(0)
        elif results.info.keyword == keywords.get("artist-title") and (keyword := keywords.get("title")):
            _search(results.info.source, keyword)

    def _search(sources: Source | Iterable[Source], keyword: str) -> None:
        for source in sources if isinstance(sources, Iterable) else (sources,):
            taskmanger.new_multithreaded_task(
                "search",
                search,
                search_callback,
                lambda e: errors.append(e),
                source,
                keyword,
                SearchType.SONG,
            )

    _search(sources, keywords.get("artist-title") or keywords.get("title") or keywords["file_name"])

    # 使用asyncio替代QTimer进行超时处理
    start_time = time.time()
    timeout_seconds = 30
    
    async def wait_for_completion():
        """等待任务完成或超时"""
        while True:
            if taskmanger.is_finished("search") and taskmanger.is_finished("get_lyrics"):
                break
            if time.time() - start_time > timeout_seconds:
                # 超时处理
                taskmanger.clear_task("search")
                taskmanger.clear_task("get_lyrics")
                raise TimeoutError("自动获取超时")
            await asyncio.sleep(0.1)  # 短暂等待

    try:
        loop.run_until_complete(wait_for_completion())
    except TimeoutError:
        raise
    finally:
        loop.close()

    if not lyrics_results:
        if songs_score:
            # 处理纯音乐
            sorted_songs_score = [info for info, score in sorted(songs_score.items(), key=lambda x: x[1], reverse=True) if info.language is not None]
            if sorted_songs_score and sorted_songs_score[0].language == Language.INSTRUMENTAL:
                inst_info = sorted_songs_score[0]
                inst_lyrics = Lyrics.get_inst_lyrics(LyricInfo(inst_info.source, inst_info))
                lyrics_results[sorted_songs_score[0]] = inst_lyrics
        if not lyrics_results:
            if not [error for error in errors if not isinstance(error, LyricsNotFoundError)]:
                msg = "没有找到符合要求的歌曲"
                raise LyricsNotFoundError(msg)
            from httpx import HTTPError

            if not [error for error in errors if not isinstance(error, ConnectionError | HTTPError)]:
                errors_str = "\n".join(f"{e.__class__.__name__}: {e!s}" for e in errors)
                msg = f"网络错误: {errors_str}"
                raise LDDCError(msg)
            msg = "自动获取时发生未知错误"
            raise AutoFetchUnknownError(msg, errors)

    # 筛选最高分结果(允许15分误差)
    highest_score = max(songs_score[song_info] for song_info, _ in lyrics_results.items())
    lyrics_results = {song_info: lyrics for song_info, lyrics in lyrics_results.items() if abs(songs_score[song_info] - highest_score) <= 15}

    # 获取最高优先级的歌词类型
    have_verbatim = [lyrics for _, lyrics in lyrics_results.items() if lyrics.types.get("orig") == LyricsType.VERBATIM]
    have_ts = [lyrics for _, lyrics in lyrics_results.items() if "ts" in lyrics]
    have_roma = [lyrics for _, lyrics in lyrics_results.items() if "roma" in lyrics]

    have_verbatim_ts: list[Lyrics] = []
    have_verbatim_roma: list[Lyrics] = []
    have_verbatim_ts_roma: list[Lyrics] = []
    have_ts_roma: list[Lyrics] = []
    for lyrics in lyrics_results.values():
        if lyrics in have_verbatim and lyrics in have_ts:
            have_verbatim_ts.append(lyrics)
        if lyrics in have_verbatim and lyrics in have_roma:
            have_verbatim_roma.append(lyrics)
        if lyrics in have_verbatim and lyrics in have_ts and lyrics in have_roma:
            have_verbatim_ts_roma.append(lyrics)
        if lyrics in have_ts and lyrics in have_roma:
            have_ts_roma.append(lyrics)

    for lyrics_list in [have_verbatim_ts_roma, have_verbatim_ts, have_ts_roma, have_ts, have_verbatim_roma, have_verbatim, have_roma]:
        if lyrics_list:
            break
    else:
        lyrics_list = list(lyrics_results.values())

    # 按源优先级返回结果
    for source in sources:
        for lyrics in lyrics_list:
            if lyrics.info.source == source:
                if not return_search_results:
                    return lyrics
                info = next(song_info for song_info, lyrics_ in lyrics_results.items() if lyrics_ == lyrics)

                return (
                    lyrics
                    if not return_search_results
                    else (
                        lyrics,
                        (
                            (search_results[info] + reduce(lambda a, b: a + b, other_search_results))
                            if (other_search_results := [result for song_info, result in search_results.items() if song_info != info])
                            else search_results[info]
                        ),
                    )
                )

        continue
    msg = "自动获取时发生未知错误"
    raise AutoFetchUnknownError(msg, errors)