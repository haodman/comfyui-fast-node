# ComfyUI FastNode插件 - 使用示例

## 🎯 快速开始

### 1. 基本图片保存
使用 `📝 Custom Naming Saver` 节点保存图片：

```
KSampler → CustomNamingSaver
```

**设置参数：**
- `output_image`: 连接KSampler的输出
- `output_dir`: "./output"
- `start_index`: "1"

**生成文件：**
```
00001_output.png
00001_metadata.json
```

### 2. 使用Seed值命名
结合Seed值创建自定义文件名：

```
KSampler → SeedToTextNode → TextConcatenatorNode → CustomNamingSaver
```

**工作流：**
1. KSampler的seed输出连接到SeedToTextNode
2. SeedToTextNode输出连接到TextConcatenatorNode
3. TextConcatenatorNode输出作为CustomNamingSaver的base_name

**示例结果：**
- seed=12345 → "landscape_12345_output.png"

### 3. 批量图片处理
使用 `🖼️ Loading Image List` 批量加载图片：

```
LoadingImageListNode → 处理节点 → CustomNamingSaver
```

**设置参数：**
- `folder_path`: "./input_images"
- `sort_by`: "name"
- `max_count`: 10

## 🔄 类型转换示例

### 数值转文本
```
IntToTextSimpleNode → TextConcatenatorNode
```

**示例：**
- 输入：42
- 输出："42"

### 浮点数格式化
```
FloatToTextSimpleNode → TextConcatenatorNode
```

**示例：**
- 输入：3.14159, decimal_places=2
- 输出："3.14"

## 📁 文件加载示例

### 批量加载图片
```
LoadingImageListNode → 处理节点
```

**参数设置：**
- `folder_path`: "./images"
- `start`: 0
- `sort_by`: "name"
- `max_count`: 5

### 区间加载图片
```
ImageListRangeNode → 处理节点
```

**参数设置：**
- `folder_path`: "./images"
- `start`: 10
- `end`: 20

### 批量加载文本
```
LoadingTextListNode → 处理节点
```

**参数设置：**
- `folder_path`: "./prompts"
- `sort_by`: "name"

## 🎨 高级工作流示例

### 完整的工作流
```
CheckpointLoader → CLIPTextEncode → KSampler → VAEDecode → CustomNamingSaver
                                    ↓
                              SeedToTextNode → TextConcatenatorNode
```

**文件输出：**
```
00001_output.png
00001_prompt.txt
00001_negative_prompt.txt
00001_metadata.json
```

### 批量处理工作流
```
LoadingImageListNode → 处理节点 → CustomNamingSaver
                ↓
        LoadingTextListNode → 提示词处理
```

## 💡 使用技巧

1. **文件命名**：使用SeedToTextNode和TextConcatenatorNode创建有意义的文件名
2. **批量处理**：使用LoadingImageListNode和LoadingTextListNode处理大量文件
3. **类型转换**：使用简单类型转换节点处理数据格式
4. **元数据**：启用save_metadata选项记录处理信息

## 🔧 故障排除

### 常见问题
1. **文件未保存**：检查output_dir路径和权限
2. **节点未显示**：重启ComfyUI并清除浏览器缓存
3. **类型错误**：确保输入数据类型正确

### 调试方法
1. 查看ComfyUI控制台输出
2. 检查生成的metadata.json文件
3. 使用热更新功能实时调试 

git clone https://github.com/haodman/comfyui-fast-node.git 