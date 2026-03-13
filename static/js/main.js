let abortController = null;
let progressInterval = null;

class CacheManager {
    constructor(prefix = 'fortune_') {
        this.prefix = prefix;
    }
    
    generateKey(data) {
        const keyStr = `${data.birth_date}_${data.birth_time}_${data.gender}_${data.question_type}`;
        return this.prefix + btoa(unescape(encodeURIComponent(keyStr)));
    }
    
    set(data, result, ttl = 3600000) {
        const key = this.generateKey(data);
        const cacheData = {
            result: result,
            timestamp: Date.now(),
            ttl: ttl
        };
        try {
            localStorage.setItem(key, JSON.stringify(cacheData));
        } catch (e) {
            console.warn('缓存保存失败:', e);
        }
    }
    
    get(data) {
        const key = this.generateKey(data);
        const cached = localStorage.getItem(key);
        
        if (!cached) return null;
        
        try {
            const cacheData = JSON.parse(cached);
            
            if (Date.now() - cacheData.timestamp > cacheData.ttl) {
                localStorage.removeItem(key);
                return null;
            }
            
            return cacheData.result;
        } catch (e) {
            console.warn('缓存读取失败:', e);
            return null;
        }
    }
    
    clear() {
        Object.keys(localStorage)
            .filter(key => key.startsWith(this.prefix))
            .forEach(key => localStorage.removeItem(key));
    }
}

const cache = new CacheManager();

function validateInput(birthDate, birthTime) {
    const errors = [];
    
    const date = new Date(birthDate);
    const todayDate = new Date();
    todayDate.setHours(0, 0, 0, 0);
    
    if (date > todayDate) {
        errors.push({field: 'birthDate', message: '出生日期不能晚于今天'});
    }
    
    const minDate = new Date('1900-01-01');
    if (date < minDate) {
        errors.push({field: 'birthDate', message: '出生日期不能早于1900年'});
    }
    
    if (!birthTime) {
        errors.push({field: 'birthTime', message: '请选择出生时间'});
    }
    
    return errors;
}

function showError(fieldId, message) {
    const errorDiv = document.getElementById(fieldId + 'Error');
    const input = document.getElementById(fieldId);
    if (errorDiv && input) {
        errorDiv.textContent = message;
        errorDiv.classList.add('show');
        input.classList.add('error');
    }
}

function clearErrors() {
    document.querySelectorAll('.error-hint').forEach(el => {
        el.classList.remove('show');
        el.textContent = '';
    });
    document.querySelectorAll('.error').forEach(el => {
        el.classList.remove('error');
    });
}

function simulateProgress() {
    let progress = 0;
    const progressBar = document.querySelector('.progress');
    
    progressInterval = setInterval(() => {
        progress += Math.random() * 8;
        if (progress > 90) progress = 90;
        progressBar.style.width = progress + '%';
    }, 1000);
    
    return progressInterval;
}

function stopProgress() {
    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }
    const progressBar = document.querySelector('.progress');
    if (progressBar) {
        progressBar.style.width = '100%';
    }
}

function cancelRequest() {
    if (abortController) {
        abortController.abort();
        abortController = null;
    }
    stopProgress();
    
    enableInputs();
    
    const btn = document.getElementById('calculateBtn');
    btn.disabled = false;
    btn.textContent = '开始算命';
    
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '<div style="color: #888; text-align: center; padding: 20px;">请求已取消</div>';
}

function disableInputs() {
    const inputs = document.querySelectorAll('#birthDate, #birthTime, #gender, #questionType');
    inputs.forEach(input => {
        input.disabled = true;
        input.style.opacity = '0.5';
        input.style.cursor = 'not-allowed';
    });
}

function enableInputs() {
    const inputs = document.querySelectorAll('#birthDate, #birthTime, #gender, #questionType');
    inputs.forEach(input => {
        input.disabled = false;
        input.style.opacity = '1';
        input.style.cursor = 'auto';
    });
}

