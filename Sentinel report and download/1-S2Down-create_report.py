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
del a

api = SentinelAPI(user, password)


""" query prepare """
producttype = "S2MSI1C"
# producttype = "S2MS2Ap"    # doesn't work
# producttype = "S2MSI2A"    # doesn't work

year_from = "2019"
year_to = "2019"

""" directories """
reportName = "ISA - cloud percent less than 35 percent and size.csv"
# parent_dir = "/media/user/My Passport/Kiarash borooshan"
parent_dir = "/media/user/406CEBC56CEBB3B6/SSIEC/ISA project/Main Source Codes 2/Sentinel report and download"

""" import tiles name """
df = pd.read_csv("Sentinel tiles.csv")

""" for """
products = OrderedDict()
cloudLessSize = 0
CloudSizesYear = []
CloudPrcYear = []
ProducName = []

n = 1
num_img = 0

for tile_name in range(df.__len__()):
    print("**** number: {}". format(n))
    n += 1
    print(df.values[tile_name][0])

    for year in range(int(year_from), int(year_to)+1):
        print(year)

        for Month in range(1, 13):
            print(Month)

            day_max = "30"
            if Month in [2]:
                day_max = "28"

            """ query """
            query_kwargs = {
                "platformname": "Sentinel-2",
                "producttype": producttype,
                "date": (str(year) + str(Month).zfill(2) + str(1).zfill(2),
                         str(year) + str(Month).zfill(2) + str(day_max).zfill(2))
            }

            kw = query_kwargs.copy()
            kw["tileid"] = df.values[tile_name][0]
            prePro = api.query(**kw)

            """ detect less cloud tile for each month and more than 400 Mb"""

            mdict = {}
            for i in prePro:
                mdict[prePro[i]['cloudcoverpercentage']] = i

            """ report least cloudy image """
            CldPrcSortTmp = sorted(mdict.keys())
            for mmin in CldPrcSortTmp:
                uuid = mdict[mmin]
                if float(prePro[uuid]["size"][:-3]) > 400 and prePro[uuid]['cloudcoverpercentage'] < 35:
                    cloudLessSize += float(prePro[uuid]["size"][:-3])
                    CloudSizesYear.append(float(prePro[uuid]["size"][:-3]))
                    CloudPrcYear.append(prePro[uuid]['cloudcoverpercentage'])
                    # break

            CloudSizesYear.append(cloudLessSize)
            CloudPrcYear.append(str(df.values[tile_name][0]))

""" export for report"""
data = {
    "size": CloudSizesYear,
    "CloudPrcYear": CloudPrcYear
}

MyDF = pd.DataFrame(data)
MyDF.insert(2, "status", "not check")
# print(MyDF)

if os.path.isfile(parent_dir + "/" + "report less cloud percent and size  .csv"):
    os.remove(parent_dir + "/" + "report less cloud percent and size  .csv")
    MyDF.to_csv(parent_dir + "/" + "report less cloud percent and size  .csv")
else:
    MyDF.to_csv(parent_dir + "/" + "report less cloud percent and size  .csv")

toc_report = time.time()
unite = "sec"
du = toc_report - tic_report
if du > 60:
    unite = "min"
    du = du / 60
print("duration {} {}" .format(du, unite))