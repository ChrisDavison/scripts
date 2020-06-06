#!/usr/bin/env python3
"""Coronavirus projections"""
import os.path as op
import re
import sys
import datetime
from collections import namedtuple

import matplotlib.pyplot as plt
import numpy as np
import requests
import pandas as pd


VERBOSE = False
LAST_N = 5
NUMBER_FILE = op.join(op.dirname(op.realpath(__file__)), "corona-numbers")
MAX_POLY = 4
DATED_NUMBER = namedtuple("DatedNumber", "date value")


def get_todays_number(last_num):
    rx_number = re.compile("([0-9,]+).*were positive")
    response = requests.get(
        "https://www.gov.scot/publications/coronavirus-covid-19-daily-data-for-scotland/"
    ).text
    covid_number = rx_number.search(response)
    if covid_number:
        num = int(covid_number.group(1).replace(",", ""))
        if last_num.value != num:
            print("Added today:", num)
            return DATED_NUMBER(datetime.date.today(), num)
    return None


def get_numbers():
    """Return the latest available number of cases in Scotland

    Read corona-numbers from the same dir as the script (following symlinks),
    and potentially add today's number if a new number has been added to
    gov.scot's coronavirus page (DOESN'T check date, just assumes that the
    number will increase and so compares to the last stored number).
    """
    # Existing numbers
    global NUMBER_FILE
    numbers = []
    for line in open(NUMBER_FILE, "r"):
        date, num = line.split(",")
        numbers.append(
            DATED_NUMBER(datetime.datetime.strptime(date, "%Y-%m-%d").date(), int(num))
        )
    is_before_2pm = datetime.datetime.now().hour < 14
    # Check if a new number exists
    todays_number = get_todays_number(last_num=numbers[-1])
    new = False
    if todays_number:
        numbers.append(todays_number)
        new = True
    return numbers, new


def predict_average(numbers):
    """Mean of growthrates"""
    delta_days = [(n1.date - n0.date).days for n0, n1 in zip(numbers, numbers[1:])]
    ratios = [n1.value / n0.value for n0, n1 in zip(numbers, numbers[1:])]
    rates = [ratio / delta for (delta, ratio) in zip(delta_days, ratios)]
    growthrate = sum(rates) / len(rates)
    if VERBOSE:
        print(rates)
        print("{:.3f}".format(growthrate))
        print()
    last_diff = numbers[-1].value - numbers[-2].value
    return int(numbers[-1].value + last_diff * growthrate), growthrate


def predict_growthrate_poly(numbers, degrees):
    """Polyfit on growthrates"""
    date_0 = numbers[0].date
    days_since_0 = np.array([(n.date - date_0).days for n in numbers][1:])
    delta_days = [(n1.date - n0.date).days for n0, n1 in zip(numbers, numbers[1:])]
    ratios = np.array([n1.value / n0.value for n0, n1 in zip(numbers, numbers[1:])])
    rates = [ratio / delta for (delta, ratio) in zip(delta_days, ratios)]
    model = np.poly1d(np.polyfit(days_since_0, rates, degrees))
    growthrate = model(days_since_0[-1] + 1)
    if VERBOSE:
        print(growthrate)
    last_diff = numbers[-1].value - numbers[-2].value
    return int(numbers[-1].value + last_diff * growthrate), growthrate


def index_of_nearest(numbers, actual):
    index_min_diff = 0
    min_diff = np.infty
    for i, val in enumerate(numbers):
        diff = np.abs(val - actual)
        if diff <= min_diff:
            min_diff = diff
            index_min_diff = i
        else:
            pass
    return index_min_diff


def prediction_list(predictions_and_descriptions, actual, with_closest=False):
    index_min_diff = index_of_nearest(
        [n[0] for n in predictions_and_descriptions], actual
    )
    out = ""
    for i, (val, description) in enumerate(predictions_and_descriptions):
        closest = " "
        if with_closest and i == index_min_diff:
            closest = "*"
        out += "  {closest} {val} - {desc}\n".format(
            val=val, desc=description, closest=closest
        )
    return out


