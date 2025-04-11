import os
import shutil

# 基本目录路径
base_dir = "/Users/chengzheng/workspace/trade/simpletrade"

# 创建主目录
os.makedirs(base_dir, exist_ok=True)

# 创建子目录
subdirs = [
    "simpletrade",
    "simpletrade/core",
    "simpletrade/api",
    "simpletrade/models",
    "simpletrade/utils",
    "docs",
    "docs/design",
    "docs/requirements",
    "tests",
    "scripts",
    "ui",
    "ui/wireframes",
    "ai_context"
]

for subdir in subdirs:
    os.makedirs(os.path.join(base_dir, subdir), exist_ok=True)

# 创建基本文件
files = {
    "README.md": "# SimpleTrade\n\n简单易用的个人量化交易平台\n",
    "setup.py": """from setuptools import setup, find_packages

setup(
    name="simpletrade",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # 依赖项将在后续添加
    ],
)
""",
    "simpletrade/__init__.py": "# SimpleTrade package\n",
    "simpletrade/core/__init__.py": "# Core module\n",
    "simpletrade/api/__init__.py": "# API module\n",
    "simpletrade/models/__init__.py": "# Data models\n",
    "simpletrade/utils/__init__.py": "# Utility functions\n",
}

for file_path, content in files.items():
    with open(os.path.join(base_dir, file_path), 'w') as f:
        f.write(content)

# 复制AI上下文文件
ai_context_src = "/Users/chengzheng/workspace/trade/vnpy/user_scripts/simpletrade/ai_context"
ai_context_dst = os.path.join(base_dir, "ai_context")

if os.path.exists(ai_context_src):
    # 复制文件
    for filename in ["PROJECT_STATUS.md", "CURRENT_FOCUS.md", "DECISIONS_LOG.md", "AI_COLLABORATION_GUIDE.md"]:
        src_file = os.path.join(ai_context_src, filename)
        dst_file = os.path.join(ai_context_dst, filename)
        if os.path.exists(src_file):
            shutil.copy2(src_file, dst_file)
            print(f"Copied {filename} to new project")

# 复制文档文件
docs_src = "/Users/chengzheng/workspace/trade/vnpy/user_scripts/simpletrade/doc"
docs_dst = os.path.join(base_dir, "docs")

if os.path.exists(docs_src):
    for filename in os.listdir(docs_src):
        src_file = os.path.join(docs_src, filename)
        if os.path.isfile(src_file):
            dst_file = os.path.join(docs_dst, filename)
            shutil.copy2(src_file, dst_file)
            print(f"Copied document {filename} to new project")

# 复制UI文件
ui_src = "/Users/chengzheng/workspace/trade/vnpy/user_scripts/simpletrade/ui"
ui_dst = os.path.join(base_dir, "ui")

if os.path.exists(ui_src):
    for item in os.listdir(ui_src):
        src_item = os.path.join(ui_src, item)
        dst_item = os.path.join(ui_dst, item)
        if os.path.isfile(src_item):
            shutil.copy2(src_item, dst_item)
            print(f"Copied UI file {item} to new project")
        elif os.path.isdir(src_item):
            shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
            print(f"Copied UI directory {item} to new project")

print("Project structure created successfully!")
