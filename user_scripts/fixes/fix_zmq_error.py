import os
from pathlib import Path

# 获取 vnpy 的 rpc/server.py 文件路径
import vnpy
vnpy_path = Path(vnpy.__file__).parent
server_path = vnpy_path / "rpc" / "server.py"

print(f"正在修复 {server_path}")

# 读取文件内容
with open(server_path, "r") as f:
    content = f.read()

# 修复 unbind 问题
if "self._socket_pub.unbind(str(self._socket_pub.LAST_ENDPOINT))" in content:
    # 添加 try-except 块来捕获 ZMQError
    modified_content = content.replace(
        "    def close(self) -> None:\n        \"\"\"Close the RPC server.\"\"\"\n        self._active = False\n        self._socket_pub.unbind(str(self._socket_pub.LAST_ENDPOINT))\n        self._socket_rep.unbind(str(self._socket_rep.LAST_ENDPOINT))\n        self._socket_pub.close()\n        self._socket_rep.close()\n        self._context.term()",
        """    def close(self) -> None:
        \"\"\"Close the RPC server.\"\"\"
        self._active = False
        
        try:
            self._socket_pub.unbind(str(self._socket_pub.LAST_ENDPOINT))
        except Exception as e:
            print(f"Warning: Failed to unbind publisher socket: {e}")
            
        try:
            self._socket_rep.unbind(str(self._socket_rep.LAST_ENDPOINT))
        except Exception as e:
            print(f"Warning: Failed to unbind reply socket: {e}")
            
        self._socket_pub.close()
        self._socket_rep.close()
        self._context.term()"""
    )

    # 写回文件
    with open(server_path, "w") as f:
        f.write(modified_content)
    
    print("修复完成！")
else:
    print("文件中没有找到需要修复的代码，可能已经被修复或问题出在其他地方。")

print("\n现在您可以重新启动 vnpy，ZMQ 错误应该不会再出现了。")
