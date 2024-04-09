from Functions import update


class DataHandler:
    _data = None
    last_refreshed_time = None

    @classmethod
    def get_data(cls):
        if cls._data is None:
            cls._data = update()
        return cls._data

    @classmethod
    def update_data(cls):
        cls._data = update()

    @classmethod
    def last_refresed_time(cls):
        return cls.last_refreshed_time

    @classmethod
    def set_last_refreshed_time(cls, time):
        cls.last_refreshed_time = time
