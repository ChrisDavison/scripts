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
import datetime
import json
import shutil
import matplotlib
import logging
import pprint

from collections import defaultdict

from toolz.itertoolz import *
from toolz.functoolz import *
from toolz.dicttoolz import *
from functools import reduce
from itertools import chain
from os.path import join, expanduser

# installed
import matplotlib.pyplot
import numpy
import pandas
import dateutil.parser
import scipy.fftpack
import seaborn

from scipy.stats import gaussian_kde
from sklearn import svm
from sklearn.model_selection import train_test_split, cross_val_score
import tensorflow
import tflearn

tf = tensorflow

plt = matplotlib.pyplot
np = numpy
pd = pandas
dp = dateutil.parser
sfft = scipy.fftpack
sns = seaborn
dt = datetime
pp = pprint

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
