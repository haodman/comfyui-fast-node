@echo off
echo ========================================
echo ComfyUI FastNode插件 - Windows安装脚本
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo 正在安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误：依赖包安装失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 请确保此文件夹已复制到ComfyUI的custom_nodes目录中
echo 然后重启ComfyUI即可使用
echo.
echo 节点分类：🐙FastNode
echo.
pause 