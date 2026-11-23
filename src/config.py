import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    symbol: str
    update_interval_seconds: int
    db_path: str
    request_timeout: float
    bot_token: str
    rsi_period: int
    ma_period: int


def _positive_int(name: str, default: int) -> int:
    raw = os.getenv(name, str(default))
    try:
        value = int(raw)
    except ValueError:
        raise ValueError(f"{name} должно быть целым числом, а не {raw!r}")
    if value <= 0:
        raise ValueError(f"{name} должно быть больше нуля")
    return value


def load_settings() -> Settings:
    load_dotenv()

    raw_interval = os.getenv("UPDATE_INTERVAL_SECONDS", "60")
    try:
        interval = int(raw_interval)
    except ValueError:
        raise ValueError(f"UPDATE_INTERVAL_SECONDS должно быть целым числом, а не {raw_interval!r}")
    if interval <= 0:
        raise ValueError("UPDATE_INTERVAL_SECONDS должно быть больше нуля")

    raw_timeout = os.getenv("REQUEST_TIMEOUT", "10")
    try:
        timeout = float(raw_timeout)
    except ValueError:
        raise ValueError(f"REQUEST_TIMEOUT должно быть числом, а не {raw_timeout!r}")

    return Settings(
        symbol=os.getenv("SYMBOL", "BTCUSDT"),
        update_interval_seconds=interval,
        db_path=os.getenv("DB_PATH", "data/quotes.db"),
        request_timeout=timeout,
        bot_token=os.getenv("BOT_TOKEN", ""),
        rsi_period=_positive_int("RSI_PERIOD", 14),
        ma_period=_positive_int("MA_PERIOD", 20),
    )
