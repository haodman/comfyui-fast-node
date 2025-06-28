# ComfyUI FastNode插件 - 维护指南

## 🎯 项目结构说明

```
comfyui-fast-node/
├── __init__.py                 # 插件入口，自动导入nodes包
├── nodes/                      # 所有节点代码
│   ├── __init__.py            # 节点注册中心
│   ├── saver.py               # 保存相关节点
│   ├── loader.py              # 加载相关节点
│   └── converter.py           # 类型转换节点
├── web/js/custom_naming.js    # 前端菜单支持
├── workflows/                 # 工作流文件
├── scripts/                   # 开发脚本
└── 文档文件...
```

## 🛠️ 如何添加新节点

### 步骤1：创建节点类
在 `nodes/` 目录中选择合适的文件添加，或创建新文件：

**在现有文件中添加（推荐）：**
```python
# 在 nodes/converter.py 中添加
class MyNewNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_value": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "my_function"
    CATEGORY = "🐙FastNode/MyCategory"
    
    def my_function(self, input_value):
        return (input_value.upper(),)
```

**创建新文件：**
```python
# 创建 nodes/my_feature.py
class MyFeatureNode:
    # 节点实现...
```

### 步骤2：注册节点
在 `nodes/__init__.py` 中添加：

```python
# 如果创建了新文件，先导入
from .my_feature import *

# 在 NODE_CLASS_MAPPINGS 中添加
NODE_CLASS_MAPPINGS = {
    # ... 现有节点
    "MyNewNode": MyNewNode,
    "MyFeatureNode": MyFeatureNode,
}

# 在 NODE_DISPLAY_NAME_MAPPINGS 中添加
NODE_DISPLAY_NAME_MAPPINGS = {
    # ... 现有节点
    "MyNewNode": "🔧 My New Node",
    "MyFeatureNode": "✨ My Feature Node",
}
```

### 步骤3：添加前端菜单
在 `web/js/custom_naming.js` 中添加：

```javascript
{
    name: "🔧 My New Node",
    category: "🐙FastNode",
    nodeType: "MyNewNode"
},
{
    name: "✨ My Feature Node", 
    category: "🐙FastNode",
    nodeType: "MyFeatureNode"
}
```

## 🔧 如何修改现有节点

### 修改节点功能
1. 找到节点所在的文件（如 `nodes/saver.py`）
2. 修改节点类的实现
3. 重启ComfyUI或使用热更新

### 修改节点参数
```python
@classmethod
def INPUT_TYPES(cls):
    return {
        "required": {
            "new_param": ("STRING", {"default": "新参数"}),
        },
        "optional": {
            "optional_param": ("INT", {"default": 0, "min": 0, "max": 100}),
        }
    }
```

### 修改节点分类
```python
CATEGORY = "🐙FastNode/新分类"
```

## 📁 文件分类指南

### nodes/ 目录
- `saver.py` - 保存、输出相关节点
- `loader.py` - 加载、输入相关节点  
- `converter.py` - 类型转换、数据处理节点
- `new_feature.py` - 新功能节点（按功能命名）

### workflows/ 目录
- `example_workflow.json` - 完整示例工作流
- `dev_workflow.json` - 开发测试工作流
- `feature_demo.json` - 新功能演示工作流

### scripts/ 目录
- `dev_setup.py` - 开发环境设置
- `hot_reload_manager.py` - 热更新管理
- `new_script.py` - 新的辅助脚本

## 🚀 开发工作流

### 1. 环境准备
```bash
# 运行开发环境设置
python scripts/dev_setup.py
```

### 2. 开发流程
1. 启动ComfyUI
2. 加载 `workflows/dev_workflow.json`
3. 启动热更新监控
4. 修改代码
5. 使用热更新节点重新加载
6. 测试功能

### 3. 测试新功能
1. 在ComfyUI中添加新节点
2. 连接输入输出
3. 运行测试
4. 检查结果

## 🔍 常见问题解决

### 节点不显示
1. 检查 `nodes/__init__.py` 中的注册
2. 检查 `web/js/custom_naming.js` 中的菜单项
3. 重启ComfyUI
4. 清除浏览器缓存

### 导入错误
1. 检查文件路径和导入语句
2. 确保所有依赖都已安装
3. 检查Python语法错误

### 热更新不工作
1. 检查热更新监控是否启动
2. 手动触发重新加载
3. 重启ComfyUI

## 📝 代码规范

### 节点命名
- 类名：`PascalCase` + `Node`（如 `CustomNamingSaverNode`）
- 文件名：`snake_case.py`（如 `custom_naming_saver.py`）
- 显示名：使用emoji + 描述（如 `📝 Custom Naming Saver`）

### 分类命名
- 主分类：`🐙FastNode`
- 子分类：`🐙FastNode/功能分类`（如 `🐙FastNode/Saver`）

### 注释规范
```python
class MyNode:
    """节点功能描述"""
    
    @classmethod
    def INPUT_TYPES(cls):
        """定义输入参数"""
        return {...}
    
    def my_function(self, param):
        """函数功能描述"""
        # 实现代码
        return result
```

## 🎯 发布准备

### 1. 测试检查
- [ ] 所有节点功能正常
- [ ] 工作流示例可用
- [ ] 文档更新完整
- [ ] 安装脚本正常

### 2. 版本更新
- 更新 `README.md` 中的版本信息
- 更新 `requirements.txt` 中的依赖版本
- 创建新的工作流示例

### 3. 发布文件
- 压缩整个项目文件夹
- 上传到GitHub
- 更新发布说明

## 💡 维护技巧

1. **模块化设计**：每个功能一个文件，便于维护
2. **统一注册**：所有节点在 `nodes/__init__.py` 中统一管理
3. **文档同步**：代码修改后及时更新文档
4. **版本控制**：使用Git管理代码版本
5. **测试驱动**：新功能先写测试，再写实现

## 🆘 获取帮助

- 查看 `README.md` 了解基本功能
- 查看 `USAGE.md` 了解使用示例
- 查看 `workflows/` 目录中的工作流示例
- 使用热更新功能快速调试
- 在GitHub上提交Issue获取帮助 