# 🔮 算命机器人

基于八字命理的智能算命服务，支持事业、姻缘、财运、健康、学业等多维度运势分析。

---

## 📝 更新日志

### v1.1.0 (2026-03-13)

#### ✨ 新增功能
- **Markdown渲染支持**：分析结果支持完整的Markdown语法渲染，包括标题、列表、粗体、链接等
- **输入字段禁用**：等待状态期间自动禁用所有输入字段，防止误操作
- **日志管理API**：新增手动清理和归档日志的API接口

#### 🎨 用户体验优化
- **输入验证**：添加日期范围验证（1900年至今）和实时错误提示
- **加载体验**：新增进度条动画、预估时间提示（15-30秒）和取消请求功能
- **错误处理**：友好的错误提示卡片、自动重试机制（最多2次）、网络状态实时监控
- **输入提示**：添加tooltip帮助信息和输入字段说明

#### 🔒 安全性加固
- **XSS防护**：前端HTML转义函数防止XSS攻击
- **后端验证**：添加输入数据格式验证和过滤
- **安全头**：添加CSP、X-Frame-Options、X-XSS-Protection等安全响应头

#### 🏗️ 代码质量提升
- **模块化重构**：分离HTML、CSS、JavaScript文件，提升代码可维护性
- **缓存机制**：LocalStorage缓存避免重复请求，提升响应速度
- **响应式设计**：优化移动端适配，支持多种屏幕尺寸
- **无障碍访问**：添加ARIA标签和键盘导航支持

#### ⚡ 性能优化
- **请求管理**：支持请求取消和自动重试
- **缓存策略**：1小时TTL缓存机制
- **日志清理**：自动清理30天前日志，限制日志大小100MB

#### 🤖 大模型优化
- **Prompt优化**：结构化提示词设计，明确分析要求（7个部分）
- **输出规范**：控制字数2000-3000字，Markdown格式输出

---

## 🎯 功能说明

### 核心功能

#### 八字命理分析
- **八字排盘**：根据出生日期时间自动计算年柱、月柱、日柱、时柱
- **五行分析**：计算五行强度分布，判断五行平衡情况
- **十神格局**：分析十神关系，揭示命理特征
- **喜用神判断**：智能判断喜用神，提供开运建议
- **命主强弱**：判断身强身弱，分析命理特点

#### 运势预测
- **大运分析**：20-60岁大运周期分析，每个大运包含感情、事业、财运、健康
- **流年运势**：近三年流年运势详细分析
- **专项分析**：针对事业、姻缘、财运、健康、学业等特定问题的深度分析

#### 用户体验
- **智能缓存**：相同输入自动使用缓存结果，提升响应速度
- **进度提示**：实时进度条和预估时间，缓解等待焦虑
- **错误恢复**：自动重试机制和友好的错误提示
- **网络监控**：实时检测网络状态，及时提醒用户

### 技术特性

#### 前端技术
- **响应式设计**：完美适配桌面端和移动端
- **无障碍访问**：支持屏幕阅读器和键盘导航
- **安全防护**：XSS防护和输入验证
- **性能优化**：缓存机制和请求管理

#### 后端技术
- **FastAPI框架**：高性能异步Web框架
- **精确计算**：使用sxtwl库进行准确的八字计算
- **日志管理**：完整的请求日志记录和自动清理
- **安全加固**：CSP策略和输入验证

---

## 🚀 本地部署方法

### 环境要求

#### 系统要求
- **操作系统**：Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **内存**：最低 512MB RAM
- **磁盘空间**：至少 100MB 可用空间

#### 软件要求
- **Python**：3.8 或更高版本
- **pip**：最新版本

#### API密钥要求
需要一个大模型API密钥，支持以下服务商：
- **OpenAI** (推荐)：https://platform.openai.com/api-keys
- **DeepSeek**：https://platform.deepseek.com/
- **Moonshot (月之暗面)**：https://platform.moonshot.cn/
- **智谱AI**：https://open.bigmodel.cn/

### 快速开始

#### macOS / Linux

```bash
# 1. 进入项目目录
cd fortune-teller

# 2. 给启动脚本添加执行权限
chmod +x start.sh

# 3. 运行启动脚本
./start.sh

# 4. 首次运行会提示创建.env文件，按提示配置API密钥后重新运行
```

#### Windows

```cmd
# 1. 进入项目目录
cd fortune-teller

# 2. 双击运行 start.bat 或在命令行执行
start.bat

# 3. 首次运行会提示创建.env文件，按提示配置API密钥后重新运行
```

### 详细安装步骤

#### 步骤1: 安装Python

**macOS**
```bash
# 使用Homebrew安装
brew install python3

# 或从官网下载: https://www.python.org/downloads/
```

**Windows**
从Python官网下载安装包: https://www.python.org/downloads/
安装时勾选 "Add Python to PATH"

