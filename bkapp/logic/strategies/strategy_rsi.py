from .base import StrategyBase
import pandas as pd

class RsiStrategy(StrategyBase):
    value = '002'
    name = 'RSI'
    params = ['fast', 'slow']
    level = 'normal'
    
    def __init__(self, fast=5, slow=10, **kwargs):
        super().__init__(fast=fast, slow=slow, **kwargs)
        self.fast = int(fast)
        self.slow = int(slow)

    def calc_RSI(self, series, period=14):
        delta = series.diff()
        gain = delta.where(delta > 0, 0).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        RS = gain / loss
        return 100 - (100 / (1 + RS))

    def backtest(self, history):


        df = pd.DataFrame(history, columns=["date", "open", "high", "low", "close"])
        df["date"] = pd.to_datetime(df["date"])
        
        # ----------- 计算 RSI -----------
        df["RSI"] = self.calc_RSI(df["close"], 14)

        # ----------- 回测变量 -----------
        position = 0
        hold_price = 0
        total_profit = 0.0

        history_list = []
        mark_points = []

        # ----------- 回测主循环 -----------
        for i in range(14, len(df)):
            today = df.iloc[i]
            date_str = today["date"].strftime("%Y/%m/%d")
            close = float(today["close"])

            rsi = today["RSI"]

            # ---------- 买入 RSI < 20 ----------
            if position == 0 and rsi < 20:
                position = 1
                hold_price = close

                history_list.append({
                    "buyDate": date_str,
                    "buyPrice": close,
                    "sellDate": "",
                    "sellPrice": "",
                    "warehousePosition": position,
                    "profitMargin": ""
                })

                mark_points.append({
                    "name": "Buy",
                    "coord": [date_str, close],
                    "value": close,
                    "itemStyle": {"color": "#00AA00"},
                    "symbolSize": 40
                })

            # ---------- 卖出 RSI > 80 ----------
            elif position == 1 and rsi > 80:
                sell_price = close
                profit = (sell_price - hold_price) / hold_price
                total_profit += profit

                # 把最近一条没卖出的填上
                for record in reversed(history_list):
                    if record["sellDate"] == "":
                        record["sellDate"] = date_str
                        record["sellPrice"] = sell_price
                        record["warehousePosition"] = 0
                        record["profitMargin"] = format(profit, ".4f")
                        break

                position = 0
                hold_price = 0

                mark_points.append({
                    "name": "Sell",
                    "coord": [date_str, close],
                    "value": close,
                    "itemStyle": {"color": "#FF0000"},
                    "symbolSize": 40
                })

        # ----------- 最后一条加合计记录 -----------
        history_list.append({
            "buyDate": "",
            "buyPrice": "",
            "sellDate": "",
            "sellPrice": "",
            "warehousePosition": position,
            "profitMargin": format(total_profit, ".4f")
        })

        return {
            "code": 0,
            "message": "success",
            "data": {
                "historyList": history_list,
                "markPoint": {"data": mark_points}
            }
        }
