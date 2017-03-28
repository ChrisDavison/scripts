from .timerange import TimeRange
from .listop import *
from .plottools import *
# from prelude import

import argparse
import os
import re
import sys
import datetime as dt
import json
import shutil
import matplotlib

from collections import defaultdict
import pprint as pp

from toolz.itertoolz import *
from toolz.functoolz import *
from toolz.dicttoolz import *
from functools import reduce
from itertools import chain
from os.path import join

# installed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import dateutil.parser as dp

import scipy.fftpack as sfft

# from sarascripts repo
sys.path.append('/Users/christopherdavison/p/engd-sarascripts/Python/scripts/')
import helpers as hlp
import hlp_heat as ht
import hlp_sh
import hlp_hoko
import hlp_rw
import pandas_utils as pu
import cdutils.log as cdl
import cdutils.osutils as cdo

from cdutils.indexable_generator import Indexable

__prelude_help__ = """StdLib Imports:

- argparse, os, re, sys, datetime (dt), json, shutil
- defaultdict
- pprint (pp)
- join (os.path)

External Imports:

- pytoolz itertoolz *, functoolz *, dicttoolz *
- matplotlib.pyplot (plt), numpy (np), pandas (pd), dateutil.parser (dp)
    scipy.fftpack (sfft)

My custom scripts (from sarascripts):

- helpers (hlp), hlp_heat (ht), hlp_sh, hlp_hoko, hlp_rw, pandas_utils (pu)
    cdutils.hmm_params (chmm), cdutils.log (cdl), cdutils.osutils (cdo)
- indexable_generator (Indexable)
"""

def prelude_help():
    print(__prelude_help__)
