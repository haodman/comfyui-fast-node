# ComfyUI FastNode插件

一个功能强大的ComfyUI插件，提供自定义图片命名保存、批量处理、类型转换和文件加载功能。

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![ComfyUI](https://img.shields.io/badge/ComfyUI-Compatible-green.svg)](https://github.com/comfyanonymous/ComfyUI)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 主要功能

### 📝 图片保存与命名
- **自定义命名格式**：支持 `00001_input.png`、`00001_output.png` 等格式
- **多种图片类型**：支持输入图片、输出图片、Canny边缘图、深度图、OpenPose图片
- **提示词保存**：自动保存正面和负面提示词为文本文件
- **元数据记录**：生成JSON格式的元数据文件，记录保存信息
- **批量处理**：支持批量图片的自动命名和保存

### 🔄 类型转换工具
- **Seed转文本**：专门处理seed值的格式化
- **文本拼接**：将多个文本片段拼接成完整文本
- **简单类型转换**：Int/Float/Text之间的快速转换

### 📁 文件加载工具
- **批量图片加载**：从文件夹批量加载图片
- **图片区间加载**：支持指定起点和终点的图片加载
- **批量文本加载**：从文件夹批量加载txt/json/csv文件

## 📦 安装方法

### 方法一：手动安装
1. 下载此仓库到本地
2. 将整个文件夹复制到ComfyUI的 `custom_nodes` 目录中
3. 重启ComfyUI
4. 在节点列表中找到 `🐙FastNode` 分类下的节点

### 方法二：使用Git克隆
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/你的用户名/comfyui-fast-node.git
```

### 方法三：使用安装脚本
```bash
# Windows
install.bat

# Linux/Mac
./install.sh
```

## 🎯 节点说明

### 📝 自定义命名保存器 (CustomNamingSaver)
**功能**：保存图片并生成自定义命名的文件

**输入参数：**
- `output_image` (必需): 要保存的主图片
- `output_dir` (必需): 输出目录路径
- `start_index` (必需): 起始索引号，如 "1"

**可选参数：**
- `input_image`: 输入图片
- `canny_image`: Canny边缘检测图片
- `depth_image`: 深度图
- `openpose_image`: OpenPose图片
- `prompt_text`: 正面提示词
- `negative_prompt`: 负面提示词
- `save_input`: 是否保存输入图片 (默认: True)
- `save_canny`: 是否保存Canny图片 (默认: False)
- `save_depth`: 是否保存深度图 (默认: False)
- `save_openpose`: 是否保存OpenPose图片 (默认: False)
- `save_prompt`: 是否保存提示词 (默认: True)
- `save_metadata`: 是否保存元数据 (默认: True)

**输出：**
- 保存的图片
- 保存文件列表的文本摘要

### 🎲 Seed转文本 (SeedToTextNode)
**功能**：将seed值转换为文本格式

**输入参数：**
- `seed` (必需): seed值
- `format` (必需): 格式类型 ["纯数字", "无前缀"]
- `padding` (必需): 填充位数 (1-10)

**输出：**
- 格式化后的seed文本

**使用示例：**
- seed=12345, format="纯数字", padding=5 → "12345"
- seed=12345, format="无前缀", padding=5 → "12345"

### 🔗 文本拼接器 (TextConcatenatorNode)
**功能**：将多个文本片段拼接成一个完整的文本

**输入参数：**
- `separator` (必需): 分隔符
- `text1` - `text5` (可选): 要拼接的文本片段

**输出：**
- 拼接后的完整文本

### 🖼️ 批量图片加载 (LoadingImageListNode)
**功能**：从文件夹批量加载图片

**输入参数：**
- `folder_path` (必需): 图片文件夹路径
- `start` (可选): 起始索引 (默认: 0)
- `sort_by` (可选): 排序方式 ["name", "mtime"] (默认: "name")
- `reverse` (可选): 是否反向排序 (默认: False)
- `max_count` (可选): 最大加载数量 (默认: 0，表示全部)

### 📐 图片区间加载 (ImageListRangeNode)
**功能**：加载指定区间的图片

**输入参数：**
- `folder_path` (必需): 图片文件夹路径
- `start` (必需): 起始索引
- `end` (必需): 结束索引
- `sort_by` (可选): 排序方式 ["name", "mtime"] (默认: "name")
- `reverse` (可选): 是否反向排序 (默认: False)

### 📄 批量文本加载 (LoadingTextListNode)
**功能**：从文件夹批量加载文本文件

**输入参数：**
- `folder_path` (必需): 文本文件夹路径
- `start` (可选): 起始索引 (默认: 0)
- `sort_by` (可选): 排序方式 ["name", "mtime"] (默认: "name")
- `reverse` (可选): 是否反向排序 (默认: False)
- `max_count` (可选): 最大加载数量 (默认: 0，表示全部)

### 🔢 简单类型转换节点
- **Int To Float (Simple)**: 整数转浮点数
- **Float To Int (Simple)**: 浮点数转整数
- **Int To Text (Simple)**: 整数转文本
- **Float To Text (Simple)**: 浮点数转文本（支持小数位数设置）

## 📁 项目结构

```
comfyui-fast-node/
├── __init__.py                 # 插件入口文件
├── custom_naming_saver.py      # 主要节点实现
├── web/                       # Web界面文件
│   └── js/
│       └── custom_naming.js   # JavaScript支持
├── workflows/                 # 工作流示例
│   ├── example_workflow.json  # 示例工作流
│   └── dev_workflow.json      # 开发工作流
├── scripts/                   # 辅助脚本
│   ├── dev_setup.py          # 开发环境设置脚本
│   └── hot_reload_manager.py # 热更新管理器
├── requirements.txt           # 依赖包
├── README.md                  # 项目说明
├── USAGE.md                   # 使用示例
├── MAINTENANCE.md             # 维护指南
├── install.bat               # Windows安装脚本
├── install.sh                # Linux/Mac安装脚本
└── .gitignore                # Git忽略文件
```

## 🎨 使用示例

### 基本图片保存
```
KSampler → CustomNamingSaver
```

### 使用Seed值命名
```
KSampler → SeedToTextNode → TextConcatenatorNode → CustomNamingSaver
```

### 批量图片处理
```
LoadingImageListNode → 处理节点 → CustomNamingSaver
```

更多使用示例请查看 [USAGE.md](USAGE.md)

## 📋 依赖要求

- Python 3.8+
- ComfyUI
- Pillow >= 9.0.0
- torch >= 1.9.0
- numpy >= 1.21.0

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢ComfyUI社区的支持和贡献
- 感谢所有使用和反馈的用户

## 📞 联系方式

- GitHub Issues: [提交问题](https://github.com/你的用户名/comfyui-fast-node/issues)
- 讨论区: [GitHub Discussions](https://github.com/你的用户名/comfyui-fast-node/discussions)

---

⭐ 如果这个项目对你有帮助，请给它一个星标！ 