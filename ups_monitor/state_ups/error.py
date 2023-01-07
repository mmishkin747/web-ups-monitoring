

from typing import Any




class StateUpsError(Exception):
    """Базовый класс для других исключений"""
    pass


class ConnectError(StateUpsError):
    pass

class ValueStateError(StateUpsError):
    pass


class ValueDetailError(StateUpsError):
    pass
