#!/usr/bin/env bash

CITY=${1:-glasgow}
curl "http://wttr.in/$CITY"
