from .base import StrategyBase

class MovingAverageStrategy(StrategyBase):
    value = '001'
    name = 'MA'
    params = ['fast', 'slow']
    level = 'normal'
    
    def __init__(self, fast=20, slow=60, **kwargs):
        super().__init__(fast=fast, slow=slow, **kwargs)
        self.fast = int(fast)
        self.slow = int(slow)

    def generate_signals(self, history):
        import pandas as pd

        df = history.copy()
        df['ma_fast'] = df['close'].rolling(self.fast).mean()
        df['ma_slow'] = df['close'].rolling(self.slow).mean()
        df['signal'] = 0
        df.loc[df['ma_fast'] > df['ma_slow'], 'signal'] = 1
        df.loc[df['ma_fast'] <= df['ma_slow'], 'signal'] = 0
        df['position'] = df['signal'].diff().fillna(0)

        signals = []
        for idx, row in df.iterrows():
            if row['position'] == 1:
                signals.append({'index': idx, 'action': 'buy'})
            elif row['position'] == -1:
                signals.append({'index': idx, 'action': 'sell'})
        return signals

    def backtest(self, history):
        from ..engine import simulate_from_signals
        signals = self.generate_signals(history)
        return simulate_from_signals(history, signals)
