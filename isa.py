#!/usr/bin/env python3
import dataclasses
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class ISA:
    invested: float = 0
    total: float = 0
    platform: float = 0
    rate: float = 0

    def __str__(self):
        return f"Invested {self.invested}; savings {self.total}"

    def one_year(self, invest: float):
        interest = 1 + ((self.rate - self.platform) / 100)
        self.total = (self.total + invest) * interest
        self.invested += invest
        return self.total

