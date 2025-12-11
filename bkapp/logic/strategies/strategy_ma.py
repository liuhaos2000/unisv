from .base import StrategyBase
import pandas as pd

class MovingAverageStrategy(StrategyBase):
    value = '001'
    name = 'MA'
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

        # ------------- 计算指标 ----------------
        df["EMA12"] = df["close"].ewm(span=12).mean()
        df["EMA26"] = df["close"].ewm(span=26).mean()
        df["DIF"] = df["EMA12"] - df["EMA26"]
        df["DEA"] = df["DIF"].ewm(span=9).mean()
        df["MACD"] = (df["DIF"] - df["DEA"]) * 2

        df["RSI"] = self.calc_RSI(df["close"], 14)

        df["MA20"] = df["close"].rolling(20).mean()
        df["MA60"] = df["close"].rolling(60).mean()

        # ------------- 模拟交易 ----------------
        position = 0
        hold_price = 0
        history_list = []
        mark_points = []
        total_profit = 0.0

        for i in range(2, len(df)):
            today = df.iloc[i]
            yesterday = df.iloc[i - 1]

            date_str = today["date"].strftime("%Y/%m/%d")
            close = float(today["close"])

            # 买入信号（全部满足）
            macd_golden = yesterday["DIF"] < yesterday["DEA"] and today["DIF"] > today["DEA"]
            rsi_reversal = yesterday["RSI"] < 30 and today["RSI"] > yesterday["RSI"]
            trend_ok = today["MA20"] > today["MA60"]

            # 加仓信号
            trend_add = (
                position > 0 and
                all(df.iloc[i - j]["close"] > df.iloc[i - j]["MA20"] for j in range(3)) and
                position < 0.8
            )

            # 卖出信号
            macd_dead = yesterday["DIF"] > yesterday["DEA"] and today["DIF"] < today["DEA"]
            rsi_overbought = today["RSI"] > 70
            break_ma20 = today["close"] < today["MA20"]
            trend_break = today["MA20"] < today["MA60"]

            # ---------- 买入 ----------
            if macd_golden and rsi_reversal and trend_ok and position == 0:
                buy_pos = 0.5
                buy_price = close

                position = buy_pos
                hold_price = buy_price

                history_list.append({
                    "buyDate": date_str,
                    "buyPrice": buy_price,
                    "sellDate": "",
                    "sellPrice": "",
                    "warehousePosition": "",
                    "profitMargin": ""
                })

                mark_points.append({
                    "name": "Buy",
                    "coord": [date_str, close],
                    "value": close,
                    "itemStyle": {"color": "#00AA00"},
                    "symbolSize": 40
                })

            # ---------- 加仓 ----------
            elif trend_add:
                buy_pos = 0.3
                buy_price = close

                new_pos = position + buy_pos
                hold_price = (hold_price * position + buy_price * buy_pos) / new_pos
                position = new_pos

                # 加仓 = 新的买入记录（保持交易轨迹清晰）
                history_list.append({
                    "buyDate": date_str,
                    "buyPrice": buy_price,
                    "sellDate": "",
                    "sellPrice": "",
                    "warehousePosition": "",
                    "profitMargin": ""
                })

                mark_points.append({
                    "name": "Add",
                    "coord": [date_str, close],
                    "value": close,
                    "itemStyle": {"color": "#0077FF"},
                    "symbolSize": 30
                })

            # ---------- 卖出 ----------
            elif position > 0 and (macd_dead or rsi_overbought or break_ma20 or trend_break):

                sell_price = close
                profit = (sell_price - hold_price) / hold_price
                total_profit += profit

                # 找到最近一笔未卖出的买入记录（倒序查找）
                for record in reversed(history_list):
                    if record["sellDate"] == "":
                        record["sellDate"] = date_str
                        record["sellPrice"] = sell_price
                        record["warehousePosition"] = position
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

        # ------------ 加入合计记录 ------------
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
