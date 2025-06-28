# GitHub发布指南

本指南将帮助你将ComfyUI FastNode插件发布到GitHub。

## 📋 发布前检查清单

### 代码质量
- [ ] 所有功能正常工作
- [ ] 没有明显的bug
- [ ] 代码已通过基本测试
- [ ] 错误处理完善

### 文档完整性
- [ ] README.md 已更新
- [ ] USAGE.md 包含使用示例
- [ ] CHANGELOG.md 记录了所有更改
- [ ] 代码注释完整

### 文件完整性
- [ ] 所有必要文件都已包含
- [ ] .gitignore 配置正确
- [ ] requirements.txt 已更新
- [ ] 安装脚本正常工作

## 🚀 发布步骤

### 1. 准备GitHub仓库

#### 创建新仓库
1. 登录GitHub
2. 点击右上角 "+" → "New repository"
3. 仓库名称：`comfyui-fast-node`
4. 描述：`ComfyUI FastNode Plugin - 自定义图片命名保存、批量处理、类型转换工具`
5. 选择 "Public"
6. 不要初始化README（我们已经有自己的）
7. 点击 "Create repository"

#### 配置仓库设置
1. 进入仓库设置 (Settings)
2. 在 "Pages" 中启用GitHub Pages（可选）
3. 在 "Issues" 中启用Issues功能
4. 在 "Discussions" 中启用Discussions功能

### 2. 初始化本地Git仓库

```bash
# 初始化Git仓库
git init

# 添加远程仓库
git remote add origin https://github.com/你的用户名/comfyui-fast-node.git

# 添加所有文件
git add .

# 初始提交
git commit -m "Initial commit: ComfyUI FastNode Plugin v1.0.0"

# 推送到GitHub
git push -u origin main
```

### 3. 使用发布脚本（推荐）

```bash
# 运行发布脚本
python scripts/release.py
```

脚本会自动：
- 询问版本号和发布说明
- 更新CHANGELOG.md
- 创建发布压缩包
- 创建Git标签
- 推送到GitHub

### 4. 手动发布（备选方案）

#### 创建标签
```bash
# 创建带注释的标签
git tag -a v1.0.0 -m "Release v1.0.0: 首次发布"

# 推送标签
git push origin v1.0.0
```

#### 创建GitHub Release
1. 在GitHub仓库页面点击 "Releases"
2. 点击 "Create a new release"
3. 选择刚创建的标签
4. 填写发布标题和说明
5. 上传发布包（可选）
6. 点击 "Publish release"

## 📦 发布包内容

发布包应包含以下文件和目录：

```
comfyui-fast-node-v1.0.0.zip
├── __init__.py                 # 插件入口
├── custom_naming_saver.py      # 主要节点实现
├── requirements.txt            # 依赖包
├── README.md                   # 项目说明
├── USAGE.md                    # 使用指南
├── MAINTENANCE.md              # 维护指南
├── CONTRIBUTING.md             # 贡献指南
├── CHANGELOG.md                # 更新日志
├── LICENSE                     # 许可证
├── install.bat                 # Windows安装脚本
├── install.sh                  # Linux/Mac安装脚本
├── .gitignore                  # Git忽略文件
├── web/                        # Web界面文件
│   └── js/
│       └── custom_naming.js
├── workflows/                  # 工作流示例
│   ├── example_workflow.json
│   └── dev_workflow.json
└── scripts/                    # 辅助脚本
    ├── dev_setup.py
    ├── hot_reload_manager.py
    └── release.py
```

## 🏷️ 版本号规范

使用语义化版本控制：

- **主版本号**：不兼容的API修改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

示例：
- `v1.0.0` - 首次发布
- `v1.1.0` - 添加新功能
- `v1.1.1` - Bug修复
- `v2.0.0` - 重大更新，可能不兼容

## 📝 发布说明模板

```markdown
## 🚀 新版本发布

### 主要更新
- 功能1描述
- 功能2描述
- Bug修复描述

### 安装方法
1. 下载并解压到ComfyUI的custom_nodes目录
2. 重启ComfyUI
3. 在节点列表中找到🐙FastNode分类

### 详细文档
请查看README.md了解详细使用方法

### 兼容性
- ComfyUI版本：>= 1.0.0
- Python版本：>= 3.8
- 操作系统：Windows, macOS, Linux
```

## 🔧 发布后维护

### 监控反馈
- 定期检查GitHub Issues
- 回复用户问题
- 收集功能建议

### 更新文档
- 根据用户反馈更新文档
- 添加常见问题解答
- 更新使用示例

### 版本管理
- 及时修复重要bug
- 定期发布新功能
- 保持向后兼容性

## 🆘 常见问题

### Q: 发布后用户无法找到节点
A: 检查节点注册是否正确，确保`__init__.py`中的映射正确

### Q: 用户报告导入错误
A: 检查依赖包是否正确，更新requirements.txt

### Q: 发布包太大
A: 检查.gitignore配置，确保不包含不必要的文件

### Q: 标签推送失败
A: 确保有推送权限，检查网络连接

## 📞 获取帮助

如果在发布过程中遇到问题：
1. 查看GitHub文档
2. 检查ComfyUI插件开发指南
3. 在GitHub Discussions中寻求帮助
4. 联系项目维护者

---

祝你发布顺利！🎉 