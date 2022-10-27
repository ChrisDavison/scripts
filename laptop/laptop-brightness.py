#!/usr/bin/env python
import os
import argparse
import re
from dataclasses import dataclass
from pathlib import Path
import subprocess


DEVICE_DIR = "/sys/class/backlight/intel_backlight"

@dataclass
class Volume:
    sink: str

    def __init__(self) -> None:
        start = False
        active_out = [line for line in
                      subprocess.run(['pactl', 'list', 'short', 'sinks'], capture_output = True).stdout
                      if 'RUNNING' in line and not 'Pulse' in line]
        if not active_out:
            raise Exception("NO SINKS")
        active_out = active_out[0][2]
        for line in subprocess.run(['pactl','list','sinks'], capture_output=True).stdout:
            if 'Name ' + active_out in line:
                start = True
            if start and 'Volume' in line and not 'Base' in line:
                # regex for number before dB
                break

    def change(self, delta) -> None:
        subprocess.run('pactl set-sink-volume {} {}dB'.format(self.sink, delta))

    def mute(self) -> None:
        subprocess.Run('pactl set-sink-volume {} 0dB'.format(self.sink))

    def increase(self, delta) -> None:
        self.change('+' + delta)

    def decrease(self, delta) -> None:
        self.change('-' + delta)


@dataclass
class Brightness:
    current: int
    max_brightness: int
    step: int

    def __init__(self):
        _devd = Path(DEVICE_DIR)
        self.current = int((_devd / "brightness").read_text())
        self.max_brightness = int((_devd / "max_brightness").read_text())
        self.step = int(self.max_brightness / 20)
        return self


    def show_current_value(self):
        pct = self.current / self.max_brightness * 100
        print(f"{self.current:.0f}/{self.max_brightness:.0f} ({pct:.0f}%)")

    def increase(self):
        self.current += self.step


    def decrease(self):
        self.current -= self.step


    def set(self, percent):
        if percent < 0:
            return
        elif percent > 1: # percent 0..100
            self.current = self.max_brightness * percent / 100
        else: # percent 0..1
            self.current = self.max_brightness * percent


    def check_limits_or_saturate(self):
        if self.current > self.max_brightness:
            self.current = self.max_brightness
        if self.current < 0:
            self.current = 0

    def write(self):
        self.check_limits_or_saturate()
        (Path(DEVICE_DIR) / "brightness").write_text(self.current)


Volume()
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     commands = parser.add_subparsers(dest='command')
#     parser_up = commands.add_parser('up')
#     parser_down = commands.add_parser('down')
#     parser_show = commands.add_parser('show')
#     parser_set = commands.add_parser('set')
#     parser_set.add_argument("percent", type=int)

#     kwargs = vars(parser.parse_args())

#     try:
#         brightness = Brightness()

#         command = kwargs["command"]
#         if command == "up":
#             brightness.increase()
#             brightness.write()
#         elif command == "down":
#             brightness.decrease()
#             brightness.write()
#         elif command == "set":
#             brightness.set(kwargs["percent"])
#             brightness.write()
#         else:
#             brightness.show_current_value()
#     except Exception as E:
#         print(E)

