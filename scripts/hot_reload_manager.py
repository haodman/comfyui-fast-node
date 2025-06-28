import os
import sys
import importlib
import time
import threading
from pathlib import Path

class HotReloadManager:
    """热更新管理器，监控文件变化并自动重新加载"""
    
    def __init__(self, module_name, file_path):
        self.module_name = module_name
        self.file_path = Path(file_path)
        self.last_modified = self.file_path.stat().st_mtime
        self.is_monitoring = False
        self.monitor_thread = None
        
    def start_monitoring(self):
        """开始监控文件变化"""
        if self.is_monitoring:
            return
            
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print(f"🔄 开始监控文件: {self.file_path}")
        
    def stop_monitoring(self):
        """停止监控"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        print("⏹️ 停止文件监控")
        
    def _monitor_loop(self):
        """监控循环"""
        while self.is_monitoring:
            try:
                current_modified = self.file_path.stat().st_mtime
                if current_modified > self.last_modified:
                    print(f"📝 检测到文件变化: {self.file_path}")
                    self._reload_module()
                    self.last_modified = current_modified
                time.sleep(1)  # 每秒检查一次
            except Exception as e:
                print(f"❌ 监控错误: {e}")
                time.sleep(5)
                
    def _reload_module(self):
        """重新加载模块"""
        try:
            if self.module_name in sys.modules:
                importlib.reload(sys.modules[self.module_name])
                print(f"✅ 模块 {self.module_name} 重新加载成功")
            else:
                print(f"⚠️ 模块 {self.module_name} 未找到")
        except Exception as e:
            print(f"❌ 重新加载失败: {e}")

# 全局热更新管理器实例
hot_reload_manager = None

def init_hot_reload():
    """初始化热更新管理器"""
    global hot_reload_manager
    current_file = Path(__file__)
    module_name = "custom_naming_saver"
    
    hot_reload_manager = HotReloadManager(module_name, current_file)
    hot_reload_manager.start_monitoring()
    
    return hot_reload_manager

def stop_hot_reload():
    """停止热更新管理器"""
    global hot_reload_manager
    if hot_reload_manager:
        hot_reload_manager.stop_monitoring()

# 自动初始化热更新
if __name__ != "__main__":
    try:
        init_hot_reload()
    except Exception as e:
        print(f"⚠️ 热更新初始化失败: {e}") 