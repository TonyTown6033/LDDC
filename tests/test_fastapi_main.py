# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only

"""LDDC.api.main 的 FastAPI 端点全面测试"""

import time
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from LDDC.api import main as api_main


class TestMainAPIEndpoints:
    """主应用端点测试"""

    @pytest.fixture
    def client(self):
        return TestClient(api_main.app)

    # 基本端点
    def test_root_ok(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert "text/html" in resp.headers.get("content-type", "")

    def test_health_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("status") == "ok"

    # 搜索（POST /api/search）
    @patch("LDDC.api.main.search")
    def test_post_search_success(self, mock_search, client):
        m = MagicMock()
        m.id = "id1"
        m.title = "晴天"
        m.artist = "周杰伦"
        m.album = "叶惠美"
        m.duration = 269
        m.source = api_main.Source.QM
        mock_search.return_value = [m]

        resp = client.post("/api/search", json={
            "keyword": "周杰伦 晴天",
            "source": "QM",
            "search_type": "SONG",
            "page": 1,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "results" in data and "total" in data
        assert data["total"] == 1
        assert data["results"][0]["title"] == "晴天"
        assert data["results"][0]["artist"] == "周杰伦"

    def test_post_search_invalid_source(self, client):
        resp = client.post("/api/search", json={
            "keyword": "x",
            "source": "INVALID",
            "search_type": "SONG",
            "page": 1,
        })
        assert resp.status_code == 400

    def test_post_search_invalid_type(self, client):
        resp = client.post("/api/search", json={
            "keyword": "x",
            "source": "QM",
            "search_type": "BADTYPE",
            "page": 1,
        })
        assert resp.status_code == 400

    def test_post_search_bad_request(self, client):
        # page 传字符串触发 422
        resp = client.post("/api/search", json={
            "keyword": "x",
            "source": "QM",
            "search_type": "SONG",
            "page": "one",
        })
        assert resp.status_code == 422

    @patch("LDDC.api.main.search")
    def test_post_search_permission_error(self, mock_search, client):
        # 模拟权限错误（如底层服务需要授权）
        mock_search.side_effect = Exception("权限错误: 未授权")
        resp = client.post("/api/search", json={
            "keyword": "x",
            "source": "QM",
            "search_type": "SONG",
            "page": 1,
        })
        assert resp.status_code == 500
        assert "搜索失败" in resp.json().get("detail", "")

    # 搜索（GET /api/search 简化）
    @patch("LDDC.api.main.search")
    def test_get_search_success(self, mock_search, client):
        mock_search.return_value = []
        resp = client.get("/api/search", params={
            "keyword": "a",
            "source": "QM",
            "search_type": "SONG",
            "page": 1,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0

    def test_get_search_missing_keyword(self, client):
        resp = client.get("/api/search", params={
            "source": "QM",
            "search_type": "SONG",
        })
        assert resp.status_code == 422

    @patch("LDDC.api.main.search")
    def test_get_search_boundary_cases(self, mock_search, client):
        mock_search.return_value = []
        # 空关键字（允许空字符串）
        resp1 = client.get("/api/search", params={
            "keyword": "",
            "source": "QM",
            "search_type": "SONG",
            "page": 1,
        })
        assert resp1.status_code == 200
        # 负页码（未限制，但应稳定返回）
        resp2 = client.get("/api/search", params={
            "keyword": "a",
            "source": "QM",
            "search_type": "SONG",
            "page": -1,
        })
        assert resp2.status_code == 200

    # 别名路由：GET /search_simple
    @patch("LDDC.api.main.search")
    def test_get_search_simple_alias_ok(self, mock_search, client):
        mock_search.return_value = []
        resp = client.get("/search_simple", params={
            "keyword": "a",
            "source": "QM",
            "search_type": "SONG",
            "page": 1,
        })
        assert resp.status_code == 200

    def test_get_search_simple_alias_missing_keyword(self, client):
        resp = client.get("/search_simple", params={
            "source": "QM",
            "search_type": "SONG",
        })
        assert resp.status_code == 422

    # 歌词（POST /api/lyrics）
    @patch("LDDC.api.main.get_lyrics")
    @patch("LDDC.api.main.lrc_converter")
    def test_post_lyrics_success(self, mock_lrc, mock_get_lyrics, client):
        mock_get_lyrics.return_value = MagicMock(tags={})
        mock_lrc.return_value = "[00:00.00]测试歌词"
        resp = client.post("/api/lyrics", json={
            "song_id": "id1",
            "title": "晴天",
            "artist": "周杰伦",
            "album": "叶惠美",
            "duration": 269,
            "source": "QM",
        })
        assert resp.status_code == 200
        assert "测试歌词" in resp.text

    def test_post_lyrics_invalid_source(self, client):
        resp = client.post("/api/lyrics", json={
            "song_id": "id1",
            "title": "晴天",
            "artist": "周杰伦",
            "album": "叶惠美",
            "duration": 269,
            "source": "BAD",
        })
        assert resp.status_code == 400

    @patch("LDDC.api.main.get_lyrics")
    def test_post_lyrics_not_found(self, mock_get_lyrics, client):
        mock_get_lyrics.return_value = None
        resp = client.post("/api/lyrics", json={
            "song_id": "id1",
            "title": "晴天",
            "artist": "周杰伦",
            "album": "叶惠美",
            "duration": 269,
            "source": "QM",
        })
        assert resp.status_code == 404

    @patch("LDDC.api.main.get_lyrics")
    @patch("LDDC.api.main.lrc_converter")
    def test_post_lyrics_convert_fail(self, mock_lrc, mock_get_lyrics, client):
        mock_get_lyrics.return_value = MagicMock(tags={})
        mock_lrc.return_value = ""
        resp = client.post("/api/lyrics", json={
            "song_id": "id1",
            "title": "晴天",
            "artist": "周杰伦",
            "album": "叶惠美",
            "duration": 269,
            "source": "QM",
        })
        assert resp.status_code == 404

    def test_get_lyrics_missing_params(self, client):
        resp = client.get("/api/lyrics", params={
            "title": "晴天",
            "artist": "周杰伦",
        })
        assert resp.status_code == 422

    # 别名路由：GET /lyrics_simple
    @patch("LDDC.api.main.get_lyrics")
    @patch("LDDC.api.main.lrc_converter")
    def test_get_lyrics_simple_alias_ok(self, mock_lrc, mock_get_lyrics, client):
        mock_get_lyrics.return_value = MagicMock(tags={})
        mock_lrc.return_value = "[00:00.00]测试歌词"
        resp = client.get("/lyrics_simple", params={
            "song_id": "id1",
            "title": "晴天",
            "artist": "周杰伦",
            "album": "叶惠美",
            "source": "QM",
        })
        assert resp.status_code == 200
        assert "测试歌词" in resp.text

    @patch("LDDC.api.main.get_lyrics")
    def test_get_lyrics_simple_alias_not_found(self, mock_get_lyrics, client):
        mock_get_lyrics.return_value = None
        resp = client.get("/lyrics_simple", params={
            "song_id": "id1",
            "title": "晴天",
            "artist": "周杰伦",
            "source": "QM",
        })
        assert resp.status_code == 404

    @patch("LDDC.api.main.get_lyrics")
    def test_post_lyrics_permission_error(self, mock_get_lyrics, client):
        mock_get_lyrics.side_effect = Exception("权限错误: 未授权")
        resp = client.post("/api/lyrics", json={
            "song_id": "id1",
            "title": "晴天",
            "artist": "周杰伦",
            "album": "叶惠美",
            "duration": 269,
            "source": "QM",
        })
        assert resp.status_code == 500
        assert "下载歌词失败" in resp.json().get("detail", "")

    # 静态资源（若存在）
    def test_static_css_js(self, client):
        r1 = client.get("/static/style.css")
        r2 = client.get("/static/script.js")
        assert r1.status_code in (200, 404)  # 根据是否挂载静态目录
        assert r2.status_code in (200, 404)


class TestMainAPIPerformance:
    """性能基准测试（响应时间）"""

    @pytest.fixture
    def client(self):
        return TestClient(api_main.app)

    @patch("LDDC.api.main.search")
    def test_search_simple_latency(self, mock_search, client):
        mock_search.return_value = []
        start = time.perf_counter()
        resp = client.get("/api/search", params={
            "keyword": "a",
            "source": "QM",
            "search_type": "SONG",
            "page": 1,
        })
        elapsed = (time.perf_counter() - start) * 1000
        assert resp.status_code == 200
        assert elapsed < 500  # 500ms内

    def test_health_latency(self, client):
        start = time.perf_counter()
        resp = client.get("/health")
        elapsed = (time.perf_counter() - start) * 1000
        assert resp.status_code == 200
        assert elapsed < 200  # 200ms内

    @patch("LDDC.api.main.get_lyrics")
    @patch("LDDC.api.main.lrc_converter")
    def test_lyrics_latency(self, mock_lrc, mock_get_lyrics, client):
        mock_get_lyrics.return_value = MagicMock(tags={})
        mock_lrc.return_value = "[00:00.00]测试歌词"
        start = time.perf_counter()
        resp = client.post("/api/lyrics", json={
            "song_id": "id1",
            "title": "晴天",
            "artist": "周杰伦",
            "album": "叶惠美",
            "duration": 269,
            "source": "QM",
        })
        elapsed = (time.perf_counter() - start) * 1000
        assert resp.status_code == 200
        assert elapsed < 700  # 700ms内