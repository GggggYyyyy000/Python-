# encoding: utf-8

import arcpy
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def count(type3,j):
    type3 = str(type3)
    j = float(j)
    fj = 1.16602
    gy = 1.897096
    jz = 1.262605
    shang = 0.051739
    miao = 1.241736
    yl = 2.276515
    if type3 == "风景名胜" or type3 == "公园" or type3 == "山" or type3 == "寺庙道观" or type3 == "游乐场":
        if type3 == "风景名胜":
            count = j * fj
        if type3 == "公园":
            count = j * gy
        if type3 == "古建筑":
            count = j * jz
        if type3 == "山":
            count = j * shang
        if type3 == "寺庙道观":
            count = j * miao
        if type3 == "游乐场":
            count = j * yl
    else:
        count = j * 0
    return count
