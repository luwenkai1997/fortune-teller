# -*- coding: utf-8 -*-
"""
算命机器人 - FastAPI 服务
"""

import os
import json
import uuid
import datetime
import shutil
from pathlib import Path
from typing import Optional
from datetime import timedelta

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from bazi_parser import analyze_bazi

# ============ 配置 ============
APP_DIR = Path(__file__).parent
LOGS_DIR = APP_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

class LogManager:
    def __init__(self, logs_dir: Path, max_days: int = 30, max_size_mb: int = 100):
        self.logs_dir = logs_dir
        self.max_days = max_days
        self.max_size_mb = max_size_mb
    
    def cleanup_old_logs(self):
        """清理过期日志"""
        cutoff_date = datetime.datetime.now() - timedelta(days=self.max_days)
        
        for log_file in self.logs_dir.glob('*.json'):
            try:
                filename = log_file.stem
                if len(filename) >= 8:
                    file_date_str = filename.split('-')[0] + '-' + filename.split('-')[1][:2] + '-' + filename.split('-')[1][2:4]
                    file_date = datetime.datetime.strptime(file_date_str, '%Y-%m%d')
                    
                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"已删除过期日志: {log_file.name}")
            except Exception as e:
                print(f"解析日志日期失败: {log_file.name}, {e}")
    
    def check_logs_size(self):
        """检查日志总大小"""
        total_size = sum(f.stat().st_size for f in self.logs_dir.glob('*.json'))
        total_size_mb = total_size / (1024 * 1024)
        
        if total_size_mb > self.max_size_mb:
            print(f"日志总大小 {total_size_mb:.2f}MB 超过限制 {self.max_size_mb}MB")
            self.cleanup_old_logs()
    
    def archive_logs(self):
        """归档日志"""
        archive_dir = self.logs_dir / 'archive'
        archive_dir.mkdir(exist_ok=True)
        
        archive_name = f"logs_{datetime.datetime.now().strftime('%Y%m%d')}.tar.gz"
        archive_path = archive_dir / archive_name
        
        shutil.make_archive(
            str(archive_path.with_suffix('')),
            'gztar',
            self.logs_dir,
            '.'
        )
        
        print(f"日志已归档: {archive_path}")
        
        for log_file in self.logs_dir.glob('*.json'):
            log_file.unlink()

log_manager = LogManager(LOGS_DIR, max_days=30, max_size_mb=100)

app = FastAPI(title="算命机器人", description="八字算命服务")

@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    log_manager.cleanup_old_logs()
    log_manager.check_logs_size()
    print("日志清理检查完成")

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """添加安全响应头"""
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' https://fonts.gstatic.com;"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")

# ============ 数据模型 ============
class FortuneRequest(BaseModel):
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    gender: str      # 男/女
    question_type: str  # 事业/姻缘/财运/健康/学业/其他
    
    def validate_input(self):
        """验证输入数据"""
        import re
        from datetime import datetime
        
        errors = []
        
        # 验证日期格式
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', self.birth_date):
            errors.append('日期格式不正确')
        else:
            try:
                date = datetime.strptime(self.birth_date, '%Y-%m-%d')
                if date > datetime.now():
                    errors.append('出生日期不能晚于今天')
                if date.year < 1900:
                    errors.append('出生日期不能早于1900年')
            except ValueError:
                errors.append('无效的日期')
        
        # 验证时间格式
        if not re.match(r'^\d{2}:\d{2}$', self.birth_time):
            errors.append('时间格式不正确')
        
        # 验证性别
        if self.gender not in ['男', '女']:
            errors.append('性别选项无效')
        
        # 验证问题类型
        if self.question_type not in ['事业', '姻缘', '财运', '健康', '学业', '其他']:
            errors.append('问题类型无效')
        
        return errors


class FortuneResponse(BaseModel):
    success: bool
    bazi: dict
    wuxing_strength: dict
    shishen: dict
    xiyongshen: str
    mingshu: str
    dayun: list
    liunian: list
    analysis: str


