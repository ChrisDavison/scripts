#!/usr/bin/env python
import os
import argparse
from dataclasses import dataclass
from pathlib import Path


DEVICE_DIR = "/sys/class/backlight/intel_backlight"


@dataclass
class Brightness:
    current: int
    bmax: int
    step: int

    def __init__(self):
        _devd = Path(DEVICE_DIR)
        current = int((_devd / "brightness").read_text())
        bmax = int((_devd / "max_brightness").read_text())
        step = int(bmax / 20)
        return self


    def show_current_value(self):
        pct = self.current / self.bmax * 100
        print(f"{self.current:.0f}/{self.bmax:.0f} ({pct:.0f}%)")

    def increase(self):
        self.current += self.step


    def decrease(self):
        self.current -= self.step


    def set(self, percent):
        if percent < 0:
            return
        elif percent > 1: # percent 0..100
            self.current = self.bmax * percent / 100
        else: # percent 0..1
            self.current = self.bmax * percent


    def check_limits_or_saturate(self):
        if self.current > self.bmax:
            self.current = self.bmax
        if self.current < 0:
            self.current = 0

    def write(self):
        self.check_limits_or_saturate()
        (Path(DEVICE_DIR) / "brightness").write_text(self.current)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest='command')

    parser_up = commands.add_parser('up')

    parser_down = commands.add_parser('down')
    parser_show = commands.add_parser('show')
    parser_set = commands.add_parser('set')
    parser_set.add_argument("percent", type=int)

    kwargs = vars(parser.parse_args())

    try:
        brightness = Brightness()

        command = kwargs["command"]
        if command == "up":
            brightness.increase()
            brightness.write()
        elif command == "down":
            brightness.decrease()
            brightness.write()
        elif command == "set":
            brightness.set(kwargs["percent"])
            brightness.write()
        else:
            brightness.show_current_value()
    except Exception as E:
        print(E)

