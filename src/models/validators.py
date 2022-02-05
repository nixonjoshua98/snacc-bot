import datetime as dt


class SecondsTimeDelta(dt.timedelta):

    @classmethod
    def __get_validators__(cls):
        yield lambda v: dt.timedelta(seconds=v)