def get_predictions(numbers):
    predict_today, rate = predict_average(numbers[-LAST_N:])
    predictions = []
    for degree in range(1, MAX_POLY + 1):
        prediction, rate = predict_growthrate_poly(numbers, degree)
        predictions.append((prediction, "poly" + str(degree), rate))

    mean_rate = np.mean([r for _, _, r in predictions])
    predictions.append((int(mean_rate * numbers[-1][1]), "μ(all poly)", mean_rate))
    return predictions


def nth(n):
    def nth_n(indexable):
        return indexable[n]

    return nth_n


def print_predictions(message, numbers, last, closest_marker):
    outfmt = "{}{} - {:12s} ({:.3f})"
    print("\n" + message)
    predictions = get_predictions(numbers)
    index_closest = index_of_nearest([p for p, _, _ in predictions], last.value)
    for i, (val, description, growth) in enumerate(predictions):
        print(
            outfmt.format(
                closest_marker if i == index_closest else "  ", val, description, growth
            )
        )


def plot_new_cases(data, ax=None):
    num_only = [n.value for n in data]
    diffs = [n - n_prev for n_prev, n in zip(num_only, num_only[1:])]
    dates = [n.date for n in data[1:]]

    weekends = [d for d in dates if d.weekday() >= 5]

    if not ax:
        f = plt.figure(figsize=(12, 7))
        ax = plt.gca()
    ax.plot_date(dates, diffs, c="b", label="new cases", marker="x")
    ax.plot_date(
        dates,
        pd.Series(diffs).rolling(7).mean(),
        ls="dashed",
        marker=".",
        c="k",
        label="7 day RM",
    )
    ax.set_title("Cases added")
    ax.set_xticks(dates)
    ax.set_xlim(dates[0]-datetime.timedelta(days=1), dates[-1]+datetime.timedelta(days=1))
    ax.tick_params(axis='x', labelrotation=90)
    ymin, ymax = ax.get_ylim()
    ax.vlines(
        weekends, ymin, ymax, ls="dashed", label="weekend", colors="r", alpha=0.5
    )
    plt.legend(loc="upper right")
    plt.tight_layout()
    return plt.gcf()


def plot_total_cases(data, ax=None):
    num_only = [n.value for n in data]
    dates = [n.date for n in data]

    if not ax:
        f = plt.figure(figsize=(12, 7))
        ax = plt.gca()
    ax.plot_date(dates, num_only, c="k", ls="solid", label="new cases", marker="x")
    ax.set_title("Total cases")
    ax.set_xticks(dates)
    ax.tick_params(axis='x', labelrotation=90)
    ax.set_xlim(dates[0]-datetime.timedelta(days=1), dates[-1]+datetime.timedelta(days=1))
    ax.set_label("Day")
    ymin, ymax = ax.get_ylim()

    weekends = [d for d in dates if d.weekday() >= 5]
    ax.vlines(
        weekends, ymin, ymax, ls="dashed", label="weekend", colors="r", alpha=0.5
    )
    plt.legend(loc="upper right")
    plt.tight_layout()
    return plt.gcf()


def main():
    """Run various coronavirus projections"""
    data, added_today = get_numbers()

    history = ", ".join([str(i[1]) for i in data[-5:]])
    print("LAST UPDATE\t", data[-1].date)
    print("...{}".format(history))
    print_predictions("predicted", data[:-1], data[-1], "* ")
    print_predictions("next?", data, data[-1], "  ")

    if added_today:
        with open(NUMBER_FILE, "w") as f_numbers:
            for entry in data:
                print("{},{}".format(entry.date, entry.value), file=f_numbers)
        print("\nWrote new number to file")

    f, (ax1, ax2) = plt.subplots(2, figsize=(12, 7), sharex=True)
    f = plot_new_cases(data, ax1)
    f = plot_total_cases(data, ax2)
    f.savefig("corona.png", dpi=300)


if __name__ == "__main__":
    if "-v" in sys.argv or "--verbose" in sys.argv:
        VERBOSE = True
    main()
