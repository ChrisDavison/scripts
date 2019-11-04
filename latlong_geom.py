#!/usr/bin/env python3
"""Calculate geometry involving latitudes and longitudes

This is approximate (i.e. it assumes perfect sphere).
"""
import sys
import numpy as np


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
    return area_of_band * vertical_proportion_of_sphere2


def area_earth():
    return area_quadrangle((-90, -180), (90, 180))


def area_quadrangle_as_proportion_of_earth(latlon1, latlon2):
    return area_quadrangle(latlon1, latlon2) / area_earth()