# ============ 提示词模板 ============
def build_prompt(bazi_data: dict, question_type: str, gender: str) -> str:
    """构建优化的提示词"""
    
    bazi = bazi_data['bazi']
    wuxing = bazi_data['wuxing_strength']
    shishen = bazi_data['shishen']
    xiyongshen = bazi_data['xiyongshen']
    mingshu = bazi_data['mingshu']
    dayun = bazi_data['dayun']
    liunian = bazi_data['liunian']
    
    question_map = {
        '事业': '事业发展、职业选择、工作运势',
        '姻缘': '感情婚姻、桃花运、红鸾星、正缘',
        '财运': '财富运势、赚钱机会、理财建议',
        '健康': '身体健康、平安福祸',
        '学业': '考试学业、升学运势',
        '其他': '综合运势'
    }
    
    prompt = f"""# 八字命理分析任务

## 角色定位
你是一位资深的八字命理师，拥有30年的实战经验。请用通俗易懂、温暖亲切的语言为用户分析命理，避免过于玄奥的术语。

## 用户信息
- 问题类型：{question_map.get(question_type, question_type)}
- 性别：{'男命' if gender == '男' else '女命'}

## 八字命盘
```
年柱：{bazi['year']}  月柱：{bazi['month']}
日柱：{bazi['day']}（日主）  时柱：{bazi['hour']}
```

## 命理分析数据

### 五行强度
| 五行 | 强度 |
|------|------|
| 木 | {wuxing['木']} |
| 火 | {wuxing['火']} |
| 土 | {wuxing['土']} |
| 金 | {wuxing['金']} |
| 水 | {wuxing['水']} |

### 十神格局
- 年干：{shishen['year']}
- 月干：{shishen['month']}
- 日干：{shishen['day']}
- 时干：{shishen['hour']}

### 命主特征
- 命主：{mingshu}
- 喜用神：{xiyongshen}

### 大运（20-60岁）
{chr(10).join([f"- {d['age']}-{d['age']+9}岁（{d['start']}-{d['end']}年）：{d['ganzhi']}" for d in dayun])}

### 近三年流年
{chr(10).join([f"- {l['year']}年：{l['ganzhi']}" for l in liunian])}

## 分析要求

请按照以下结构进行分析，每个部分都要详细且实用：

### 1. 命主性格特点（200-300字）
- 性格优势
- 性格劣势
- 人际交往特点
- 适合的职业方向

### 2. 五行平衡分析（150-200字）
- 五行强弱分析
- 缺失五行的影响
- 补救建议（颜色、方位、数字等）

### 3. 喜用神解读（150-200字）
- 喜用神的含义
- 对命主的帮助
- 如何运用喜用神

### 4. {question_type}专项分析（400-500字）
针对用户关心的"{question_map.get(question_type, question_type)}"问题，提供：
- 当前状况分析
- 未来趋势预测
- 具体建议和注意事项
- 最佳时机和方位

### 5. 大运流年运势（300-400字）
- 20-30岁：感情、事业、财运、健康
- 30-40岁：感情、事业、财运、健康
- 40-50岁：感情、事业、财运、健康
- 50-60岁：感情、事业、财运、健康

### 6. 近三年流年提示（200-300字）
逐年分析2024、2025、2026年的：
- 整体运势
- 注意事项
- 发展机遇

### 7. 综合建议（150-200字）
- 人生发展建议
- 需要避免的事项
- 开运方法

## 输出要求
1. 语言通俗易懂，避免专业术语堆砌
2. 分析要具体实用，不要泛泛而谈
3. 建议要可操作，给出明确的方向
4. 保持温暖积极的语气，给用户信心
5. 总字数控制在2000-3000字
6. 使用Markdown格式输出，结构清晰

## 示例输出格式
```
## 命主性格特点

根据您的八字分析，您是一位...

## 五行平衡分析

您的五行分布情况为...

## 喜用神解读

您的喜用神为...

## {question_type}专项分析

针对您的{question_type}运势...

## 大运流年运势

### 20-30岁（2017-2027年）
...

## 近三年流年提示

### 2024年（甲辰年）
...

## 综合建议

综合以上分析，建议您...
```

请开始您的分析："""
    
    return prompt


