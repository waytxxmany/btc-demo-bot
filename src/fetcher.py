import requests

from src.errors import FetchError
from src.parser import Quote, parse_quote


API_URL = "https://data-api.binance.vision/api/v3/ticker/24hr"
DEFAULT_SYMBOL = "BTCUSDT"
DEFAULT_TIMEOUT = 10


def fetch_raw(symbol: str = DEFAULT_SYMBOL, timeout: float = DEFAULT_TIMEOUT) -> dict:
    try:
        response = requests.get(API_URL, params={"symbol": symbol}, timeout=timeout)
    except requests.Timeout:
        raise FetchError(f"таймаут: Binance не ответил за {timeout} сек")
    except requests.ConnectionError:
        raise FetchError("ошибка соединения с Binance")
    except requests.RequestException as e:
        raise FetchError(f"ошибка запроса: {e}")

    if response.status_code != 200:
        raise FetchError(f"Binance вернул код {response.status_code}")

    try:
        return response.json()
    except ValueError:
        raise FetchError("ответ Binance не является JSON")


def fetch_quote(symbol: str = DEFAULT_SYMBOL, timeout: float = DEFAULT_TIMEOUT) -> Quote:
    return parse_quote(fetch_raw(symbol, timeout))
