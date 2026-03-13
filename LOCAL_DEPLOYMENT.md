# 算命机器人 - 本地部署指南

## 📋 目录

1. [环境要求](#环境要求)
2. [快速开始](#快速开始)
3. [详细安装步骤](#详细安装步骤)
4. [配置说明](#配置说明)
5. [运行测试](#运行测试)
6. [常见问题](#常见问题)
7. [性能优化建议](#性能优化建议)

---

## 环境要求

### 系统要求
- **操作系统**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **内存**: 最低 512MB RAM
- **磁盘空间**: 至少 100MB 可用空间

### 软件要求
- **Python**: 3.8 或更高版本
- **pip**: 最新版本

### API密钥要求
您需要一个大模型API密钥，支持以下服务商：
- **OpenAI** (推荐): https://platform.openai.com/api-keys
- **DeepSeek**: https://platform.deepseek.com/
- **Moonshot (月之暗面)**: https://platform.moonshot.cn/
- **智谱AI**: https://open.bigmodel.cn/
- **火山引擎**: https://www.volcengine.com/

---

## 快速开始

### macOS / Linux

```bash
# 1. 进入项目目录
cd fortune-teller

# 2. 给启动脚本添加执行权限
chmod +x start.sh

# 3. 运行启动脚本
./start.sh

# 4. 首次运行会提示创建.env文件，按提示配置API密钥后重新运行
```

### Windows

```cmd
# 1. 进入项目目录
cd fortune-teller

# 2. 双击运行 start.bat 或在命令行执行
start.bat

# 3. 首次运行会提示创建.env文件，按提示配置API密钥后重新运行
```

---

## 详细安装步骤

### 步骤1: 安装Python

#### macOS
```bash
# 使用Homebrew安装
brew install python3

# 或从官网下载: https://www.python.org/downloads/
```

#### Windows
从Python官网下载安装包: https://www.python.org/downloads/
安装时勾选 "Add Python to PATH"

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 步骤2: 创建虚拟环境

```bash
# 进入项目目录
cd fortune-teller

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 步骤3: 安装依赖

```bash
# 升级pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

依赖包列表：
- `fastapi==0.109.0` - Web框架
- `uvicorn==0.27.0` - ASGI服务器
- `httpx==0.26.0` - HTTP客户端
- `sxtwl==1.1.5` - 八字计算库
- `python-dotenv==1.0.0` - 环境变量管理
- `python-dateutil==2.8.2` - 日期处理
- `pytz==2024.1` - 时区处理

### 步骤4: 配置API密钥

#### 方法1: 使用.env文件（推荐）

```bash
# 复制配置模板
cp .env.example .env

# 编辑.env文件
# macOS/Linux:
nano .env

# Windows:
notepad .env
```

修改以下配置：
```env
# API配置（必填）
LLM_API_KEY=your-actual-api-key-here

# 其他配置（可选）
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-3.5-turbo
HOST=127.0.0.1
PORT=8080
```

#### 方法2: 使用环境变量

```bash
# macOS/Linux (临时)
export LLM_API_KEY="your-api-key-here"
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL="gpt-3.5-turbo"

# macOS/Linux (永久，添加到 ~/.bashrc 或 ~/.zshrc)
echo 'export LLM_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc

# Windows (临时)
set LLM_API_KEY=your-api-key-here

# Windows (永久 - 系统环境变量)
# 控制面板 → 系统 → 高级系统设置 → 环境变量
```

### 步骤5: 启动服务

```bash
# 确保虚拟环境已激活
python app.py
```

看到以下输出表示启动成功：
```
🔮 算命机器人服务启动中...
📍 访问地址: http://127.0.0.1:8080
🤖 使用模型: gpt-3.5-turbo
🌐 API地址: https://api.openai.com/v1

INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8080
```

### 步骤6: 访问应用

打开浏览器访问: http://127.0.0.1:8080

---

## 配置说明

### 环境变量详解

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `LLM_API_KEY` | ✅ | 无 | 大模型API密钥 |
| `LLM_BASE_URL` | ❌ | `https://api.openai.com/v1` | API基础URL |
| `LLM_MODEL` | ❌ | `gpt-3.5-turbo` | 模型名称 |
| `HOST` | ❌ | `127.0.0.1` | 服务监听地址 |
| `PORT` | ❌ | `8080` | 服务监听端口 |

### 不同服务商配置示例

#### OpenAI
```env
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-xxxxxxxxxxxxxxxx
LLM_MODEL=gpt-3.5-turbo
```

#### DeepSeek
```env
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_API_KEY=sk-xxxxxxxxxxxxxxxx
LLM_MODEL=deepseek-chat
```

#### Moonshot
```env
LLM_BASE_URL=https://api.moonshot.cn/v1
LLM_API_KEY=sk-xxxxxxxxxxxxxxxx
LLM_MODEL=moonshot-v1-8k
```

#### 智谱AI
```env
LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4
LLM_API_KEY=xxxxxxxxxxxxxxxx
LLM_MODEL=glm-4
```

#### 火山引擎（原服务器配置）
```env
LLM_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
LLM_API_KEY=xxxxxxxxxxxxxxxx
LLM_MODEL=ark-code-latest
```

---

## 运行测试

### 1. 功能测试

#### 测试八字计算模块
```bash
# 运行八字计算测试
python bazi_parser.py
```

预期输出：
```
=== 测试结果 ===
八字: {'year': '丁丑', 'month': '壬子', 'day': '壬寅', 'hour': '庚戌', 'day_zhu': '寅'}
五行强度: {'木': 2.0, '火': 1, '土': 2, '金': 2, '水': 4.0}
十神: {'year': '丁（财星）', 'month': '壬（比肩）', 'day': '壬（日主）', 'hour': '庚（印星）'}
喜用神: 木,火,财星
命主: 身强
大运: [...]
流年: [...]
```

#### 测试API接口
```bash
# 启动服务
python app.py

# 在另一个终端测试API
curl -X POST http://127.0.0.1:8080/api/fortune \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1997-04-15",
    "birth_time": "15:00",
    "gender": "男",
    "question_type": "事业"
  }'
```

### 2. 浏览器测试

1. 访问 http://127.0.0.1:8080
2. 填写表单：
   - 出生日期: 1997-04-15
   - 出生时间: 15:00
   - 性别: 男
   - 问题类型: 事业
3. 点击"开始算命"
4. 等待结果返回（通常需要10-30秒）

### 3. 日志验证

```bash
# 查看日志文件
ls -lh logs/

# 查看最新日志
cat logs/*.json | python -m json.tool
```

---

## 常见问题

### Q1: 启动时提示"未配置API密钥"

**原因**: 未设置 `LLM_API_KEY` 环境变量

**解决方案**:
```bash
# 方法1: 创建.env文件
cp .env.example .env
# 编辑.env文件，填入API密钥

# 方法2: 设置环境变量
export LLM_API_KEY="your-api-key"
```

### Q2: 安装sxtwl库失败

**原因**: sxtwl库需要编译C扩展

**解决方案**:
```bash
# macOS
xcode-select --install
pip install sxtwl

# Linux (Ubuntu/Debian)
sudo apt install build-essential python3-dev
pip install sxtwl

# Windows
# 从 https://www.lfd.uci.edu/~gohlke/pythonlibs/ 下载预编译包
pip install sxtwl‑1.1.5‑cp311‑cp311‑win_amd64.whl
```

### Q3: API调用失败

**可能原因**:
1. API密钥无效
2. 网络连接问题
3. API配额用尽

**解决方案**:
```bash
# 检查API密钥是否正确
echo $LLM_API_KEY

# 测试网络连接
curl -I https://api.openai.com

# 查看详细错误信息
# 在app.py中添加日志输出
```

### Q4: 端口被占用

**错误信息**: `Address already in use`

**解决方案**:
```bash
# 方法1: 修改端口
export PORT=8081
python app.py

# 方法2: 查找并关闭占用进程
# macOS/Linux:
lsof -i :8080
kill -9 <PID>

# Windows:
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

### Q5: 响应速度慢

**原因**: 大模型API调用需要时间

**优化方案**:
1. 使用更快的模型（如 gpt-3.5-turbo）
2. 减少max_tokens参数
3. 使用国内API服务商（如DeepSeek、智谱AI）
4. 启用API响应缓存（需要修改代码）

---

## 性能优化建议

### 1. 本地缓存优化

在 `app.py` 中添加简单缓存：
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_bazi_analysis(birth_date, birth_time, gender):
    return analyze_bazi(birth_date, birth_time, gender, '其他')
```

### 2. 并发处理

Uvicorn默认配置已支持并发，可调整worker数量：
```bash
uvicorn app:app --workers 4 --host 127.0.0.1 --port 8080
```

### 3. 资源限制处理

#### 内存限制
- 单次请求内存占用: ~50MB
- 建议可用内存: 512MB+

#### CPU限制
- 八字计算: CPU密集型（<100ms）
- API调用: I/O密集型（10-30s）

#### 网络限制
- API请求超时: 60秒
- 建议网络带宽: 1Mbps+

### 4. 日志管理

定期清理日志文件：
```bash
# 删除7天前的日志
find logs/ -name "*.json" -mtime +7 -delete
```

### 5. 安全建议

1. **不要提交.env文件到版本控制**
   ```bash
   # 添加到.gitignore
   echo ".env" >> .gitignore
   echo "venv/" >> .gitignore
   echo "__pycache__/" >> .gitignore
   ```

2. **使用HTTPS（生产环境）**
   ```bash
   # 使用nginx反向代理
   # 或使用certbot配置SSL证书
   ```

3. **限制访问IP**
   ```python
   # 在app.py中添加IP白名单
   ALLOWED_IPS = ['127.0.0.1', '192.168.1.0/24']
   ```

---

## 与原服务器版本的差异

### 已移除的配置
- ❌ 硬编码的火山引擎API密钥
- ❌ 固定的服务器监听地址（0.0.0.0）
- ❌ 特定云服务商依赖

### 新增功能
- ✅ 环境变量配置支持
- ✅ .env文件配置
- ✅ 多API服务商支持
- ✅ 本地开发启动脚本
- ✅ 详细的错误提示

### 保持不变
- ✅ 核心八字计算逻辑
- ✅ 大模型提示词模板
- ✅ 前端界面
- ✅ 日志记录功能
- ✅ API接口设计

---

## 技术支持

如遇到问题，请检查：
1. Python版本是否符合要求
2. 所有依赖是否正确安装
3. API密钥是否有效
4. 网络连接是否正常
5. 查看logs目录下的日志文件

祝您使用愉快！🔮
