from src.indicators import DEFAULT_RSI_PERIOD, rsi

RSI_BUY_LEVEL = 30
RSI_SELL_LEVEL = 70


def get_signal(prices: list[float], period: int = DEFAULT_RSI_PERIOD) -> tuple[str | None, float]:
    value = rsi(prices, period)
    if value < RSI_BUY_LEVEL:
        return "BUY", value
    if value > RSI_SELL_LEVEL:
        return "SELL", value
    return None, value
