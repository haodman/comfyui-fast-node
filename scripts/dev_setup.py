#!/usr/bin/env python3
"""
ComfyUI FastNode插件 - 开发环境设置脚本
用于快速设置开发环境和工作流
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """打印欢迎横幅"""
    print("=" * 60)
    print("🎨 ComfyUI FastNode插件 - 开发环境设置")
    print("=" * 60)
    print()

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """安装依赖包"""
    print("\n📦 安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖包安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False

def create_dev_directories():
    """创建开发目录"""
    print("\n📁 创建开发目录...")
    directories = [
        "./dev_output",
        "./test_output", 
        "./logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ 创建目录: {directory}")

def create_test_files():
    """创建测试文件"""
    print("\n🧪 创建测试文件...")
    
    # 创建测试配置
    test_config = {
        "dev_mode": True,
        "hot_reload": True,
        "output_dir": "./dev_output",
        "test_prompts": [
            "a beautiful landscape",
            "a cute cat",
            "a futuristic city"
        ]
    }
    
    import json
    with open("dev_config.json", "w", encoding="utf-8") as f:
        json.dump(test_config, f, ensure_ascii=False, indent=2)
    
    print("✅ 创建测试配置文件: dev_config.json")

def setup_git_hooks():
    """设置Git钩子（如果存在Git仓库）"""
    print("\n🔧 设置Git钩子...")
    if Path(".git").exists():
        hooks_dir = Path(".git/hooks")
        hooks_dir.mkdir(exist_ok=True)
        
        # 创建pre-commit钩子
        pre_commit_hook = """#!/bin/bash
echo "🔍 运行代码检查..."
python -m py_compile custom_naming_saver.py
if [ $? -eq 0 ]; then
    echo "✅ 代码检查通过"
    exit 0
else
    echo "❌ 代码检查失败"
    exit 1
fi
"""
        
        hook_file = hooks_dir / "pre-commit"
        with open(hook_file, "w") as f:
            f.write(pre_commit_hook)
        
        # 设置执行权限
        os.chmod(hook_file, 0o755)
        print("✅ 创建Git pre-commit钩子")
    else:
        print("ℹ️ 未检测到Git仓库，跳过Git钩子设置")

def print_dev_instructions():
    """打印开发说明"""
    print("\n" + "=" * 60)
    print("🚀 开发环境设置完成！")
    print("=" * 60)
    print()
    print("📋 开发工作流程：")
    print("1. 启动ComfyUI")
    print("2. 加载 dev_workflow.json 工作流")
    print("3. 启动热更新监控（设置HotReloadControlNode为'start'）")
    print("4. 修改 custom_naming_saver.py 文件")
    print("5. 使用HotReloadNode触发重新加载")
    print("6. 测试新功能")
    print()
    print("📁 可用目录：")
    print("- ./dev_output/     - 开发输出目录")
    print("- ./test_output/    - 测试输出目录")
    print("- ./logs/          - 日志目录")
    print()
    print("🔧 可用文件：")
    print("- dev_workflow.json - 开发工作流")
    print("- dev_config.json  - 开发配置")
    print("- hot_reload_manager.py - 热更新管理器")
    print()
    print("💡 提示：")
    print("- 修改代码后使用热更新节点重新加载")
    print("- 查看ComfyUI控制台获取详细日志")
    print("- 使用dev_workflow.json进行快速测试")
    print()

def main():
    """主函数"""
    print_banner()
    
    if not check_python_version():
        return 1
    
    if not install_dependencies():
        return 1
    
    create_dev_directories()
    create_test_files()
    setup_git_hooks()
    print_dev_instructions()
    
    return 0

if __name__ == "__main__":
    exit(main()) 