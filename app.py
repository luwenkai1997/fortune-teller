# -*- coding: utf-8 -*-
"""
算命机器人 - FastAPI 服务
"""

import os
import json
import uuid
import datetime
from pathlib import Path
from typing import Optional

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

app = FastAPI(title="算命机器人", description="八字算命服务")

# 挂载静态文件
app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")

# ============ 数据模型 ============
class FortuneRequest(BaseModel):
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    gender: str      # 男/女
    question_type: str  # 事业/姻缘/财运/健康/学业/其他


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
def build_prompt(bazi_data: dict, question_type: str) -> str:
    """构建发送给大模型的提示词"""
    
    bazi = bazi_data['bazi']
    wuxing = bazi_data['wuxing_strength']
    shishen = bazi_data['shishen']
    xiyongshen = bazi_data['xiyongshen']
    mingshu = bazi_data['mingshu']
    dayun = bazi_data['dayun']
    liunian = bazi_data['liunian']
    
    # 问题类型映射
    question_map = {
        '事业': '事业发展、职业选择、工作运势',
        '姻缘': '感情婚姻、桃花运、红鸾星、正缘',
        '财运': '财富运势、赚钱机会、理财建议',
        '健康': '身体健康、平安福祸',
        '学业': '考试学业、升学运势',
        '其他': '综合运势'
    }
    
    prompt = f"""你是一位专业的八字命理师，请根据以下八字信息进行分析。

【八字信息】
- 年柱：{bazi['year']}
- 月柱：{bazi['month']}
- 日柱：{bazi['day']}（日主）
- 时柱：{bazi['hour']}

【五行强度】
木:{wuxing['木']} 火:{wuxing['火']} 土:{wuxing['土']} 金:{wuxing['金']} 水:{wuxing['水']}

【十神】
- 年干：{shishen['year']}
- 月干：{shishen['month']}
- 日干：{shishen['day']}
- 时干：{shishen['hour']}

【命主】
{mingshu}

【喜用神】
{xiyongshen}

【大运】（20-60岁）
"""
    for d in dayun:
        prompt += f"- {d['age']}-{d['age']+9}岁（{d['start']}-{d['end']}年）: {d['ganzhi']}\n"
    
    prompt += f"""
【近三年流年】
"""
    for l in liunian:
        prompt += f"- {l['year']}年: {l['ganzhi']}\n"
    
    prompt += f"""
【用户问题】
{question_map.get(question_type, question_type)}

请分析：
1. 命主性格特点
2. 五行平衡情况
3. 喜用神对命主的影响
4. 针对用户问题的详细分析
5. 大运期间（20-60岁）的运势，包括：
   - 感情运势
   - 事业运势  
   - 财运
   - 健康状况
6. 近三年流年运势
7. 综合建议

请用通俗易懂的语言回答，在分析和建议方面尽量详细，控制在5000字以内。"""
    
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


@app.post("/api/fortune")
async def calculate_fortune(request: FortuneRequest):
    """算命接口"""
    try:
        # 1. 解析八字
        bazi_data = analyze_bazi(
            request.birth_date,
            request.birth_time,
            request.gender,
            request.question_type
        )
        
        # 2. 构建提示词
        prompt = build_prompt(bazi_data, request.question_type)
        
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