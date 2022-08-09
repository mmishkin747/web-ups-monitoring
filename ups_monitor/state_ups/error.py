

class StateUpsError(Exception):
    """Базовый класс для других исключений"""
    pass

class ConnectError(StateUpsError):
    pass

class ValueStateError(StateUpsError):
    pass

class NoneValueError(StateUpsError):
    pass