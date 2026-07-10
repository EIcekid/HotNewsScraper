// Global State
let currentRegion = 'JP';
let currentCategory = 'all';
let searchQuery = '';
let searchTimeout = null;

// DOM Elements
const regionTabs = document.getElementById('regionTabs');
const categoryNav = document.getElementById('categoryNav');
const searchInput = document.getElementById('searchInput');
const refreshBtn = document.getElementById('refreshBtn');
const refreshIcon = document.getElementById('refreshIcon');
const newsGrid = document.getElementById('newsGrid');
const emptyState = document.getElementById('emptyState');
const statusText = document.getElementById('statusText');
const themeToggle = document.getElementById('themeToggle');
const notificationContainer = document.getElementById('notificationContainer');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Theme setup
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme', savedTheme);
    
    // Bind Event Listeners
    setupEventListeners();
    
    // Fetch News
    loadNews();
});

// Event Listeners Binding
function setupEventListeners() {
    // Theme Toggle
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.body.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });

    // Region Switcher
    regionTabs.addEventListener('click', (e) => {
        const tab = e.target.closest('.region-tab');
        if (!tab || tab.classList.contains('active')) return;
        
        // Update UI
        document.querySelectorAll('.region-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // Update State & Fetch
        currentRegion = tab.getAttribute('data-region');
        loadNews();
    });

    // Category Switcher
    categoryNav.addEventListener('click', (e) => {
        const btn = e.target.closest('.category-btn');
        if (!btn || btn.classList.contains('active')) return;
        
        // Update UI
        document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Update State & Fetch
        currentCategory = btn.getAttribute('data-category');
        loadNews();
    });

    // Search Input (with Debounce)
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            searchQuery = e.target.value.trim();
            loadNews();
        }, 300);
    });

    // Manual Refresh
    refreshBtn.addEventListener('click', triggerScrape);
}

// Show notification popup
function showNotification(message, type = 'success') {
    const el = document.createElement('div');
    el.className = `notification ${type}`;
    el.innerHTML = `
        <span class="noti-icon">${type === 'success' ? '✅' : '❌'}</span>
        <span>${message}</span>
    `;
    notificationContainer.appendChild(el);
    
    // Remove after 4 seconds
    setTimeout(() => {
        el.style.animation = 'slideUp 0.3s reverse forwards';
        setTimeout(() => el.remove(), 300);
    }, 4000);
}

// Fetch and render news data
async function loadNews() {
    showSkeletons();
    emptyState.classList.add('hidden');
    
    try {
        let url = `/api/news?region=${currentRegion}&limit=60`;
        if (currentCategory !== 'all') {
            url += `&category=${currentCategory}`;
        }
        if (searchQuery) {
            url += `&search=${encodeURIComponent(searchQuery)}`;
        }
        
        const response = await fetch(url);
        if (!response.ok) throw new Error('网络响应失败，无法获取新闻数据');
        
        const resJson = await response.json();
        if (resJson.status === 'success') {
            renderNews(resJson.data);
        } else {
            throw new Error(resJson.detail || '拉取数据出错');
        }
    } catch (error) {
        console.error('Error fetching news:', error);
        newsGrid.innerHTML = '';
        emptyState.classList.remove('hidden');
        showNotification(error.message, 'error');
    }
}

// Show skeleton cards during loading state
function showSkeletons() {
    newsGrid.innerHTML = Array(6).fill(0).map(() => `<div class="skeleton-card"></div>`).join('');
}

// Render news items inside grid
function renderNews(items) {
    newsGrid.innerHTML = '';
    
    if (!items || items.length === 0) {
        emptyState.classList.remove('hidden');
        return;
    }
    
    // Category mapping for badge css class
    const categoryClasses = {
        'top': 'cat-top',
        'society': 'cat-society',
        'business': 'cat-business',
        'technology': 'cat-technology',
        'sports': 'cat-sports',
        'entertainment': 'cat-entertainment'
    };
    
    // Category display name
    const categoryNames = {
        'top': '要闻',
        'society': '社会/国际',
        'business': '财经',
        'technology': '科技',
        'sports': '体育',
        'entertainment': '娱乐'
    };

    items.forEach(item => {
        const card = document.createElement('a');
        card.className = 'news-card';
        card.href = item.url;
        card.target = '_blank';
        
        const badgeClass = categoryClasses[item.category] || 'cat-top';
        const badgeName = categoryNames[item.category] || item.category;
        
        // Format Time
        const pubDate = item.published_time ? new Date(item.published_time) : null;
        let timeString = '刚刚';
        if (pubDate && !isNaN(pubDate)) {
            timeString = pubDate.toLocaleString('zh-CN', {
                month: 'numeric',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
        
        card.innerHTML = `
            <div class="card-header">
                <span class="card-source">${item.source}</span>
                <span class="card-badge ${badgeClass}">${badgeName}</span>
            </div>
            <h3 class="card-title" title="${item.title}">${item.title}</h3>
            <p class="card-desc" title="${item.description || '点击查看全文'}">${item.description || '无摘要内容，点击查看详情原文。'}</p>
            <div class="card-footer">
                <span class="card-time">🕒 ${timeString}</span>
                <span class="read-more">阅读原文 &rarr;</span>
            </div>
        `;
        
        newsGrid.appendChild(card);
    });
}

// Trigger Backend Scrape Manually
async function triggerScrape() {
    if (refreshBtn.disabled) return;
    
    refreshBtn.disabled = true;
    refreshIcon.classList.add('spinning');
    statusText.innerText = '正在抓取日美最新热点...';
    
    try {
        const response = await fetch('/api/scrape', { method: 'POST' });
        if (!response.ok) throw new Error('手动刷新失败，服务器繁忙');
        
        const resJson = await response.json();
        if (resJson.status === 'success') {
            const count = resJson.inserted;
            showNotification(`刷新完成！抓取并更新了 ${count} 条新报道。`, 'success');
            loadNews();
        } else {
            throw new Error(resJson.detail || '抓取过程发生未知错误');
        }
    } catch (error) {
        console.error('Scraping failed:', error);
        showNotification(error.message, 'error');
    } finally {
        refreshBtn.disabled = false;
        refreshIcon.classList.remove('spinning');
        statusText.innerText = '每 30 分钟自动更新';
    }
}
