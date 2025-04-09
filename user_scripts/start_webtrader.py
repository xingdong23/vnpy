import os
import sys
import subprocess
import shutil
from pathlib import Path

# 复制配置文件
config_src = Path("user_scripts/web_trader_setting.json")
config_dst = Path.home() / ".vntrader" / "web_trader_setting.json"

# 创建目录
os.makedirs(config_dst.parent, exist_ok=True)

# 复制文件
shutil.copy(config_src, config_dst)
print(f"配置文件已复制到 {config_dst}")

# 启动 RPC 服务
print("正在启动 RPC 服务...")
rpc_cmd = ["/opt/anaconda3/envs/vnpy/bin/python", "-m", "vnpy_rpcservice.run_service"]
rpc_process = subprocess.Popen(rpc_cmd)

# 等待 RPC 服务启动
import time
time.sleep(2)

# 启动 WebTrader
print("正在启动 WebTrader...")
web_cmd = ["/opt/anaconda3/envs/vnpy/bin/python", "-m", "vnpy_webtrader.run_server"]

print(f"WebTrader 将启动，请访问 http://127.0.0.1:8099")
print(f"用户名: admin, 密码: admin")

# 启动 WebTrader
web_process = subprocess.Popen(web_cmd)

print("按 Ctrl+C 退出...")

try:
    # 保持主程序运行
    web_process.wait()
except KeyboardInterrupt:
    # 捕获 Ctrl+C
    web_process.terminate()
    rpc_process.terminate()
    print("已终止 WebTrader 和 RPC 服务")
