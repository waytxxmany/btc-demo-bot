import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from src import storage
from src.config import Settings, load_settings
from src.errors import NotEnoughDataError
from src.formatting import (
    format_history,
    format_ma,
    format_not_enough_data,
    format_price,
    format_rsi,
    format_signal,
)
from src.indicators import rsi, sma
from src.signals import get_signal
from src.updater import start_scheduler


HISTORY_LIMIT = 10
INDICATOR_QUOTES_LIMIT = 500


def load_prices(settings: Settings) -> list[float]:
    quotes = storage.get_history(settings.symbol, INDICATOR_QUOTES_LIMIT, settings.db_path)
    return [q.price for q in reversed(quotes)]


def build_dispatcher(settings: Settings) -> Dispatcher:
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        await message.answer(
            "Привет! Я показываю котировки BTC.\n"
            "/price - последняя цена\n"
            "/history - последние 10 записей\n"
            "/rsi - значение RSI\n"
            "/ma - значение скользящей средней MA\n"
            "/signal - сигнал на покупку или продажу"
        )

    @dp.message(Command("price"))
    async def cmd_price(message: Message):
        quote = await asyncio.to_thread(storage.get_latest, settings.symbol, settings.db_path)
        await message.answer(format_price(quote))

    @dp.message(Command("history"))
    async def cmd_history(message: Message):
        quotes = await asyncio.to_thread(
            storage.get_history, settings.symbol, HISTORY_LIMIT, settings.db_path
        )
        await message.answer(format_history(quotes))

    @dp.message(Command("rsi"))
    async def cmd_rsi(message: Message):
        prices = await asyncio.to_thread(load_prices, settings)
        try:
            value = rsi(prices, settings.rsi_period)
        except NotEnoughDataError as e:
            await message.answer(format_not_enough_data(e))
            return
        await message.answer(format_rsi(value, settings.rsi_period))

    @dp.message(Command("ma"))
    async def cmd_ma(message: Message):
        prices = await asyncio.to_thread(load_prices, settings)
        try:
            value = sma(prices, settings.ma_period)
        except NotEnoughDataError as e:
            await message.answer(format_not_enough_data(e))
            return
        await message.answer(format_ma(value, settings.ma_period))

    @dp.message(Command("signal"))
    async def cmd_signal(message: Message):
        prices = await asyncio.to_thread(load_prices, settings)
        try:
            signal, value = get_signal(prices, settings.rsi_period)
        except NotEnoughDataError as e:
            await message.answer(format_not_enough_data(e))
            return
        await message.answer(format_signal(signal, value))

    return dp


async def run_bot(settings: Settings) -> None:
    bot = Bot(token=settings.bot_token)
    dp = build_dispatcher(settings)
    await dp.start_polling(bot)


def main() -> None:
    settings = load_settings()
    if not settings.bot_token:
        raise SystemExit("BOT_TOKEN не задан. Впиши токен от @BotFather в файл .env")

    scheduler = start_scheduler(settings)
    try:
        asyncio.run(run_bot(settings))
    except KeyboardInterrupt:
        pass
    finally:
        scheduler.shutdown(wait=False)


if __name__ == "__main__":
    main()
