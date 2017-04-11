from .timerange import *
from .listop import *
from .plottools import *
from .utility import *
from .indexable_generator import *

from .plots import *

import pandas_utils as pu

from .dsp import calculus as calc
from .dsp.fft import easy_fft
from .dsp.filter import high_pass, low_pass

import argparse
import os
import re
import sys
import datetime as dt
import json
import shutil
import matplotlib
import logging

from collections import defaultdict
import pprint as pp

from toolz.itertoolz import *
from toolz.functoolz import *
from toolz.dicttoolz import *
from functools import reduce
from itertools import chain
from os.path import join, expanduser

# installed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import dateutil.parser as dp

import scipy.fftpack as sfft

# from sarascripts repo
__homedir = expanduser('~'),
__sarascripts_path = os.path.join(__homedir[0], 'cow-analysis')
sys.path.append(__sarascripts_path)

from pyscripts.helpers import *

def create_logger(name, level=logging.DEBUG):
    """Create a logger for monitoring long-running jobs."""  
    fmt = '%(asctime)s %(levelname)s -- %(message)s'
    logging.basicConfig(format=fmt, filename=name, level=level)
    return os.path.abspath(name)
