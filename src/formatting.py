from src.errors import NotEnoughDataError
from src.parser import Quote

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def _money(value: float) -> str:
    return f"{value:,.2f}".replace(",", " ")


def format_price(quote: Quote | None) -> str:
    if quote is None:
        return "Данных пока нет. Подожди первого обновления."
    return f"{quote.symbol}: {_money(quote.price)}\nВремя котировки: {quote.ts.strftime(TIME_FORMAT)} UTC"


def format_history(quotes: list[Quote]) -> str:
    if not quotes:
        return "история пока пуста"
    return "\n".join(f"{q.ts.strftime(TIME_FORMAT)} UTC: {_money(q.price)}" for q in quotes)


def format_not_enough_data(error: NotEnoughDataError) -> str:
    return f"Недостаточно данных. {error}."


def format_rsi(value: float, period: int) -> str:
    if value < 30:
        state = "перепроданность"
    elif value > 70:
        state = "перекупленность"
    else:
        state = "нейтральная зона"
    return f"RSI({period}): {value:.2f} ({state})"


def format_ma(value: float, period: int) -> str:
    return f"MA({period}): {_money(value)}"


def format_signal(signal: str | None, rsi_value: float) -> str:
    if signal is None:
        return f"Сигнала нет, условия не выполнены. Текущий RSI: {rsi_value:.2f}"
    return f"Сигнал: {signal}. RSI: {rsi_value:.2f}"
