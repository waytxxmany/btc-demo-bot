class FetchError(Exception):
    pass


class ParseError(Exception):
    pass


class NotEnoughDataError(Exception):
    def __init__(self, needed: int, have: int):
        self.needed = needed
        self.have = have
        super().__init__(f"Нужно минимум {needed} котировок, сейчас {have}")
