""" create a report for haw many images are available
 with specific clouds and date in the tiles"""

from sentinelsat import SentinelAPI
from collections import OrderedDict
import pandas as pd
import time
import os

tic_report = time.time()

""" read password file and login """

a = pd.read_csv("pass.txt")
user = a.values[0][0]
password = a.values[1][0]

api = SentinelAPI(user, password)

""" query prepare """
producttype = "S2MSI1C"
# producttype = "S2MS2Ap"    # doesn't work
# producttype = "S2MSI2A"    # doesn't work

year_from = "2019"
year_to = "2019"

""" report """
reportName = "ISA - cloud percent less than 35 percent and size.csv"
