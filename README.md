# 算命机器人项目技术文档

## 1. 项目概述

- **项目名称**： fortune-teller（算命机器人）
- **项目类型**： Web API 服务
- **核心功能**： 用户输入出生日期、时间和性别，生成八字并获取完整运势分析
- **目标用户**： 娱乐用途

## 2. 技术架构

### 2.1 整体架构

```
用户浏览器 → FastAPI 服务 → 前端页面(static/index.html)
                        ↓
                八字解析模块(bazi_parser.py)
                        ↓
                大模型(当前OpenClaw接入的模型)
                        ↓
                日志系统(logs/*.json)
```

### 2.2 技术栈

| 组件 | 技术选型 |
|------|----------|
| 后端框架 | FastAPI |
| 前端 | HTML + CSS（原生，无框架） |
| 大模型 | 使用当前 OpenClaw 配置的模型（通过 OpenClaw API） |
| 日志存储 | JSON 文件 |

### 2.3 目录结构

```
/root/fortune-teller/
├── PROJECT.md              # 本文件 - 项目技术文档
├── app.py                  # FastAPI 主服务
├── bazi_parser.py          # 八字解析模块
├── requirements.txt        # Python 依赖
├── static/
│   └── index.html          # 前端页面
└── logs/
    └── (JSON日志文件)
```

## 3. 功能模块

### 3.1 前端页面 (index.html)

**输入表单**：
- 出生日期（年-月-日）
- 出生时间（时:分，24小时制）
- 性别（男/女）
- 问题类型（下拉选择：事业、姻缘、财运、健康、学业、其他）

**输出展示**：
- 解析后的八字（年柱、月柱、日柱、时柱）
- 五行强度分析
- 喜用神
- 命主强弱
- 十神格局
- 大运分析（20-60岁，4个大运，每个大运包含：感情、事业、财运、健康）
- 流年分析（最近3年）
- 针对用户问题类型的专项分析

### 3.2 八字解析模块 (bazi_parser.py)

**核心功能**：
- 公历日期时间 → 八字转换
- 判定节气（中气、节令）
- 计算五行强度
- 判断喜用神
- 判断命主强弱
- 排出大运（20-60岁，4个大运）
- 排出流年（最近3年）

**八字格式**：
```
年柱：庚辰
月柱：辛巳
日柱：丙戌
时柱：丙申
```

**五行对应**：
```
天干：甲乙→木，丙丁→火，戊己→土，庚辛→金，壬癸→水
地支：寅卯→木，巳午→火，申酉→金，亥子→水，辰戌丑未→土
```

### 3.3 日志系统

**日志格式** (logs/YYYY-MM-DD-HHMMSS.json)：
```json
{
  "id": "uuid",
  "timestamp": "2026-03-13T19:00:00",
  "input": {
    "birth_date": "1997-04-15",
    "birth_time": "15:00",
    "gender": "男",
    "question_type": "事业"
  },
  "bazi": {
    "year": "庚辰",
    "month": "辛巳",
    "day": "丙戌",
    "hour": "丙申",
    "day_zhu": "戌",
    "xiyongshen": "木、火",
    "mingshu": "身弱",
    "wuxing_strength": {
      "木": 2,
      "火": 3,
      "土": 1,
      "金": 2,
      "水": 1
    },
    "shishen": {
      "年干": "庚（偏官）",
      "月干": "辛（正官）",
      "日干": "丙（日主）",
      "时干": "丙（偏印）"
    }
  },
  "dayun": [
    {"age": 20, "start": "2017", "end": "2027", "ganzhi": "壬午", "description": "..."},
    {"age": 30, "start": "2027", "end": "2037", "ganzhi": "癸未", "description": "..."},
    {"age": 40, "start": "2037", "end": "2047", "ganzhi": "甲申", "description": "..."},
    {"age": 50, "start": "2047", "end": "2057", "ganzhi": "乙酉", "description": "..."}
  ],
  "liunian": [
    {"year": "2026", "ganzhi": "丙午", "description": "..."},
    {"year": "2025", "ganzhi": "乙巳", "description": "..."},
    {"year": "2024", "ganzhi": "甲辰", "description": "..."}
  ],
  "output": "大模型的完整回答"
}
```

## 4. API 设计

### 4.1 接口列表

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 主页，返回 index.html |
| POST | /api/fortune | 算命接口 |

### 4.2 请求格式

```json
{
  "birth_date": "1997-04-15",
  "birth_time": "15:00",
  "gender": "男",
  "question_type": "事业"
}
```

### 4.3 响应格式

```json
{
  "success": true,
  "bazi": {
    "year": "庚辰",
    "month": "辛巳",
    "day": "丙戌",
    "hour": "丙申",
    "day_zhu": "戌",
    "xiyongshen": "木、火",
    "mingshu": "身弱"
  },
  "dayun": [...],
  "liunian": [...],
  "analysis": "大模型的完整分析"
}
```

## 5. 实现步骤

### 第一阶段：基础框架
1. 创建项目目录结构
2. 编写 requirements.txt
3. 实现 bazi_parser.py（八字解析核心逻辑）
4. 实现 app.py（FastAPI 服务）

### 第二阶段：前端
5. 实现 static/index.html（输入表单 + 结果展示）

### 第三阶段：大模型集成
6. 接入 OpenClaw API 进行大模型分析
7. 组装 prompt，包含完整八字信息、大运、流年

### 第四阶段：日志
8. 实现日志记录功能
9. 每次请求保存完整 JSON 日志

## 6. 注意事项

- 每次修改代码前，必须先阅读本 PROJECT.md 文件
- 八字计算必须准确（大运起始年龄、节气转换）
- 日志必须记录完整，便于复盘
- 前端先简单实现，功能优先
- 使用当前 OpenClaw 配置的大模型

## 7. 待定事项

- [ ] 大模型 prompt 优化
- [ ] 前端样式美化（后续迭代）
- [ ] 日志清理机制（后续迭代）