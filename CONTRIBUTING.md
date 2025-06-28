# 贡献指南

感谢您对ComfyUI FastNode插件的关注！我们欢迎所有形式的贡献。

## 如何贡献

### 报告Bug
如果您发现了一个bug，请使用[bug报告模板](.github/ISSUE_TEMPLATE/bug_report.md)创建一个issue。

### 请求新功能
如果您想要一个新功能，请使用[功能请求模板](.github/ISSUE_TEMPLATE/feature_request.md)创建一个issue。

### 提交代码
1. Fork这个仓库
2. 创建一个功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个Pull Request

## 开发环境设置

### 前提条件
- Python 3.8+
- ComfyUI
- Git

### 设置步骤
1. Fork并克隆仓库
```bash
git clone https://github.com/haodman/comfyui-fast-node.git
cd comfyui-fast-node
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 将插件链接到ComfyUI
```bash
# 在ComfyUI的custom_nodes目录中创建符号链接
ln -s /path/to/your/comfyui-fast-node /path/to/ComfyUI/custom_nodes/
```

## 代码规范

### Python代码风格
- 遵循PEP 8规范
- 使用4个空格缩进
- 行长度限制在120字符以内
- 使用有意义的变量和函数名

### 节点开发规范
- 每个节点类都应该有清晰的文档字符串
- 输入参数应该有类型提示
- 错误处理应该友好且信息丰富
- 节点名称应该清晰描述功能

### 提交信息规范
使用清晰的提交信息：
- `feat:` 新功能
- `fix:` Bug修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

## 测试

### 运行测试
在提交代码之前，请确保：
1. 所有现有功能正常工作
2. 新功能经过充分测试
3. 没有引入新的错误

### 测试清单
- [ ] 节点在ComfyUI中正常加载
- [ ] 所有输入参数正常工作
- [ ] 错误处理正确
- [ ] 输出格式符合预期

## 文档

### 更新文档
如果您添加了新功能或修改了现有功能，请：
1. 更新README.md
2. 更新USAGE.md（如果适用）
3. 添加代码注释

### 文档规范
- 使用清晰简洁的语言
- 提供使用示例
- 包含截图（如果适用）
- 保持文档与代码同步

## 发布流程

### 版本号规范
我们使用语义化版本控制：
- 主版本号：不兼容的API修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

### 发布步骤
1. 更新版本号
2. 更新CHANGELOG.md
3. 创建Git标签
4. 发布到GitHub

## 行为准则

### 我们的承诺
为了营造一个开放和友好的环境，我们承诺：
- 尊重所有贡献者
- 欢迎建设性的反馈
- 专注于问题本身
- 展示对其他社区成员的同情

### 我们的标准
不可接受的行为包括：
- 使用性暗示的语言或图像
- 挑衅、侮辱/贬损的评论
- 人身攻击
- 骚扰行为

## 联系方式

如果您有任何问题或建议，请：
- 创建GitHub Issue
- 发送邮件到项目维护者
- 参与GitHub Discussions

感谢您的贡献！ 