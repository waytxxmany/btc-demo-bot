import math
from dataclasses import dataclass
from datetime import datetime, timezone

from src.errors import ParseError


@dataclass(frozen=True)
class Quote:
    symbol: str
    price: float
    ts: datetime


def parse_quote(data) -> Quote:
    return _parse(data)


def _parse(data) -> Quote:
    if not isinstance(data, dict) or not data:
        raise ParseError("пустой ответ или не словарь")

    for field in ("symbol", "lastPrice", "closeTime"):
        if field not in data:
            raise ParseError(f"нет поля {field}")

    symbol = data["symbol"]
    if not isinstance(symbol, str) or not symbol:
        raise ParseError("symbol должен быть непустой строкой")

    try:
        price = float(data["lastPrice"])
    except (TypeError, ValueError):
        raise ParseError(f"цена не число: {data['lastPrice']!r}")
    if not math.isfinite(price) or price <= 0:
        raise ParseError(f"цена должна быть больше нуля: {price}")

    close_time = data["closeTime"]
    if isinstance(close_time, bool) or not isinstance(close_time, int) or close_time <= 0:
        raise ParseError(f"неверное время: {close_time!r}")
    try:
        ts = datetime.fromtimestamp(close_time / 1000, tz=timezone.utc)
    except (OverflowError, OSError, ValueError):
        raise ParseError(f"время вне допустимого диапазона: {close_time!r}")

    return Quote(symbol=symbol, price=price, ts=ts)
