import dateutil.parser
import datetime

class TimeRange:
    """Simple helper class to generate a range of times."""
    def __init__(self, start, stop):
        self.start = dateutil.parser.parse(start) if type(start) == str else start
        self.end = dateutil.parser.parse(stop) if type(stop) == str else stop

    def days(self):
        return self.__custom_range(datetime.timedelta(days=1))

    def hours(self):
        return self.__custom_range(datetime.timedelta(hours=1))

    def minutes(self):
        return self.__custom_range(datetime.timedelta(minutes=1))

    def seconds(self):
        return self.__custom_range(datetime.timedelta(seconds=1))

    def __custom_range(self, step):
        start = self.start
        while start < self.end:
            yield start
            start += step
