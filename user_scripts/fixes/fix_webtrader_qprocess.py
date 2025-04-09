import os
from pathlib import Path

# 获取 vnpy_webtrader 包的路径
import vnpy_webtrader
webtrader_path = Path(vnpy_webtrader.__file__).parent
widget_path = webtrader_path / "ui" / "widget.py"

print(f"正在修复 {widget_path}")

# 读取文件内容
with open(widget_path, "r") as f:
    content = f.read()

# 检查是否已经导入了 QProcess
if "from PySide6.QtCore import QProcess" in content:
    # 修改 QProcess 导入
    content = content.replace(
        "from PySide6.QtCore import QProcess",
        "from PySide6.QtCore import QProcess"
    )
    
    # 修复 MergedChannels 问题
    if "self.process.setProcessChannelMode(QProcessModule.ProcessChannelMode.MergedChannels)" in content:
        content = content.replace(
            "self.process.setProcessChannelMode(QProcessModule.ProcessChannelMode.MergedChannels)",
            "self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)"
        )
    elif "self.process.setProcessChannelMode(self.process.MergedChannels)" in content:
        content = content.replace(
            "self.process.setProcessChannelMode(self.process.MergedChannels)",
            "self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)"
        )
    
    # 写回文件
    with open(widget_path, "w") as f:
        f.write(content)
    
    print("修复完成！")
else:
    print("未找到 QProcess 导入语句，请检查文件内容。")
    
    # 打印文件的前几行，帮助诊断问题
    lines = content.split("\n")
    print("\n文件前20行:")
    for i, line in enumerate(lines[:20]):
        print(f"{i+1}: {line}")

print("\n现在您可以重新启动 vnpy 并尝试使用 WebTrader 了。")
