#!/usr/bin/env python3
"""
GitHub发布脚本
用于自动化发布流程
"""

import os
import sys
import json
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

def run_command(command, cwd=None):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        print(f"错误输出: {e.stderr}")
        return None

def get_current_version():
    """获取当前版本号"""
    # 从git标签获取最新版本
    latest_tag = run_command("git describe --tags --abbrev=0 2>/dev/null || echo 'v0.0.0'")
    return latest_tag

def create_release_zip():
    """创建发布压缩包"""
    version = get_current_version()
    zip_name = f"comfyui-fast-node-{version}.zip"
    
    # 要包含的文件和目录
    include_files = [
        "__init__.py",
        "custom_naming_saver.py",
        "requirements.txt",
        "README.md",
        "USAGE.md",
        "MAINTENANCE.md",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "LICENSE",
        "install.bat",
        "install.sh",
        ".gitignore"
    ]
    
    include_dirs = [
        "web",
        "workflows",
        "scripts"
    ]
    
    print(f"创建发布包: {zip_name}")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 添加文件
        for file_path in include_files:
            if os.path.exists(file_path):
                zipf.write(file_path, file_path)
                print(f"  + {file_path}")
        
        # 添加目录
        for dir_path in include_dirs:
            if os.path.exists(dir_path):
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_path = file_path
                        zipf.write(file_path, arc_path)
                        print(f"  + {arc_path}")
    
    print(f"发布包创建完成: {zip_name}")
    return zip_name

def update_changelog(version):
    """更新CHANGELOG.md"""
    changelog_path = "CHANGELOG.md"
    
    if not os.path.exists(changelog_path):
        print("CHANGELOG.md不存在，跳过更新")
        return
    
    with open(changelog_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换未发布版本为当前版本
    today = datetime.now().strftime("%Y-%m-%d")
    content = content.replace("[未发布]", f"[{version}] - {today}")
    
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已更新CHANGELOG.md: {version}")

def create_git_tag(version, message):
    """创建Git标签"""
    print(f"创建Git标签: {version}")
    
    # 添加所有更改
    run_command("git add .")
    
    # 提交更改
    commit_message = f"Release {version}: {message}"
    run_command(f'git commit -m "{commit_message}"')
    
    # 创建标签
    run_command(f'git tag -a {version} -m "Release {version}"')
    
    print(f"Git标签创建完成: {version}")

def push_to_github():
    """推送到GitHub"""
    print("推送到GitHub...")
    
    # 推送代码
    run_command("git push origin main")
    
    # 推送标签
    run_command("git push origin --tags")
    
    print("推送完成")

def main():
    """主函数"""
    print("=== ComfyUI FastNode 发布脚本 ===")
    
    # 检查是否在Git仓库中
    if not os.path.exists(".git"):
        print("错误: 当前目录不是Git仓库")
        sys.exit(1)
    
    # 获取版本号
    current_version = get_current_version()
    print(f"当前版本: {current_version}")
    
    # 询问新版本号
    new_version = input(f"请输入新版本号 (当前: {current_version}): ").strip()
    if not new_version:
        new_version = current_version
    
    # 确保版本号格式正确
    if new_version and not new_version.startswith('v'):
        new_version = f"v{new_version}"
    
    # 询问发布说明
    release_message = input("请输入发布说明: ").strip()
    if not release_message:
        release_message = "Bug修复和功能改进"
    
    print(f"\n准备发布版本: {new_version}")
    print(f"发布说明: {release_message}")
    
    # 确认发布
    confirm = input("\n确认发布? (y/N): ").strip().lower()
    if confirm != 'y':
        print("发布已取消")
        sys.exit(0)
    
    try:
        # 更新CHANGELOG
        update_changelog(new_version)
        
        # 创建发布包
        zip_file = create_release_zip()
        
        # 创建Git标签
        create_git_tag(new_version, release_message)
        
        # 推送到GitHub
        push_to_github()
        
        print(f"\n✅ 发布完成!")
        print(f"版本: {new_version}")
        print(f"发布包: {zip_file}")
        print(f"GitHub: https://github.com/haodman/comfyui-fast-node/releases/tag/{new_version}")
        
    except Exception as e:
        print(f"❌ 发布失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 