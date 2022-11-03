#!/usr/bin/env python
import os
import argparse
import re
from dataclasses import dataclass
from pathlib import Path
import subprocess

DEVICE_DIR = "/sys/class/backlight/intel_backlight"
RE_SINK = re.compile(r'(?:^|\n)\d+\s+([a-zA-Z0-9._]+)\s+.*RUNNING')
RE_VOL = re.compile(r'Volume.* (-\d+)\.\d+ dB.*')

@dataclass
class Volume:
    sink: str
    volume_db: str

    def __init__(self) -> None:
        start = False
        cmd = subprocess.run(['pactl', 'list', 'short', 'sinks'], capture_output = True)
        m = RE_SINK.search(cmd.stdout.decode())
        if m:
            self.sink = m.group(1)
        else:
            raise Exception("Couldn't get sink. Audio suspended?")

        for line in subprocess.run(['pactl','list','sinks'], capture_output=True).stdout.splitlines():
            line = line.decode()
            if ('Name: ' + self.sink) in line:
                start = True
            m = RE_VOL.search(line)
            if start and m:
                m = RE_VOL.search(line)
                self.volume_db = int(m.group(1))
                break

    def __str__(self) -> str:
        return "Volume of `{}`: {}dB".format(self.sink, self.volume_db)

    def set_volume(self, db):
        subprocess.run(['pactl', 'set-sink-volume', self.sink, '{}dB'.format(db)])

    def change(self, delta) -> None:
        self.set_volume(delta)

    def mute(self) -> None:
        self.set_volume(0)

    def increase(self, delta) -> None:
        self.change('+' + str(delta))

    def decrease(self, delta) -> None:
        self.change('-' + str(delta))


@dataclass
class Brightness:
    current: int
    max_brightness: int
    step: int

    def __init__(self, delta):
        _devd = Path(DEVICE_DIR)
        self.current = int((_devd / "brightness").read_text())
        self.max_brightness = int((_devd / "max_brightness").read_text())
        delta = 100 / delta if delta else 20
        self.step = int(self.max_brightness / delta)


    def __str__(self) -> str:
        pct = self.current / self.max_brightness * 100
        return f"Brightness: {self.current:.0f}/{self.max_brightness:.0f} ({pct:.0f}%)"

    def increase(self):
        self.current += self.step
        self.write()

    def decrease(self):
        self.current -= self.step
        self.write()

    def set(self, percent):
        if percent < 0:
            return
        elif percent > 1: # percent 0..100
            self.current = self.max_brightness * percent / 100
        else: # percent 0..1
            self.current = self.max_brightness * percent
        self.write()


    def check_limits_or_saturate(self):
        if self.current > self.max_brightness:
            self.current = self.max_brightness
        if self.current < 0:
            self.current = 0

    def write(self):
        self.check_limits_or_saturate()
        (Path(DEVICE_DIR) / "brightness").write_text(str(self.current))


def volume_main(action, delta):
    v = Volume()
    if action == 'up':
        v.increase(delta)
    elif action == 'down':
        v.decrease(delta)
    elif action == 'show':
        print(v)
    elif action == 'mute':
        v.mute()
    else:
        print('Unrecognised action:', action)

def brightness_main(action, delta):
    b = Brightness(delta)
    if action == 'up':
        b.increase()
    elif action == 'down':
        b.decrease()
    elif action == 'show':
        print(b)
    else:
        print('Unrecognised action:', action)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest='command')
    cmd_vol = commands.add_parser('volume')
    cmd_brightness = commands.add_parser('brightness')

    parser_vol = cmd_vol.add_subparsers(dest='action', required=True)
    vol_up = parser_vol.add_parser('up')
    delta = vol_up.add_argument('delta', type=int, default=5, nargs='?')
    vol_down = parser_vol.add_parser('down')
    delta = vol_up.add_argument('delta', type=int, default=5, nargs='?')
    vol_mute = parser_vol.add_parser('mute')
    vol_show = parser_vol.add_parser('show')

    parser_brightness = cmd_brightness.add_subparsers(dest='action', required=True)
    brightness_up = parser_brightness.add_parser('up')
    delta = brightness_up.add_argument('delta', type=int, default=3, nargs='?')
    brightness_down = parser_brightness.add_parser('down')
    delta = brightness_down.add_argument('delta', type=int, default=3, nargs='?')
    brightness_show = parser_brightness.add_parser('show')
    brightness_mute = parser_brightness.add_parser('mute')

    kwargs = vars(parser.parse_args())

    try:
        command = kwargs['command']
        action = kwargs['action']
        if command == 'brightness':
            brightness_main(kwargs['action'], kwargs.get('delta', 0))
        elif kwargs['command'] == 'volume':
                volume_main(kwargs['action'], kwargs.get('delta', 0))
    except Exception as E:
        print(E)