# ============ 日志记录 ============
def save_log(request_data: dict, bazi_data: dict, analysis: str):
    """保存算命日志"""
    timestamp = datetime.datetime.now().strftime('%Y-%m%d-%H%M%S')
    log_file = LOGS_DIR / f"{timestamp}.json"
    
    log_data = {
        'id': str(uuid.uuid4()),
        'timestamp': datetime.datetime.now().isoformat(),
        'input': request_data,
        'bazi': bazi_data['bazi'],
        'wuxing_strength': bazi_data['wuxing_strength'],
        'shishen': bazi_data['shishen'],
        'xiyongshen': bazi_data['xiyongshen'],
        'mingshu': bazi_data['mingshu'],
        'dayun': bazi_data['dayun'],
        'liunian': bazi_data['liunian'],
        'output': analysis
    }
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    return log_data['id']


# ============ 大模型调用 ============
LLM_CONFIG = {
    'base_url': os.getenv('LLM_BASE_URL', 'https://api.openai.com/v1'),
    'api_key': os.getenv('LLM_API_KEY', ''),
    'model': os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
}

if not LLM_CONFIG['api_key']:
    raise ValueError(
        "未配置API密钥！请在.env文件中设置LLM_API_KEY环境变量，\n"
        "或直接设置环境变量: export LLM_API_KEY=your-api-key"
    )


async def call_llm(prompt: str) -> str:
    """调用大模型"""
    import httpx
    
    headers = {
        'Authorization': f'Bearer {LLM_CONFIG["api_key"]}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': LLM_CONFIG['model'],
        'messages': [
            {'role': 'system', 'content': '你是一位专业的八字命理师，擅长分析八字、五行、大运流年。请用通俗易懂的语言为用户分析命理。'},
            {'role': 'user', 'content': prompt}
        ],
        'max_tokens': 10000,
        'temperature': 0.7
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f'{LLM_CONFIG["base_url"]}/chat/completions',
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"API调用失败: {response.status_code} - {response.text}"


# ============ 路由 ============
@app.get("/")
async def index():
    """主页，返回前端页面"""
    from fastapi.responses import FileResponse
    return FileResponse(APP_DIR / "static" / "index.html")


@app.post("/api/admin/cleanup-logs")
async def cleanup_logs_manual():
    """手动清理日志"""
    try:
        log_manager.cleanup_old_logs()
        log_manager.check_logs_size()
        return {"success": True, "message": "日志清理完成"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/admin/archive-logs")
async def archive_logs_manual():
    """手动归档日志"""
    try:
        log_manager.archive_logs()
        return {"success": True, "message": "日志归档完成"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/fortune")
async def calculate_fortune(request: FortuneRequest):
    """算命接口"""
    try:
        # 验证输入
        validation_errors = request.validate_input()
        if validation_errors:
            return {
                'success': False,
                'error': '; '.join(validation_errors)
            }
        
        # 1. 解析八字
        bazi_data = analyze_bazi(
            request.birth_date,
            request.birth_time,
            request.gender,
            request.question_type
        )
        
        # 2. 构建提示词
        prompt = build_prompt(bazi_data, request.question_type, request.gender)
        
        # 3. 调用大模型
        analysis = await call_llm(prompt)
        
        # 4. 保存日志
        log_id = save_log(
            {
                'birth_date': request.birth_date,
                'birth_time': request.birth_time,
                'gender': request.gender,
                'question_type': request.question_type
            },
            bazi_data,
            analysis
        )
        
        # 5. 返回结果
        return {
            'success': True,
            'log_id': log_id,
            'bazi': bazi_data['bazi'],
            'wuxing_strength': bazi_data['wuxing_strength'],
            'shishen': bazi_data['shishen'],
            'xiyongshen': bazi_data['xiyongshen'],
            'mingshu': bazi_data['mingshu'],
            'dayun': bazi_data['dayun'],
            'liunian': bazi_data['liunian'],
            'analysis': analysis
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '8080'))
    
    print(f"\n🔮 算命机器人服务启动中...")
    print(f"📍 访问地址: http://{host}:{port}")
    print(f"🤖 使用模型: {LLM_CONFIG['model']}")
    print(f"🌐 API地址: {LLM_CONFIG['base_url']}\n")
    
    uvicorn.run(app, host=host, port=port)