async function calculate() {
    clearErrors();
    
    const birthDate = document.getElementById('birthDate').value;
    const birthTime = document.getElementById('birthTime').value;
    const gender = document.getElementById('gender').value;
    const questionType = document.getElementById('questionType').value;
    
    const errors = validateInput(birthDate, birthTime);
    if (errors.length > 0) {
        errors.forEach(error => {
            showError(error.field, error.message);
        });
        return;
    }
    
    const inputData = {
        birth_date: birthDate,
        birth_time: birthTime,
        gender: gender,
        question_type: questionType
    };
    
    const cachedResult = cache.get(inputData);
    if (cachedResult) {
        showNotification('使用缓存结果', 'success');
        renderResult(cachedResult, questionType);
        return;
    }
    
    const btn = document.getElementById('calculateBtn');
    btn.disabled = true;
    btn.textContent = '算命中...';
    
    disableInputs();
    
    const resultDiv = document.getElementById('result');
    resultDiv.classList.remove('show');
    resultDiv.innerHTML = `
        <div class="loading-container">
            <div class="progress-bar">
                <div class="progress"></div>
            </div>
            <div class="loading-text">正在分析八字</div>
            <div class="estimated-time">预计需要 15-30 秒</div>
            <button class="btn btn-cancel" onclick="cancelRequest()">取消请求</button>
        </div>
    `;
    resultDiv.classList.add('show');
    
    simulateProgress();
    
    abortController = new AbortController();
    
    try {
        const response = await fetchWithRetry('/api/fortune', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(inputData),
            signal: abortController.signal
        }, 2);
        
        const data = await response.json();
        
        stopProgress();
        
        if (data.success) {
            cache.set(inputData, data);
            renderResult(data, questionType);
        } else {
            showErrorCard('api_error', data.error);
        }
    } catch (error) {
        stopProgress();
        
        if (error.name === 'AbortError') {
            resultDiv.innerHTML = '<div style="color: #888; text-align: center; padding: 20px;">请求已取消</div>';
        } else if (error.message && error.message.includes('HTTP')) {
            showErrorCard('server', '服务器响应异常: ' + error.message);
        } else if (!navigator.onLine) {
            showErrorCard('network');
        } else {
            showErrorCard('network', error.message);
        }
    } finally {
        abortController = null;
        btn.disabled = false;
        btn.textContent = '开始算命';
        enableInputs();
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function parseMarkdown(markdown) {
    if (!markdown) return '';
    
    let html = markdown;
    
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    
    html = html.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    html = html.replace(/!\[([^\]]*)\]\(([^\)]*)\)/g, '<img src="$2" alt="$1">');
    html = html.replace(/\[([^\]]*)\]\(([^\)]*)\)/g, '<a href="$2" target="_blank">$1</a>');
    
    html = html.replace(/^[\s]*[-\*+][\s]+(.*)$/gim, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    
    html = html.replace(/^[\s]*\d+\.[\s]+(.*)$/gim, '<li>$1</li>');
    
    html = html.replace(/`{3}[\s\S]*?`{3}/g, function(match) {
        const code = match.replace(/`{3}/g, '').trim();
        return '<pre><code>' + escapeHtml(code) + '</code></pre>';
    });
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    html = html.replace(/\n\n/g, '</p><p>');
    html = html.replace(/\n/g, '<br>');
    
    html = '<p>' + html + '</p>';
    
    html = html.replace(/<p><\/p>/g, '');
    html = html.replace(/<p>(<h[1-6]>)/g, '$1');
    html = html.replace(/(<\/h[1-6]>)<\/p>/g, '$1');
    html = html.replace(/<p>(<ul>)/g, '$1');
    html = html.replace(/(<\/ul>)<\/p>/g, '$1');
    html = html.replace(/<p>(<pre>)/g, '$1');
    html = html.replace(/(<\/pre>)<\/p>/g, '$1');
    
    return html;
}

const errorMessages = {
    'network': '网络连接失败，请检查网络后重试',
    'timeout': '请求超时，请稍后重试',
    'server': '服务器繁忙，请稍后重试',
    'invalid_input': '输入信息有误，请检查后重试',
    'api_error': '算命服务暂时不可用，请稍后重试'
};

function showErrorCard(errorType, errorMessage) {
    const message = errorMessages[errorType] || errorMessage || '未知错误，请刷新页面重试';
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `
        <div class="error-card">
            <div class="error-icon">⚠️</div>
            <div class="error-message">${escapeHtml(message)}</div>
            <button class="btn-retry" onclick="retryCalculate()">重新算命</button>
        </div>
    `;
}

function retryCalculate() {
    calculate();
}

async function fetchWithRetry(url, options, maxRetries = 3) {
    let lastError;
    
    for (let i = 0; i < maxRetries; i++) {
        try {
            const response = await fetch(url, options);
            if (response.ok) {
                return response;
            }
            throw new Error(`HTTP ${response.status}`);
        } catch (error) {
            lastError = error;
            if (i < maxRetries - 1) {
                await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
            }
        }
    }
    
    throw lastError;
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

window.addEventListener('online', () => {
    showNotification('网络已恢复', 'success');
});

window.addEventListener('offline', () => {
    showNotification('网络已断开，请检查网络连接', 'error');
});

function renderResult(data, questionType) {
    const bazi = data.bazi;
    const dayun = data.dayun;
    const liunian = data.liunian;
    
    let html = `
        <div class="result-title">📊 八字分析结果</div>
        
        <div class="bazi-grid">
            <div class="bazi-item">
                <div class="label">年柱</div>
                <div class="value">${escapeHtml(bazi.year)}</div>
            </div>
            <div class="bazi-item">
                <div class="label">月柱</div>
                <div class="value">${escapeHtml(bazi.month)}</div>
            </div>
            <div class="bazi-item">
                <div class="label">日柱</div>
                <div class="value">${escapeHtml(bazi.day)}</div>
            </div>
            <div class="bazi-item">
                <div class="label">时柱</div>
                <div class="value">${escapeHtml(bazi.hour)}</div>
            </div>
        </div>
        
        <div class="info-row">
            <span class="label">命主</span>
            <span class="value">${escapeHtml(data.mingshu)}</span>
        </div>
        <div class="info-row">
            <span class="label">喜用神</span>
            <span class="value">${escapeHtml(data.xiyongshen)}</span>
        </div>
        <div class="info-row">
            <span class="label">五行强度</span>
            <span class="value">木:${data.wuxing_strength.木} 火:${data.wuxing_strength.火} 土:${data.wuxing_strength.土} 金:${data.wuxing_strength.金} 水:${data.wuxing_strength.水}</span>
        </div>
        
        <div class="section">
            <div class="section-title">📅 大运（20-60岁）</div>
            <div class="dayun-list">
                ${dayun.map(d => `
                    <div class="dayun-item">
                        <span class="dayun-age">${d.age}-${d.age+9}岁</span> 
                        <span>${escapeHtml(d.ganzhi)}</span>
                        <span style="color: #888; font-size: 12px;">(${d.start}-${d.end}年)</span>
                    </div>
                `).join('')}
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">📆 近三年流年</div>
            <div class="liunian-list">
                ${liunian.map(l => `
                    <div class="liunian-item">
                        <span>${l.year}年</span>
                        <span style="color: #f0e68c; margin-left: 10px;">${escapeHtml(l.ganzhi)}</span>
                    </div>
                `).join('')}
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">✨ ${escapeHtml(questionType)}分析</div>
            <div class="analysis markdown-content">${parseMarkdown(data.analysis)}</div>
        </div>
    `;
    
    document.getElementById('result').innerHTML = html;
}

document.addEventListener('DOMContentLoaded', function() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('birthDate').value = today;
    document.getElementById('birthTime').value = '12:00';
});
