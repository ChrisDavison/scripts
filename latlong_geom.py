#!/usr/bin/env python3
"""Calculate geometry involving latitudes and longitudes

This is approximate (i.e. it assumes perfect sphere).
"""
import sys
import numpy as np
from argparse import ArgumentParser


RADIUS_EARTH = 6317 # kilometres


def area_above_latitude(lat, radius=RADIUS_EARTH):
    lat_as_radians = lat * np.pi / 180
    return 2 * np.pi * radius * radius * (1 - np.sin(lat_as_radians))


def area_between_latitudes(lat1, lat2, radius=RADIUS_EARTH):
    lat1, lat2 = (lat1, lat2) if lat1 > lat2 else (lat2, lat1)
    return area_above_latitude(lat2, radius) - area_above_latitude(lat1, radius)


def area_quadrangle(latlon1, latlon2, radius=RADIUS_EARTH):
    lat1, lon1 = latlon1
    lat2, lon2 = latlon2
    area_of_band = area_between_latitudes(lat1, lat2, radius)
    vertical_proportion_of_sphere = (lon2 - lon1) / 360
    return area_of_band * vertical_proportion_of_sphere


def area_earth():
    return area_quadrangle((-90, -180), (90, 180))


def area_quadrangle_as_proportion_of_earth(latlon1, latlon2):
    return area_quadrangle(latlon1, latlon2) / area_earth()


def to_decimal_degrees(dms_north, dms_east):
    degrees, minutes, seconds = dms_north
    dd_north = degrees + (minutes + (seconds / 60)) / 60

    degrees, minutes, seconds = dms_east
    dd_east = degrees + (minutes + (seconds / 60)) / 60
    print("{:.3f},{:.3f}".format(dd_north, dd_east))


if __name__ == "__main__":
    PARSER = ArgumentParser()
    PARSER.add_argument("d_north", type=float)
    PARSER.add_argument("m_north", type=float)
    PARSER.add_argument("s_north", type=float)
    PARSER.add_argument("d_east", type=float)
    PARSER.add_argument("m_east", type=float)
    PARSER.add_argument("s_east", type=float)
    ARGS = PARSER.parse_args()
    dms_north = (ARGS.d_north, ARGS.m_north, ARGS.s_north)
    dms_east = (ARGS.d_east, ARGS.m_east, ARGS.s_east)
    to_decimal_degrees(dms_north, dms_east)
