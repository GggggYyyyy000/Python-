# -*- coding: utf-8 -*-
import arcpy

a = ["0101","0102","0103"]
b = ["0201","0202","0203","0204"]
c = ["0301","0302","0303","0304","0305","0306","0307"]
d = ["0401","0402","0403","0404"]
e = ["0501","0502","0503","0504","0505","0506","0507"]
f = ["0601","0602","0603","0604"]
g = ["0701","0702"]
h = ["0801","0802","0803","0804","0805","0806","0807","0808","0809","0810"]
i = ["0901","0902","0903","0904","0905","0906"]
j = ["1001","1002","1003","1004","1005","1006","1007","1008","1009"]
k = ["1101","1102","1103","1104","1105","1106","1107","1108","1109","1110"]
l = ["1201","1202","1203","1204","1205","1206","1207"]  


coding = {"a":"耕地","b":"园地","c":"林地","d":"草地","e":"商服用地","f":"公矿仓储用地","g":"住宅用地","h":"公共管理与公共服务用地","i":"特殊用地","j":"交通运输用地","k":"水域及水利设施用地","l":"其他用地"}
Agricultural_land = ["0101","0102","0103","0201","0202","0203","0204",
                    "0301","0302","0303","0304","0305","0306","0307",
                    "0401","0402","0403","1006","1103","1104","1107","1202","1203"]
Construction_land = ["0501","0502","0503","0504","0505","0506","0507","0601","0602",
                    "0603","0604","0701","0702","0801","0802","0803","0804","0805",
                    "0806","0807","0808","0809","0810","0901","0902","0903","0904",
                    "0905","0906","1001","1002","1003","1004","1005","1006","1007",
                    "1008","1009","1109","1201",]
Unused_land = ["0404","1101","1102","1105","1106","1108","1110","1204","1205","1206","1207"]

#fc = arcpy.GetParameterAsText(0)
fc = r"D:\\python\\Acrpy\\data\\land.shp"
code = "DLBM2"
try:
    arcpy.AddField_management(fc, "DLBM_一级类", "TEXT")     #添加字段
    arcpy.AddField_management(fc, "DLBM_二级类", "TEXT")     #添加字段
    arcpy.AddField_management(fc, "DLBM_大类", "TEXT")     #添加字段
    arcpy.AddMessage("新的字段添加成功")
except:
    arcpy.AddWarning("字段已存在，添加失败")   
cursor = arcpy.UpdateCursor(fc)
for row in cursor:
    DLBM = str(row.getValue(code))
    if DLBM in a:
        row.setValue("DLBM_一级类", coding["a"])
    if DLBM in b:
        row.setValue("DLBM_一级类", coding["b"])
    if DLBM in c:
        row.setValue("DLBM_一级类", coding["c"])
    if DLBM in d:
        row.setValue("DLBM_一级类", coding["d"])
    if DLBM in e:
        row.setValue("DLBM_一级类", coding["e"])
    if DLBM in f:
        row.setValue("DLBM_一级类", coding["f"])
    if DLBM in g:
        row.setValue("DLBM_一级类", coding["g"])
    if DLBM in h:
        row.setValue("DLBM_一级类", coding["h"])
    if DLBM in i:
        row.setValue("DLBM_一级类", coding["i"])
    if DLBM in j:
        row.setValue("DLBM_一级类", coding["j"])
    if DLBM in k:
        row.setValue("DLBM_一级类", coding["k"])
    if DLBM in l:
        row.setValue("DLBM_一级类", coding["l"])
    if DLBM in Agricultural_land:
        row.setValue("DLBM_大类", "农用地")
    if DLBM in Construction_land:
        row.setValue("DLBM_大类", "建设用地")
    if DLBM in Unused_land:
        row.setValue("DLBM_大类", "非利用地")
    cursor.updateRow(row)
