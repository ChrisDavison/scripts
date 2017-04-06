import dateutil.parser
import datetime

class TimeRange:
    """Simple helper class to generate a range of times."""
    def __init__(self, start, stop):
        self.start = dateutil.parser.parse(start) if type(start) == str else start
        self.end = dateutil.parser.parse(stop) if type(stop) == str else stop
        self.backwards = self.end < self.start

    def days(self):
        return self.__custom_range(datetime.timedelta(days=1))

    def hours(self):
        return self.__custom_range(datetime.timedelta(hours=1))

    def minutes(self):
        return self.__custom_range(datetime.timedelta(minutes=1))

    def seconds(self):
        return self.__custom_range(datetime.timedelta(seconds=1))

    def still_in_range(self, current):
        if self.backwards:
            return current > self.end
        return current < self.end

    def __custom_range(self, step):
        start = self.start
        step = -1 * step if self.backwards else step
        while self.still_in_range(start):
            yield start
            start += step
        if start != self.start:
            yield start
