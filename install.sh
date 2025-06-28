#!/bin/bash

echo "========================================"
echo "ComfyUI FastNode插件 - Linux/Mac安装脚本"
echo "========================================"
echo

echo "正在检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "正在安装依赖包..."
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "错误：依赖包安装失败"
    exit 1
fi

echo
echo "========================================"
echo "安装完成！"
echo "========================================"
echo
echo "请确保此文件夹已复制到ComfyUI的custom_nodes目录中"
echo "然后重启ComfyUI即可使用"
echo
echo "节点分类：🐙FastNode"
echo 