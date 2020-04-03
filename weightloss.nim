import os
import strUtils
import strformat

const start = 118
var appname = extractFilename(getAppFilename())

proc print_usage = 
  echo fmt"usage: {appname} <value> <lb|st|kg>"

proc show_weight(value: float, unit: string) = 
  var
    value_kg: float
    value_st: float
    value_lb: float
    diff:     float
  case unit
  of "kg":
    value_kg = value
  of "lb":
    value_kg = value / 2.2
  of "st":
    value_kg = value * 14.0 / 2.2
  else: 
    echo "unknown unit: ", unit
    echo fmt"usage: {appname} <value> <lb|st|kg>"
    quit 1
  value_st = value_kg * 2.2 / 14
  value_lb = value_kg * 2.2
  diff = start - value_kg
  echo fmt"{value_kg:.2f}kg {value_st:.2f}st {value_lb:.2f}lb (lost {diff:.2f}kg)"

let arguments = commandLineParams()

if len(arguments) < 2:
  echo fmt"usage: {appname} <value> <lb|st|kg>"
  quit 0

show_weight(parseFloat(arguments[0]), arguments[1])

