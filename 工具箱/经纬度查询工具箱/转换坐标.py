import transCoordinateSystem as trc
import pandas as pd
from tqdm import tqdm

files = pd.read_csv("/Users/creative/Downloads/2016_11_15denoise_grade=1,need_mapmatch=1,transport_mode=auto,vacuate_grade=2.csv")

for i in tqdm(range(len(files))):
    loc = trc.bd09_to_wgs84(files.loc[i,"longitude"],files.loc[i,"latitude"])
    files.loc[i,"wgs84_lon"] = loc[0]
    files.loc[i,"wgs84_lat"] = loc[1]

files.to_csv("/Users/creative/Desktop/track84.csv",encoding="utf_8_sig")

