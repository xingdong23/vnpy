import os
import shutil
from pathlib import Path

# 源目录和目标目录
src_base = "/Users/chengzheng/workspace/trade/vnpy/user_scripts/simpletrade"
dst_base = "/Users/chengzheng/workspace/trade/simpletrade"

# 确保目标目录存在
os.makedirs(dst_base, exist_ok=True)

# 需要迁移的目录
dirs_to_migrate = [
    ("doc", "docs"),  # 源目录中的doc迁移到目标目录的docs
    ("ai_context", "ai_context"),
    ("ui", "ui")
]

# 迁移目录
for src_dir, dst_dir in dirs_to_migrate:
    src_path = os.path.join(src_base, src_dir)
    dst_path = os.path.join(dst_base, dst_dir)
    
    # 确保目标目录存在
    os.makedirs(dst_path, exist_ok=True)
    
    # 如果源目录存在，复制所有文件
    if os.path.exists(src_path):
        for item in os.listdir(src_path):
            src_item = os.path.join(src_path, item)
            dst_item = os.path.join(dst_path, item)
            
            if os.path.isfile(src_item):
                shutil.copy2(src_item, dst_item)
                print(f"Copied file: {src_item} -> {dst_item}")
            elif os.path.isdir(src_item):
                if os.path.exists(dst_item):
                    shutil.rmtree(dst_item)
                shutil.copytree(src_item, dst_item)
                print(f"Copied directory: {src_item} -> {dst_item}")

print("Migration completed successfully!")
