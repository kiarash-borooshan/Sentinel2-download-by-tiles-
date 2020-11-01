""" download images with specific tile, cloudy and date """


from sentinelsat import SentinelAPI
from collections import OrderedDict
import pandas as pd
import time
import os

tic_Down = time.time()

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
report = parent_dir + "/" + reportName

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

            """ make directory according by tile number """

            if not os.path.exists(parent_dir + "/" + "ISA-Sentinel"):
                os.mkdir(parent_dir + "/" + "ISA-Sentinel")

            if not os.path.exists(parent_dir + "/" + "ISA-Sentinel" + "/" + str(df.values[tile_name][0])):
                os.mkdir(parent_dir + "/" + "ISA-Sentinel" + "/" + str(df.values[tile_name][0]))

            if not os.path.exists(parent_dir + "/" + "ISA-Sentinel" + "/" + str(df.values[tile_name][0]) +
                                  "/" + str(year)):
                os.mkdir(parent_dir + "/" + "ISA-Sentinel" + "/" + str(df.values[tile_name][0]) + "/" + str(year))

            if not os.path.exists(parent_dir + "/" + "ISA-Sentinel" + "/" + str(df.values[tile_name][0]) + "/" +
                                  str(year)
                                  + "/" + str(Month)):
                os.mkdir(parent_dir + "/" + "ISA-Sentinel" + "/" + str(df.values[tile_name][0]) + "/" + str(year) +
                         "/" + str(Month))

            """ download cloud less than 35 percent and more than 400 Mb"""
            CldPrcSort = sorted(mdict.keys())
            for mmin in CldPrcSort:
                # mdict[CldPrcSort[0]]
                uuid = mdict[mmin]
                # prod = prePro[uuid]
                if float(prePro[uuid]['size'][:-3]) > 400 and prePro[uuid]['cloudcoverpercentage'] < 35:
                    if api.is_online(uuid):
                        a = pd.read_csv(report, index_col=None)
                        if a["title"][num_img] == "total size (Mb) / frame name":
                            num_img += 1
                            continue
                        else:
                            a["status"][num_img] = "downloaded"
                            a.to_csv(report, index=False)
                            del a
                            num_img += 1

                            api.download(uuid, parent_dir + "/" + "ISA-Sentinel" + "/" +
                                         str(df.values[tile_name][0]) + "/" + str(year) + "/" + str(Month))

                    else:
                        a = pd.read_csv(report, index_col=None)
                        if a["title"][num_img] == "total size (Mb) / frame name":
                            num_img += 1
                            continue
                        else:
                            a["status"][num_img] = "not online"
                            a.to_csv(report, index=False)
                            del a
                            num_img += 1
                            api.download(uuid, parent_dir + "/" + "ISA-Sentinel" + "/" +
                                         str(df.values[tile_name][0]) + "/" + str(year) + "/" + str(Month))
                    # break

toc_Down = time.time()
unite = "sec"
du = toc_Down - tic_Down
if du > 60:
    unite = "min"
    du = du / 60
print("duration {} {}" .format(du, unite))
