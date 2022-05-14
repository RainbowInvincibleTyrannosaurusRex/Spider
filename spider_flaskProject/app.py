# coding=utf-8

from flask import Flask, render_template

import jieba  # 分词
from wordcloud import WordCloud  # 词云
from matplotlib import pyplot  # 绘图、数据可视化
import numpy  # 矩阵运算
import sqlite3

app = Flask(__name__)


@app.route('/')
def html():  # put application's code here
    # 返回html静态页面
    return render_template("index.html")


# 首页
@app.route('/index')
def index():
    # return render_template("index.html")
    return html()


# 电影
@app.route('/movie')
def movie():
    datalist = []
    database = sqlite3.connect("movie.db")
    cursor = database.cursor()
    sql = "select * from top250"
    data = cursor.execute(sql)
    for item in data:
        datalist.append(item)
    cursor.close()
    database.close()
    return render_template("movie.html", movies=datalist)


# 评分
@app.route('/score')
def score():
    score = []  # 评分
    num = []  # 评分对应电影数
    database = sqlite3.connect("movie.db")
    cursor = database.cursor()
    sql = "select score,count(score) from top250 group by score"
    data = cursor.execute(sql)
    for item in data:
        score.append(item[0])
        num.append(str(item[1]))
        print(item[0])
    cursor.close()
    database.close()
    return render_template("score.html", score=score, num=num)


# 词云
@app.route('/word')
def word():
    return render_template("word.html")


# 团队
@app.route('/team')
def team():
    return render_template("team.html")


if __name__ == '__main__':
    app.run()

# ctrl+R替换 ctrl+F搜索
