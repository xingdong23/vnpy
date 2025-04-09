import os
import sys
from pathlib import Path

# 获取 vnpy_webtrader 包的路径
import vnpy_webtrader
webtrader_path = Path(vnpy_webtrader.__file__).parent
widget_path = webtrader_path / "ui" / "widget.py"

print(f"正在修复 {widget_path}")

# 读取文件内容
with open(widget_path, "r") as f:
    content = f.read()

# 修复 MergedChannels 问题
if "self.process.setProcessChannelMode(self.process.MergedChannels)" in content:
    # 修改导入语句
    if "from PySide6.QtCore import QProcess" in content:
        content = content.replace(
            "from PySide6.QtCore import QProcess",
            "from PySide6.QtCore import QProcess"
        )
    
    # 替换 MergedChannels
    content = content.replace(
        "self.process.setProcessChannelMode(self.process.MergedChannels)",
        "self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)"
    )

    # 写回文件
    with open(widget_path, "w") as f:
        f.write(content)
    
    print("修复完成！")
else:
    print("文件中没有找到 'self.process.setProcessChannelMode(self.process.MergedChannels)'，可能已经被修复或问题出在其他地方。")
    
    # 打印文件内容中包含 MergedChannels 的行
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "MergedChannels" in line:
            print(f"行 {i+1}: {line}")

print("\n现在您可以重新启动 vnpy 并尝试使用 WebTrader 了。")
