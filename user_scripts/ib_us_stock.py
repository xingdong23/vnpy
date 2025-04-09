from datetime import datetime
from time import sleep

from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.constant import Exchange
from vnpy_ib import IbGateway


# 创建事件引擎和主引擎
event_engine = EventEngine()
main_engine = MainEngine(event_engine)

# 添加IB接口
main_engine.add_gateway(IbGateway)

# IB接口设置
ib_setting = {
    "TWS地址": "127.0.0.1",
    "TWS端口": 7496,
    "客户号": 1,  # 通常为1，除非您有多个账户
    "交易账户": "",  # 留空使用默认账户
}

# 连接到IB
main_engine.connect(ib_setting, "IB")
print("正在连接到IB，请等待...")
sleep(10)  # 等待连接建立

# 订阅美股行情
symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
for symbol in symbols:
    vt_symbol = f"{symbol}.SMART"  # SMART是IB的智能路由
    main_engine.subscribe(vt_symbol, "IB")
    print(f"已订阅 {symbol} 行情")

# 保持程序运行
try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    print("正在关闭连接...")
    main_engine.close()
    print("程序已退出")
