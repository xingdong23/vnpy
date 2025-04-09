from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.setting import SETTINGS

# 导入 IB 接口（用于美股交易）
from vnpy_ib import IbGateway

# 导入 RPC 服务模块和 WebTrader 模块
from vnpy_rpcservice import RpcServiceApp
from vnpy_webtrader import WebTraderApp

# 创建事件引擎
event_engine = EventEngine()

# 创建主引擎
main_engine = MainEngine(event_engine)

# 添加交易接口
main_engine.add_gateway(IbGateway)

# 添加 RPC 服务模块
main_engine.add_app(RpcServiceApp)

# 添加 WebTrader 模块
main_engine.add_app(WebTraderApp)

# 启动图形界面
from vnpy.trader.ui import create_qapp, MainWindow

# 创建 Qt 应用
qapp = create_qapp()

# 创建主窗口
main_window = MainWindow(main_engine, event_engine)
main_window.showMaximized()

# 运行 Qt 应用
qapp.exec()

# 关闭主引擎
main_engine.close()
