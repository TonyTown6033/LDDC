// 全局变量
let currentLyrics = '';
let currentSongInfo = {};

// DOM 元素
const searchKeyword = document.getElementById('searchKeyword');
const searchSource = document.getElementById('searchSource');
const searchBtn = document.getElementById('searchBtn');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const searchResults = document.getElementById('searchResults');
const lyricsSection = document.getElementById('lyricsSection');
const lyricsTitle = document.getElementById('lyricsTitle');
const lyricsArtist = document.getElementById('lyricsArtist');
const lyricsContent = document.getElementById('lyricsContent');
const downloadBtn = document.getElementById('downloadBtn');
const copyBtn = document.getElementById('copyBtn');
const toast = document.getElementById('toast');

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    // 绑定事件
    searchBtn.addEventListener('click', handleSearch);
    searchKeyword.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
    downloadBtn.addEventListener('click', handleDownload);
    copyBtn.addEventListener('click', handleCopy);
});

// 显示提示消息
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove('hidden');
    
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

// 显示加载状态
function showLoading(show = true) {
    if (show) {
        loading.classList.remove('hidden');
        resultsSection.classList.add('hidden');
        lyricsSection.classList.add('hidden');
    } else {
        loading.classList.add('hidden');
    }
}

// 处理搜索
async function handleSearch() {
    const keyword = searchKeyword.value.trim();
    if (!keyword) {
        showToast('请输入搜索关键词', 'warning');
        return;
    }

    showLoading(true);
    
    try {
        const response = await fetch('/search_simple?' + new URLSearchParams({
            keyword: keyword,
            source: searchSource.value
        }));
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        displaySearchResults(data.results || []);
        showToast(`找到 ${data.total || 0} 首歌曲`);
        
    } catch (error) {
        console.error('搜索失败:', error);
        showToast('搜索失败，请稍后重试', 'error');
    } finally {
        showLoading(false);
    }
}

// 显示搜索结果
function displaySearchResults(results) {
    searchResults.innerHTML = '';
    
    if (results.length === 0) {
        searchResults.innerHTML = '<p class="no-results">未找到相关歌曲，请尝试其他关键词</p>';
        resultsSection.classList.remove('hidden');
        return;
    }
    
    results.forEach(song => {
        const resultItem = document.createElement('div');
        resultItem.className = 'result-item';
        resultItem.innerHTML = `
            <div class="result-title">${escapeHtml(song.title || '未知标题')}</div>
            <div class="result-artist"><i class="fas fa-user"></i> ${escapeHtml(song.artist || '未知歌手')}</div>
            <div class="result-album"><i class="fas fa-compact-disc"></i> ${escapeHtml(song.album || '未知专辑')}</div>
            <div class="result-duration"><i class="fas fa-clock"></i> ${formatDuration(song.duration || 0)}</div>
        `;
        
        resultItem.addEventListener('click', () => {
            downloadLyrics(song);
        });
        
        searchResults.appendChild(resultItem);
    });
    
    resultsSection.classList.remove('hidden');
}

// 下载歌词
async function downloadLyrics(song) {
    showLoading(true);
    
    try {
        const response = await fetch('/lyrics_simple?' + new URLSearchParams({
            song_id: song.id || '',
            title: song.title || '',
            artist: song.artist || '',
            album: song.album || '',
            source: song.source || searchSource.value
        }));
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const lyrics = await response.text();
        displayLyrics(song, lyrics);
        showToast('歌词获取成功！');
        
    } catch (error) {
        console.error('获取歌词失败:', error);
        showToast('获取歌词失败，请稍后重试', 'error');
    } finally {
        showLoading(false);
    }
}

// 显示歌词
function displayLyrics(song, lyrics) {
    currentLyrics = lyrics;
    currentSongInfo = song;
    
    lyricsTitle.textContent = song.title || '未知标题';
    lyricsArtist.textContent = song.artist || '未知歌手';
    lyricsContent.textContent = lyrics || '暂无歌词';
    
    lyricsSection.classList.remove('hidden');
    
    // 滚动到歌词区域
    lyricsSection.scrollIntoView({ behavior: 'smooth' });
}

// 处理下载
function handleDownload() {
    if (!currentLyrics) {
        showToast('没有可下载的歌词', 'warning');
        return;
    }
    
    const filename = `${currentSongInfo.artist || '未知歌手'} - ${currentSongInfo.title || '未知标题'}.lrc`;
    const blob = new Blob([currentLyrics], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showToast('歌词文件下载成功！');
}

// 处理复制
async function handleCopy() {
    if (!currentLyrics) {
        showToast('没有可复制的歌词', 'warning');
        return;
    }
    
    try {
        await navigator.clipboard.writeText(currentLyrics);
        showToast('歌词已复制到剪贴板！');
    } catch (error) {
        // 降级方案
        const textArea = document.createElement('textarea');
        textArea.value = currentLyrics;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showToast('歌词已复制到剪贴板！');
    }
}

// 工具函数
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDuration(duration) {
    if (!duration || duration === 0) return '未知时长';
    
    const minutes = Math.floor(duration / 60000);
    const seconds = Math.floor((duration % 60000) / 1000);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

// 添加一些交互效果
document.addEventListener('DOMContentLoaded', function() {
    // 搜索框焦点效果
    searchKeyword.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
    });
    
    searchKeyword.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
    
    // 按钮点击效果
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('mousedown', function() {
            this.style.transform = 'scale(0.95)';
        });
        
        button.addEventListener('mouseup', function() {
            this.style.transform = 'scale(1)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
});