# coding=utf-8
# 时间：2022/5/7 9:50
import re
import sqlite3
import urllib.request, urllib.response, urllib.parse

# 浏览器用GET请求来获取一个html页面/图片/css/js等资源；用POST来提交一个<form>表单，并得到一个结果的网页。
# 获取一个get请求
#     datalist = urllib.request.urlopen("http://www.baidu.com/")
# return datalist.read().decode("utf-8")  # 解码操作，使内容正常
# 获取一个post请求，由于没写服务器，用httpbin.org测试
# data=bytes(urllib.parse.urlencode({"hello":"world"}),encoding="utf-8")
# response=urllib.request.urlopen("http://httpbin.org/post",data=data)
# print(response.read().decode("utf-8"))
#  设置超时
# try:
#     datalist=urllib.request.urlopen("http://www.baidu.com/",timeout=0.01)
#     print(datalist.read().decode("utf-8"))
# except urllib.error.URLError as e:#取别名e
#     print("请求超时")
#     datalist.status http状态码
# 被发现是爬虫，则会报状态码418
# 超时报错
# data=urllib.request.urlopen("http://www.bilibili.com/")
# print(data.status)
# data.getheaders() 获取访问过程中的response header信息
# data.getheader("Sever") 获取访问过程中的response header信息中的Sever字段

# 避免被发现是爬虫，伪装成浏览器
# url="http://www.bilibili.com"
# header={
# "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
# }
# # 构建请求对象，向其中封装信息，伪装为浏览器骗过服务器
# request=urllib.request.Request(url=url,headers=header)
# # 构建响应对象存储数据
# response=urllib.request.urlopen(request)
# print(response.read().decode("utf-8"))

from bs4 import BeautifulSoup

file = open("./test.html", "rb")
html = file.read().decode("utf-8")
bs = BeautifulSoup(html, "html.parser")

# Tag类型，输出第一个符合的标签及其内容
# print(bs.title, type(bs.title))
# NavigableString类型，只拿第一个的内容
# print(bs.title.string, type(bs.title.string))
# 输出第一个符合的标签的属性值，以字典形式输出
# print(bs.a.attrs, type(bs.a.attrs))
# BeautifulSoup类型，表示整个文档
# print(type(bs))
# Comment类型，是一个特殊的NavigableString类型，输出的内容不包含注释符号<--!-->

# 文档的遍历
# print(bs.head.contents)#以列表形式输出head中全部元素
# 遍历列表即实现文档遍历

# 文档的搜索
# 1.find_all 返回列表
# 字符串过滤：会查找与字符串完全匹配的内容
# t = bs.find_all("a")
# print(t)
# 正则表达式搜索 search()方法搜索 包含a都会输出
# import re
#
# t = bs.find_all(re.compile("a"))
# print(t)
# 自定义方法
# def find(tag):
# return tag.has_attr("name")
# 输出包含name的标签
# t = bs.find_all(find)
# print(t)

# 2.kwargs参数
# 查找class属性时，因为python中有class关键字，所以用class_查找
# t = bs.find_all(class_=True)
# print(t)

# 3.text参数
# 找匹配文本，存在则返回，不存在返回空列表
# text也可以是一个列表
# t = bs.find_all(text="哔哩哔哩 (゜-゜)つロ 干杯~-bilibili")
# t = bs.find_all(text=re.compile('\d'))
# 搭配正则表达式，找包含数字的内容
# print(t)

# 4.limit参数
# limit指定搜索几个
# t = bs.find_all("li", limit=3)
# print(t)

# css选择器
# print(bs.select("title"))
# print(bs.select(".title")) #查找类名
# print(bs.select("#i_cecream")) #查找id
# print(bs.select("link[rel='stylesheet']"))#通过属性查找
# print(bs.select("div>ul")) # 查找div中ul
# print(bs.select("script~div")) #查找script标签的兄弟div标签

'''Re库主要函数
re.search() 在一个字符串中搜索正则表达式第一个位置，返回match对象
re.match() 从一个字符串的开始起匹配正则表达式，返回match对象
re.findall() 搜索字符串，以列表形式返回全部能匹配的子串
re.split() 将字符串按照正则表达式匹配结果进行分割，返回列表类型
re.finditer() 搜索字符串，返回匹配结果的迭代类型，每个迭代元素都是match对象
re.sub() 在一个字符串中替换所有匹配正则表达式的子串，返回替换后的字符串
修饰符
re.l 使匹配对大小写不敏感
re.L 做本地化识别匹配
re.M 多行匹配，影响^和&
re.S 使.匹配包括换行在内的所有字符
re.U 根据unicode字符集解析字符，影响\w、\W、\b、\B
re.X 使正则表达式格式更灵活'''
import re

# 创建模式对象
# pat = re.compile("a")
# m = pat.search("asgbdhsgdhas")

# 不创建模式对象
# m = re.search("a", "asgbdhsgdhas")
# print(m)

# SQLite数据库
sqlite3.connect("test.db")
