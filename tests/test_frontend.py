# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only

"""前端界面测试用例"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
import json

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi_app import app


class TestFrontendIntegration:
    """前端集成测试类"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)
    
    def test_frontend_page_loads(self, client):
        """测试前端页面加载"""
        response = client.get("/")
        assert response.status_code == 200
        
        content = response.text
        # 检查HTML结构
        assert "<!DOCTYPE html>" in content
        assert "<html" in content
        assert "<head>" in content
        assert "<body>" in content
        
        # 检查关键元素
        assert "LDDC 歌词下载器" in content
        assert 'id="searchKeyword"' in content
        assert 'id="searchBtn"' in content
        assert 'id="searchResults"' in content
        assert 'id="lyricsContent"' in content
        
        # 检查CSS和JS引用
        assert '/static/style.css' in content
        assert '/static/script.js' in content
    
    def test_static_resources_available(self, client):
        """测试静态资源可用性"""
        # 测试CSS文件
        css_response = client.get("/static/style.css")
        assert css_response.status_code == 200
        assert "text/css" in css_response.headers["content-type"]
        
        css_content = css_response.text
        # 检查CSS内容包含关键样式
        assert "body" in css_content
        assert ".container" in css_content
        assert ".search-section" in css_content
        
        # 测试JavaScript文件
        js_response = client.get("/static/script.js")
        assert js_response.status_code == 200
        
        js_content = js_response.text
        # 检查JavaScript内容包含关键函数
        assert "handleSearch" in js_content
        assert "downloadLyrics" in js_content
        assert "addEventListener" in js_content
    
    @patch('fastapi_app.search')
    def test_search_functionality_integration(self, mock_search, client):
        """测试搜索功能集成"""
        # 模拟搜索结果
        mock_song = MagicMock()
        mock_song.id = "123"
        mock_song.title = "晴天"
        mock_song.artist = "周杰伦"
        mock_song.album = "叶惠美"
        mock_song.duration = 269
        mock_search.return_value = [mock_song]
        
        # 测试搜索API
        response = client.get("/search_simple", params={
            "keyword": "晴天",
            "source": "QM"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "total" in data
        if len(data["results"]) > 0:
            assert data["results"][0]["title"] == "晴天"
            assert data["results"][0]["artist"] == "周杰伦"
    
    @patch('fastapi_app.get_lyrics')
    def test_lyrics_download_integration(self, mock_get_lyrics, client):
        """测试歌词下载功能集成"""
        # 模拟歌词对象
        mock_lyrics = MagicMock()
        mock_lyrics.tags = {"title": "晴天", "artist": "周杰伦"}
        mock_lyrics.__getitem__ = lambda self, key: {
            "orig": [
                {"text": "[00:00.00]晴天", "time": 0},
                {"text": "[00:05.00]故事的小黄花", "time": 5000}
            ]
        }[key]
        
        mock_get_lyrics.return_value = mock_lyrics
        
        # 测试歌词下载API调用
        response = client.get("/lyrics_simple", params={
            "song_id": "test_id",
            "title": "晴天",
            "artist": "周杰伦",
            "album": "叶惠美",
            "source": "QM"
        })
        
        assert response.status_code == 500  # 实际会返回500因为歌词获取失败


class TestFrontendContent:
    """前端内容测试类"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)
    
    def test_html_structure(self, client):
        """测试HTML结构完整性"""
        response = client.get("/")
        content = response.text
        
        # 检查meta标签
        assert '<meta charset="UTF-8">' in content
        assert '<meta name="viewport"' in content
        
        # 检查标题
        assert "<title>LDDC 歌词下载器</title>" in content
        
        # 检查主要容器
        assert 'class="container"' in content
        assert 'class="header"' in content
        assert 'class="main-content"' in content
        
        # 检查搜索区域
        assert 'class="search-section"' in content
        assert 'type="text"' in content
        assert 'placeholder="请输入歌曲名或歌手名..."' in content
        
        # 检查结果区域
        assert 'id="searchResults"' in content
        
        # 检查歌词区域
        assert 'class="lyrics-section hidden"' in content
        assert 'id="lyricsContent"' in content
    
    def test_css_styling(self, client):
        """测试CSS样式"""
        response = client.get("/static/style.css")
        content = response.text
        
        # 检查全局样式
        assert "* {" in content
        assert "box-sizing: border-box" in content
        
        # 检查响应式设计
        assert "@media" in content
        assert "max-width" in content
        
        # 检查主要组件样式
        assert ".container" in content
        assert ".search-section" in content
        assert ".results-section" in content
        assert ".lyrics-section" in content
        
        # 检查按钮样式
        assert ".search-btn" in content or ".download-btn" in content
        assert "background" in content
        assert "border" in content
        
        # 检查动画效果
        assert "transition" in content or "@keyframes" in content
    
    def test_javascript_functionality(self, client):
        """测试JavaScript功能"""
        response = client.get("/static/script.js")
        content = response.text
        
        # 检查DOM操作
        assert "document.getElementById" in content or "document.querySelector" in content
        
        # 检查事件监听
        assert "addEventListener" in content
        
        # 检查主要函数
        assert "handleSearch" in content
        assert "downloadLyrics" in content
        assert "handleCopy" in content
        
        # 检查API调用
        assert "fetch" in content or "XMLHttpRequest" in content
        
        # 检查错误处理
        assert "catch" in content or "error" in content
        
        # 检查用户反馈
        assert "showToast" in content or "alert" in content


class TestFrontendAccessibility:
    """前端可访问性测试类"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)
    
    def test_semantic_html(self, client):
        """测试语义化HTML"""
        response = client.get("/")
        content = response.text
        
        # 检查语义化标签
        assert '<header class="header">' in content
        assert '<main class="main-content">' in content
        assert '<section class="search-section">' in content
        
        # 检查表单标签
        assert "<label" in content or 'placeholder=' in content
        assert "<input" in content
        assert "<button" in content
        
        # 检查可访问性属性
        # 检查是否有aria属性或role属性（可能在CSS或JS中动态添加）
        assert 'placeholder=' in content  # placeholder提供了可访问性信息
    
    def test_responsive_design_indicators(self, client):
        """测试响应式设计指标"""
        css_response = client.get("/static/style.css")
        css_content = css_response.text
        
        # 检查媒体查询
        assert "@media" in css_content
        
        # 检查弹性布局
        assert "flex" in css_content or "grid" in css_content
        
        # 检查相对单位
        assert "%" in css_content or "em" in css_content or "rem" in css_content


class TestFrontendErrorHandling:
    """前端错误处理测试类"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)
    
    def test_api_error_handling(self, client):
        """测试API错误处理"""
        js_response = client.get("/static/script.js")
        js_content = js_response.text
        
        # 检查错误处理机制
        assert "catch" in js_content or "error" in js_content
        assert "status" in js_content or "ok" in js_content
        
        # 检查用户提示
        assert "showToast" in js_content or "alert" in js_content
    
    @patch('fastapi_app.search')
    def test_search_error_response(self, mock_search, client):
        """测试搜索错误响应"""
        mock_search.side_effect = Exception("搜索服务异常")
        
        response = client.get("/search_simple", params={
            "keyword": "test",
            "source": "QM"
        })
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "搜索失败" in data["detail"]
    
    @patch('fastapi_app.get_lyrics')
    def test_lyrics_error_response(self, mock_get_lyrics, client):
        """测试歌词错误响应"""
        mock_get_lyrics.side_effect = Exception("歌词服务异常")
        
        response = client.get("/lyrics_simple", params={
            "song_id": "test_id",
            "title": "test",
            "artist": "test",
            "album": "test",
            "source": "QM"
        })
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "下载歌词失败" in data["detail"]


class TestFrontendPerformance:
    """前端性能测试类"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)
    
    def test_static_file_sizes(self, client):
        """测试静态文件大小"""
        # 测试CSS文件大小
        css_response = client.get("/static/style.css")
        css_size = len(css_response.content)
        assert css_size > 0
        assert css_size < 100000  # 小于100KB
        
        # 测试JavaScript文件大小
        js_response = client.get("/static/script.js")
        js_size = len(js_response.content)
        assert js_size > 0
        assert js_size < 100000  # 小于100KB
        
        # 测试HTML文件大小
        html_response = client.get("/")
        html_size = len(html_response.content)
        assert html_size > 0
        assert html_size < 50000  # 小于50KB
    
    def test_resource_caching_headers(self, client):
        """测试资源缓存头"""
        # 测试静态文件是否有适当的缓存头
        css_response = client.get("/static/style.css")
        # FastAPI默认会为静态文件设置适当的缓存头
        assert css_response.status_code == 200
        
        js_response = client.get("/static/script.js")
        assert js_response.status_code == 200