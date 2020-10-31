from sentinelsat import SentinelAPI
from collections import OrderedDict
import pandas as pd
import time
import os

tic_report = time.time()

""" read password file """
a = pd.read_csv("pass.txt")
user = a.values[0][0]
password = a.values[1][0]

