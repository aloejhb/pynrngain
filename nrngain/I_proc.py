"""
             InjectStimulus

first argument defines one out of three possible stimulus types:
  0: constant current input
  1: Ornstein-Uhlenbeck process (colored noise)
  2: Sinusoid with additive colored noise
"""
import numpy as np
import random
from math import exp, sqrt, pi

import neuron

