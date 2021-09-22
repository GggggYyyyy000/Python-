import os 

"""
1.zotero的附件是放在一个hash值命名的文件夹中，该hash值即zotero的url scheme中[item id]
2.遍历zotero的storage库，构建pdf文件名到其[item id]的映射字典
3.利用quicker获取当前pdf阅读器的窗口标题，即pdf文件名
4.从字典中查出[item id]
5.构建url scheme
6.在原句子末尾添加markdown链接
7.将附带markdown链接的句子写入剪切板
"""

def better_zoteroAn(content,name,page):
    file_path = "/Users/creative/Zotero/storage"
    files = {}
    for i in os.listdir(file_path):
        try:
            for x in os.listdir(file_path + "/" + i):
                if ".pdf" in x:
                    files.update({x.replace(".pdf",""):i})
        except:
            pass
    links = "zotero://open-pdf/library/items/" + files[name] + "?page=" + page
    Anlink = content + "[" + name.split("-")[len(name.split("-"))-1] + "](" + links + ")"
    return Anlink


def clip_zoteroAn(content,name,page):
    codes = name.split("/")[len(name.split("/"))-2]
    N = name.split("/")[len(name.split("/"))-1]

    links = "zotero://open-pdf/library/items/" + codes + "?page=" + page
    Anlink = content + "[" + N.replace(".pdf","") + "](" + links + ")"
    return Anlink


content = "Urban public services are traditionally covered under the definition of public goods that are consumed by many citizen-consumers simultaneously; exclusion from their benefits is impossible or very difficult."
#name = "Aljohani 和 Thompson - 2016 - Impacts of logistics sprawl on the urban environme"
text = "/Users/creative/Zotero/storage/L2LZSSLP/(Beler) Erkip - 1997 - The distribution of urban public services the cas.pdf"
page = "2"

#print(better_zoteroAn(content,name,page))
print(clip_zoteroAn(content,text,page))



