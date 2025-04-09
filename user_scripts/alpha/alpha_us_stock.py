from datetime import datetime
import os

from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.constant import Interval
from vnpy.alpha import AlphaLab
from vnpy.alpha.dataset import AlphaDataset, process_drop_na, process_cs_norm
from vnpy.alpha.model.models.lasso_model import LassoModel
from vnpy.alpha.strategy.backtesting import BacktestingEngine
from vnpy_ib import IbGateway


# 创建数据目录
lab_path = "./alpha_lab"
os.makedirs(lab_path, exist_ok=True)

# 创建Alpha实验室
lab = AlphaLab(lab_path)

# 设置美股股票池
us_stocks = ["AAPL.SMART", "MSFT.SMART", "GOOGL.SMART", "AMZN.SMART", "TSLA.SMART"]

# 下载历史数据（实际使用时需要先获取数据）
# 这里仅作为示例，实际运行前需要先获取数据
def download_data():
    # 创建事件引擎和主引擎
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    
    # 添加IB接口
    main_engine.add_gateway(IbGateway)
    
    # IB接口设置
    ib_setting = {
        "TWS地址": "127.0.0.1",
        "TWS端口": 7496,
        "客户号": 1,
        "交易账户": "",
    }
    
    # 连接到IB
    main_engine.connect(ib_setting, "IB")
    
    # 下载历史数据
    for vt_symbol in us_stocks:
        # 下载日线数据
        main_engine.download_data(
            vt_symbol=vt_symbol,
            interval=Interval.DAILY,
            start=datetime(2020, 1, 1),
            gateway_name="IB"
        )
    
    # 关闭连接
    main_engine.close()

# 创建Alpha数据集
def create_dataset():
    # 创建数据集
    df = lab.load_bar_data(
        vt_symbols=us_stocks,
        interval=Interval.DAILY,
        start=datetime(2020, 1, 1),
        end=datetime.now()
    )
    
    # 定义训练、验证和测试时间段
    train_period = ("2020-01-01", "2021-12-31")
    valid_period = ("2022-01-01", "2022-12-31")
    test_period = ("2023-01-01", "2023-12-31")
    
    # 创建数据集
    dataset = AlphaDataset(df, train_period, valid_period, test_period)
    
    # 添加特征
    # 动量因子
    dataset.add_feature("mom_5", "close.pct_change(5)")
    dataset.add_feature("mom_10", "close.pct_change(10)")
    dataset.add_feature("mom_20", "close.pct_change(20)")
    
    # 波动率因子
    dataset.add_feature("vol_5", "close.pct_change().rolling(5).std()")
    dataset.add_feature("vol_10", "close.pct_change().rolling(10).std()")
    dataset.add_feature("vol_20", "close.pct_change().rolling(20).std()")
    
    # 设置标签（5日收益率）
    dataset.set_label("close.pct_change(5).shift(-5)")
    
    # 添加数据处理器
    dataset.add_processor("infer", process_drop_na)
    dataset.add_processor("infer", process_cs_norm)
    dataset.add_processor("learn", process_drop_na)
    dataset.add_processor("learn", process_cs_norm)
    
    # 准备数据
    dataset.prepare_data()
    
    return dataset

# 训练模型
def train_model(dataset):
    # 创建Lasso模型
    model = LassoModel()
    
    # 训练模型
    model.fit(dataset)
    
    # 保存模型
    lab.save_model(model, "us_stock_lasso")
    
    return model

# 回测策略
def backtest_strategy(model):
    # 创建回测引擎
    engine = BacktestingEngine(lab)
    
    # 设置回测参数
    engine.set_parameters(
        vt_symbols=us_stocks,
        interval=Interval.DAILY,
        start=datetime(2022, 1, 1),
        end=datetime(2023, 12, 31),
        capital=1_000_000,
        risk_free=0.02,
        annual_days=252
    )
    
    # 生成信号
    signal = model.predict(dataset, Segment.TEST)
    engine.set_signal(signal)
    
    # 运行回测
    engine.run_backtesting()
    
    # 计算结果
    engine.calculate_result()
    engine.calculate_statistics()
    
    # 显示结果
    engine.show_chart()

# 主程序
if __name__ == "__main__":
    # 下载数据（实际使用时取消注释）
    # download_data()
    
    # 创建数据集
    dataset = create_dataset()
    
    # 训练模型
    model = train_model(dataset)
    
    # 回测策略
    backtest_strategy(model)
