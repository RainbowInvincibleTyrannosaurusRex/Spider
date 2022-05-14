# coding=utf-8
# Time : 2022/5/12  20:27
import jieba  # 分词
from wordcloud import WordCloud  # 词云
from matplotlib import pyplot  # 绘图、数据可视化
import numpy  # 矩阵运算
import sqlite3
from PIL import Image  # 图片处理

text = ""
database = sqlite3.connect("movie.db")
cursor = database.cursor()
sql = "select instroduction from top250"
data = cursor.execute(sql)
for item in data:
    text += item[0]
cursor.close()
database.close()

# 分词
cut = jieba.cut(text)  # 返回一个对象
info = ' '.join(cut)
# print(info)

# 生成遮罩
img = Image.open(r'./static/assets/img/img.jpeg')  # 打开遮罩图
img_array = numpy.array(img)  # 将图片转换为数组
wc = WordCloud(
    # 是输出的背景图颜色，不是遮罩图颜色
    background_color='white',
    mask=img_array,
    font_path="msyh.ttc"
    #     选择的字体需支持中文才可显示
).generate_from_text(info)
# 也可wc.generate_from_text(info)

# 绘图
fig = pyplot.figure(1)
pyplot.imshow(wc)
pyplot.axis('off')  # 不显示横纵坐标轴
# pyplot.show()  # 显示生成的词云图片
#  输出词云图片到文件
pyplot.savefig(r'./static/assets/img/wordcloud.jpg', dpi=500)
# dpi调节清晰度
