import click
from dataclasses import dataclass


KM_IN_MI = 1.60934
L_IN_UK_GAL = 4.54609

@dataclass
class KmPerL:
    pass

@dataclass
class LPer100Km:
    pass


@dataclass
class MPG:
    mpg: float

    def to_mpg(self):
        return self

    def to_kmperl(self) -> KmPerL:
        return KmPerL(self.mpg / L_IN_UK_GAL * KM_IN_MI)

    def to_lper100km(self) -> LPer100Km:
        return LPer100Km()

@dataclass
class KmPerL:
    kmperl: float
    def to_mpg(self):
        return MPG(self.kmperl * L_IN_UK_GAL / KM_IN_MI)

    def to_kmperl(self) -> KmPerL:
        return self

    def to_lper100km(self) -> LPer100Km:
        return LPer100Km(100 * self.kmperl)


@dataclass
class LPer100Km:
    lper100km: float
    def to_mpg(self):
        return MPG()

    def to_kmperl(self) -> KmPerL:
        return KmPerL()

    def to_lper100km(self) -> LPer100Km:
        return self


def to_mpg(value, unit):
    if unit == "mpg":
        return value
    elif unit == "km/l":
        # ... TODO
        return value * L_IN_UK_GAL / KM_IN_MI
    else:
        # TODO
        return (100 / value) * L_IN_UK_GAL / KM_IN_MI


def to_kmperl(value, unit):
    if unit == "mpg":
        return value / L_IN_UK_GAL * KM_IN_MI
    elif unit == "km/l":
        return value
    else:
        return 100 / value


def to_lper100km(value, unit):
    if unit == "mpg":
        return 1 / (value * KM_IN_MI / L_IN_UK_GAL / 100)
    elif unit == "km/l":
        return 100 * value
    else:
        return value



@click.command()
@click.argument("value", type=float, required=True)
@click.argument("unit", type=click.Choice(["mpg", "km/l", "l/100km"]), default="mpg")
def main(value, unit):
    mpg = to_mpg(value, unit)
    kmperl = to_kmperl(value, unit)
    lper100km = to_lper100km(value, unit)
    print(f"Economy {mpg:.2f}mpg ({kmperl:.2f}km/l)")
    print(f"Consumption {lper100km:.2f} l/100km")

    print(MPG(mpg).to_kmperl().range())

    tank=10.0

    range_mi = mpg * (tank / L_IN_UK_GAL)
    range_km = range_mi * 1.61
    print(f"\nFor {tank}l tank...")
    print(f"\t{range_mi:.2f}mi ({range_km:.2f}km)")


if __name__ == "__main__":
    main()
