# coding: utf-8

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

"""基础设置"""
file_path = "data.txt"
font = "张海山草泥马体.ttf"
text = open(file_path,"r",encoding="utf-8").read()

"""制作图片蒙板"""
png_path = Image.open(r"wen.png")
img_array = np.array(png_path)

"""绘制词云"""
wordcloud = WordCloud(mask=img_array,
                      background_color="white",
                      scale=1.5,
                      font_path=font
                      ).generate(text)
plt.imshow(wordcloud)
plt.axis("off")  #关闭坐标轴
plt.show()

"""保存图片"""
save_path = "result.jpg"
wordcloud.to_file(save_path)