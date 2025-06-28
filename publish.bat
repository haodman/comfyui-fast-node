@echo off
echo ========================================
echo ComfyUI FastNode Plugin 发布脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查Git是否安装
git --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Git，请先安装Git
    pause
    exit /b 1
)

echo 正在运行发布脚本...
python scripts/release.py

echo.
echo 发布完成！按任意键退出...
pause >nul 