# VeighNa (vnpy) 用户脚本

本目录包含用户自定义的 VeighNa (vnpy) 脚本和文档，与源码和示例目录分开管理。

## 文件说明

### 文档

- **vnpy_installation_guide.md**: VeighNa 安装指南，记录了完整的安装过程、安装的组件以及常见问题的解决方案。

### 交易脚本

- **ib_us_stock.py**: 使用 IB 接口连接盈透证券并获取美股行情数据的示例脚本。
  - 功能：连接 IB 接口，订阅美股行情，实时接收行情数据。
  - 使用方法：`python user_scripts/ib_us_stock.py`
  - 注意：需要先启动 TWS 或 IB Gateway 并登录账户。

- **alpha_us_stock.py**: 使用 Alpha 模块开发美股交易策略的示例脚本。
  - 功能：创建 Alpha 数据集，添加动量和波动率因子，训练 Lasso 回归模型，回测策略。
  - 使用方法：`python user_scripts/alpha_us_stock.py`
  - 注意：需要先获取历史数据。

## 使用说明

1. 激活 conda 环境：
   ```bash
   conda activate vnpy
   ```

2. 运行脚本：
   ```bash
   python user_scripts/ib_us_stock.py
   ```

3. 修改脚本：
   根据自己的需求修改脚本，例如更改订阅的股票代码、调整策略参数等。

## 目录结构

```
vnpy/
├── examples/           # 官方示例
├── vnpy/               # 源码
└── user_scripts/       # 用户自定义脚本
    ├── README.md
    ├── vnpy_installation_guide.md
    ├── ib_us_stock.py
    └── alpha_us_stock.py
```
