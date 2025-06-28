// ComfyUI FastNode插件 - JavaScript支持
import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

// 注册右键菜单项
app.registerExtension({
    name: "comfyui-fast-node",
    async setup() {
        // 添加右键菜单项
        const menuItems = [
            {
                name: "📝 Custom Naming Saver",
                category: "🐙FastNode",
                nodeType: "CustomNamingSaver"
            },
            {
                name: "🎲 Seed To Text",
                category: "🐙FastNode",
                nodeType: "SeedToTextNode"
            },
            {
                name: "🔗 Text Concatenator",
                category: "🐙FastNode",
                nodeType: "TextConcatenatorNode"
            },
            {
                name: "🖼️ Loading Image List",
                category: "🐙FastNode",
                nodeType: "LoadingImageListNode"
            },
            {
                name: "🔢 Int To Float (Simple)",
                category: "🐙FastNode",
                nodeType: "IntToFloatSimpleNode"
            },
            {
                name: "🔢 Float To Int (Simple)",
                category: "🐙FastNode",
                nodeType: "FloatToIntSimpleNode"
            },
            {
                name: "🔤 Int To Text (Simple)",
                category: "🐙FastNode",
                nodeType: "IntToTextSimpleNode"
            },
            {
                name: "🔤 Float To Text (Simple)",
                category: "🐙FastNode",
                nodeType: "FloatToTextSimpleNode"
            },
            {
                name: "📐 Image List Range Node",
                category: "🐙FastNode",
                nodeType: "ImageListRangeNode"
            },
            {
                name: "📄 Loading Text List",
                category: "🐙FastNode",
                nodeType: "LoadingTextListNode"
            }
        ];

        // 为每个菜单项添加右键菜单支持
        menuItems.forEach(item => {
            // 添加到节点创建菜单
            if (app.nodeConstructorMap) {
                app.nodeConstructorMap[item.nodeType] = {
                    category: item.category,
                    name: item.name
                };
            }
        });

        console.log("✅ FastNode菜单已注册");
    }
}); 