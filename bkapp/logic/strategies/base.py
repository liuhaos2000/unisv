# backtest/strategies/base.py
class StrategyBase:
    value = '00'
    name = 'base'
    params = []
    level = 'normal'  # 'normal' 或 'vip'

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def generate_signals(self, history):
        raise NotImplementedError

    def backtest(self, history):
        raise NotImplementedError
