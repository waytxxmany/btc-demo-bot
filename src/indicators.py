from src.errors import NotEnoughDataError

DEFAULT_MA_PERIOD = 20
DEFAULT_RSI_PERIOD = 14


def sma(prices: list[float], period: int = DEFAULT_MA_PERIOD) -> float:
    if period <= 0:
        raise ValueError("period должен быть больше нуля")
    if len(prices) < period:
        raise NotEnoughDataError(period, len(prices))
    last = prices[-period:]
    return sum(last) / period


def rsi(prices: list[float], period: int = DEFAULT_RSI_PERIOD) -> float:
    if period <= 0:
        raise ValueError("period должен быть больше нуля")
    needed = period + 1
    if len(prices) < needed:
        raise NotEnoughDataError(needed, len(prices))

    changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [max(c, 0) for c in changes]
    losses = [max(-c, 0) for c in changes]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(changes)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 50.0
    rs = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)
