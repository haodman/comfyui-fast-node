#!/bin/bash

echo "========================================"
echo "ComfyUI FastNode Plugin 发布脚本"
echo "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo "错误: 未找到Git，请先安装Git"
    exit 1
fi

echo "正在运行发布脚本..."
python3 scripts/release.py

echo
echo "发布完成！" 