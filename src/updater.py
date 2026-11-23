import time
from datetime import datetime, timezone

from src import storage
from src.config import Settings, load_settings
from src.fetcher import fetch_quote


def update_once(settings: Settings) -> bool:
    try:
        quote = fetch_quote(settings.symbol, settings.request_timeout)
        storage.save_quote(quote, settings.db_path)
        return True
    except Exception:
        return False


def start_scheduler(settings: Settings):
    from apscheduler.schedulers.background import BackgroundScheduler

    storage.init_db(settings.db_path)
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        update_once,
        "interval",
        seconds=settings.update_interval_seconds,
        args=[settings],
        next_run_time=datetime.now(timezone.utc),
        max_instances=1,
        coalesce=True,
    )
    scheduler.start()
    return scheduler


if __name__ == "__main__":
    scheduler = start_scheduler(load_settings())
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()