**Linux (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### 步骤2: 创建虚拟环境

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

#### 步骤3: 安装依赖

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

#### 步骤4: 配置API密钥

**方法1: 使用.env文件（推荐）**

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

**方法2: 使用环境变量**

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

#### 步骤5: 启动服务

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

#### 步骤6: 访问应用

打开浏览器访问: http://127.0.0.1:8080

### 配置说明

#### 环境变量详解

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `LLM_API_KEY` | ✅ | 无 | 大模型API密钥 |
| `LLM_BASE_URL` | ❌ | `https://api.openai.com/v1` | API基础URL |
| `LLM_MODEL` | ❌ | `gpt-3.5-turbo` | 模型名称 |
| `HOST` | ❌ | `127.0.0.1` | 服务监听地址 |
| `PORT` | ❌ | `8080` | 服务监听端口 |

#### 不同服务商配置示例

**OpenAI**
```env
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-xxxxxxxxxxxxxxxx
LLM_MODEL=gpt-3.5-turbo
```

**DeepSeek**
```env
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_API_KEY=sk-xxxxxxxxxxxxxxxx
LLM_MODEL=deepseek-chat
```

**Moonshot**
```env
LLM_BASE_URL=https://api.moonshot.cn/v1
LLM_API_KEY=sk-xxxxxxxxxxxxxxxx
LLM_MODEL=moonshot-v1-8k
```

**智谱AI**
```env
LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4
LLM_API_KEY=xxxxxxxxxxxxxxxx
LLM_MODEL=glm-4
```

### 运行测试

#### 功能测试

**测试八字计算模块**
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

**测试API接口**
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

#### 浏览器测试

1. 访问 http://127.0.0.1:8080
2. 填写表单：
   - 出生日期: 1997-04-15
   - 出生时间: 15:00
   - 性别: 男
   - 问题类型: 事业
3. 点击"开始算命"
4. 等待结果返回（通常需要10-30秒）

### 常见问题

#### Q1: 启动时提示"未配置API密钥"

**原因**：未设置 `LLM_API_KEY` 环境变量

**解决方案**：
```bash
# 方法1: 创建.env文件
cp .env.example .env
# 编辑.env文件，填入API密钥

# 方法2: 设置环境变量
export LLM_API_KEY="your-api-key"
```

#### Q2: 安装sxtwl库失败

**原因**：sxtwl库需要编译C扩展

**解决方案**：
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

#### Q3: API调用失败

**可能原因**：
1. API密钥无效
2. 网络连接问题
3. API配额用尽

**解决方案**：
```bash
# 检查API密钥是否正确
echo $LLM_API_KEY

# 测试网络连接
curl -I https://api.openai.com

# 查看详细错误信息
# 在app.py中添加日志输出
```

#### Q4: 端口被占用

**错误信息**：`Address already in use`

**解决方案**：
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

#### Q5: 响应速度慢

**原因**：大模型API调用需要时间

**优化方案**：
1. 使用更快的模型（如 gpt-3.5-turbo）
2. 减少max_tokens参数
3. 使用国内API服务商（如DeepSeek、智谱AI）
4. 启用API响应缓存（已内置）

---

## 📁 项目结构

```
fortune-teller/
├── static/
│   ├── index.html          # 主页面
│   ├── css/
│   │   └── main.css       # 样式文件
│   └── js/
│       └── main.js        # JavaScript逻辑
├── app.py                  # FastAPI主服务
├── bazi_parser.py         # 八字解析模块
├── requirements.txt        # Python依赖
├── .env.example           # 环境变量模板
├── start.sh               # Linux/macOS启动脚本
├── start.bat              # Windows启动脚本
└── README.md              # 项目文档
```

---

## 🔧 API文档

### 接口列表

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 主页，返回 index.html |
| POST | /api/fortune | 算命接口 |
| POST | /api/admin/cleanup-logs | 手动清理日志 |
| POST | /api/admin/archive-logs | 手动归档日志 |

### 请求格式

```json
{
  "birth_date": "1997-04-15",
  "birth_time": "15:00",
  "gender": "男",
  "question_type": "事业"
}
```

### 响应格式

```json
{
  "success": true,
  "log_id": "uuid",
  "bazi": {
    "year": "庚辰",
    "month": "辛巳",
    "day": "丙戌",
    "hour": "丙申"
  },
  "wuxing_strength": {
    "木": 2, "火": 3, "土": 1, "金": 2, "水": 1
  },
  "shishen": {
    "year": "庚（偏官）",
    "month": "辛（正官）",
    "day": "丙（日主）",
    "hour": "丙（偏印）"
  },
  "xiyongshen": "木、火",
  "mingshu": "身弱",
  "dayun": [...],
  "liunian": [...],
  "analysis": "大模型的完整分析（Markdown格式）"
}
```

---

## 📄 许可证

本项目仅供娱乐和学习使用，请勿用于商业用途。

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**最后更新时间**：2026-03-13
