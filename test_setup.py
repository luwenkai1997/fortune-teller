#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
算命机器人 - 功能测试脚本
用于验证本地部署是否成功
"""

import sys
import os
import json
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_success(msg):
    print(f"✅ {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def print_warning(msg):
    print(f"⚠️  {msg}")

def print_info(msg):
    print(f"ℹ️  {msg}")

def test_python_version():
    print_header("测试 1: Python版本检查")
    version = sys.version_info
    print(f"当前Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print_success("Python版本符合要求 (>= 3.8)")
        return True
    else:
        print_error("Python版本过低，需要 3.8 或更高版本")
        return False

def test_dependencies():
    print_header("测试 2: 依赖包检查")
    
    required_packages = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'httpx': 'httpx',
        'sxtwl': 'sxtwl',
        'dotenv': 'python-dotenv',
        'pydantic': 'pydantic'
    }
    
    all_installed = True
    for module, package in required_packages.items():
        try:
            __import__(module)
            print_success(f"{package} 已安装")
        except ImportError:
            print_error(f"{package} 未安装")
            all_installed = False
    
    if all_installed:
        print_success("\n所有依赖包已正确安装")
    else:
        print_warning("\n部分依赖包未安装，请运行: pip install -r requirements.txt")
    
    return all_installed

def test_env_config():
    print_header("测试 3: 环境变量配置检查")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        print_success(".env 文件存在")
        
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
        
        api_key = os.getenv('LLM_API_KEY', '')
        base_url = os.getenv('LLM_BASE_URL', '')
        model = os.getenv('LLM_MODEL', '')
        
        if api_key and api_key != 'your-api-key-here':
            print_success(f"LLM_API_KEY 已配置 (长度: {len(api_key)})")
        else:
            print_error("LLM_API_KEY 未配置或使用默认值")
            print_info("请编辑.env文件，设置您的API密钥")
            return False
        
        if base_url:
            print_success(f"LLM_BASE_URL: {base_url}")
        else:
            print_info("LLM_BASE_URL 使用默认值")
        
        if model:
            print_success(f"LLM_MODEL: {model}")
        else:
            print_info("LLM_MODEL 使用默认值")
        
        return True
    else:
        print_error(".env 文件不存在")
        if env_example.exists():
            print_info("请运行: cp .env.example .env")
        return False

def test_bazi_parser():
    print_header("测试 4: 八字计算模块测试")
    
    try:
        from bazi_parser import analyze_bazi
        
        print_info("测试数据: 1997-12-15 19:31 男")
        result = analyze_bazi('1997-12-15', '19:31', '男', '事业')
        
        print_success("八字计算成功")
        print(f"\n八字: {result['bazi']}")
        print(f"五行强度: {result['wuxing_strength']}")
        print(f"命主: {result['mingshu']}")
        print(f"喜用神: {result['xiyongshen']}")
        
        if result['dayun']:
            print_success(f"大运计算成功 ({len(result['dayun'])}个)")
        
        if result['liunian']:
            print_success(f"流年计算成功 ({len(result['liunian'])}个)")
        
        return True
    except Exception as e:
        print_error(f"八字计算失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_app_import():
    print_header("测试 5: 应用模块导入测试")
    
    try:
        print_info("导入 app.py...")
        import app
        
        print_success("app.py 导入成功")
        
        if hasattr(app, 'app'):
            print_success("FastAPI应用实例创建成功")
        
        if hasattr(app, 'LLM_CONFIG'):
            print_success(f"LLM配置加载成功")
            print(f"  - API地址: {app.LLM_CONFIG['base_url']}")
            print(f"  - 模型: {app.LLM_CONFIG['model']}")
        
        return True
    except ValueError as e:
        if "未配置API密钥" in str(e):
            print_error("API密钥未配置")
            print_info("请设置环境变量 LLM_API_KEY 或在.env文件中配置")
            return False
        else:
            print_error(f"导入失败: {str(e)}")
            return False
    except Exception as e:
        print_error(f"导入失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_static_files():
    print_header("测试 6: 静态文件检查")
    
    static_dir = Path('static')
    index_file = static_dir / 'index.html'
    
    if static_dir.exists() and static_dir.is_dir():
        print_success("static/ 目录存在")
    else:
        print_error("static/ 目录不存在")
        return False
    
    if index_file.exists():
        print_success("index.html 存在")
        size = index_file.stat().st_size
        print_info(f"文件大小: {size} 字节")
        return True
    else:
        print_error("index.html 不存在")
        return False

def test_logs_directory():
    print_header("测试 7: 日志目录检查")
    
    logs_dir = Path('logs')
    
    if logs_dir.exists():
        print_success("logs/ 目录存在")
        
        log_files = list(logs_dir.glob('*.json'))
        if log_files:
            print_info(f"找到 {len(log_files)} 个日志文件")
            latest = max(log_files, key=lambda f: f.stat().st_mtime)
            print_info(f"最新日志: {latest.name}")
        else:
            print_info("暂无日志文件（运行后会自动生成）")
        
        return True
    else:
        print_warning("logs/ 目录不存在，将在首次运行时创建")
        return True

def run_all_tests():
    print("\n" + "🔮" * 30)
    print("  算命机器人 - 本地部署测试")
    print("🔮" * 30)
    
    tests = [
        ("Python版本", test_python_version),
        ("依赖包", test_dependencies),
        ("环境变量", test_env_config),
        ("八字计算", test_bazi_parser),
        ("应用导入", test_app_import),
        ("静态文件", test_static_files),
        ("日志目录", test_logs_directory),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"{name}测试异常: {str(e)}")
            results.append((name, False))
    
    print_header("测试结果汇总")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:15s} {status}")
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n" + "🎉" * 30)
        print("  所有测试通过！可以启动服务")
        print("🎉" * 30)
        print("\n启动命令:")
        print("  python app.py")
        print("\n或使用启动脚本:")
        print("  ./start.sh  (macOS/Linux)")
        print("  start.bat   (Windows)")
        return 0
    else:
        print("\n" + "⚠️" * 30)
        print("  部分测试未通过，请检查上述错误信息")
        print("⚠️" * 30)
        return 1

if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
