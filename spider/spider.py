# coding=utf-8
# 时间：2022/5/7 9:49

from bs4 import BeautifulSoup  # 网页解析、获取数据
import re  # 正则表达式、文字匹配
import urllib.request, urllib.error  # 指定URL，获取网页数据
import xlwt  # 进行Excel操作
import sqlite3  # SQLite数据库
import urllib.parse

'''
爬取网页
解析数据
保存数据
'''


def main():
    url = "http://movie.douban.com/top250?start="
    # savepath = "豆瓣Top250.xls"
    datalist = getData(url)
    # saveDataforExcel(datalist,savepath)
    # savepath = "movie.db"
    # saveDataforDataBase(datalist, savepath)


findlink = re.compile(r'<a href="(.*?)">')  # html文档中href是双引号，故最外层用单引号，而最外层用单引号则内层用双引号
findImgsrc = re.compile(r'<img .*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


def getData(baseurl):
    datalist = []
    for i in range(25):
        url = baseurl + str(i * 25)
        html = askURL(url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            data = []
            item = str(item)
            link = re.findall(findlink, item)[0]  # 返回类型是列表，可以通过下标访问
            data.append(link)
            img = re.findall(findImgsrc, item)[0]
            data.append(img)
            title = re.findall(findTitle, item)  # 片名可能不止一个，或者只有一个
            if len(title) == 2:
                data.append(title[0])
                data.append(title[1].replace("/", "").replace("\xa0", ""))
            else:
                data.append(title[0])
                data.append(' ')  # 外文名留空
            rat = re.findall(findRating, item)[0]
            data.append(rat)
            judge = re.findall(findJudge, item)[0]
            data.append(judge)
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                data.append(inq[0].replace("。", ""))
            else:
                data.append(' ')
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', ' ', str(bd))
            data.append(bd.replace("\xa0", " ").replace("/", "").replace("...", "").strip())  # 去掉空格
            datalist.append(data)
    # for index in datalist:
    #     print(index)
    return datalist


def askURL(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
    }
    request = urllib.request.Request(url=url, headers=header)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    # print(html)
    return html


def saveDataforExcel(datalist, savepath):
    workbook = xlwt.Workbook(encoding="utf-8")  # 创建workbook对象
    worksheet = workbook.add_sheet("豆瓣Top250", cell_overwrite_ok=True)  # 创建工作表 cell_overwrite_ok=True，写入时覆盖以前内容
    col = ("电影详情链接", "海报链接", "中文名", "外文名", "评分", "评价人数", "概括", "相关信息")
    # 放入表头
    for i in range(8):
        worksheet.write(0, i, col[i])
    #     放入数据
    for i in range(250):
        # print("第%d条"%i)
        data = datalist[i]
        for j in range(8):
            worksheet.write(i + 1, j, data[j])
    workbook.save(savepath)


def saveDataforDataBase(dadalist, savepath):
    initDateBase(savepath)
    database = sqlite3.connect(savepath)
    cursor = database.cursor()
    for data in dadalist:
        for index in range(len(data)):
            data[index] = '"' + data[index] + '"'
        sql = '''
        insert into top250 
        (movie_link,photo_link,cname,fname,score,rated,instroduction,info)
        values(%s)''' % ",".join(data)
        cursor.execute(sql)
        database.commit()
    cursor.close()
    database.close()


def initDateBase(savepath):
    sql = '''
        create table top250
        (
        id integer primary key autoincrement,
        movie_link text,
        photo_link text,
        cname varchar,
        fname varchar,
        score varchar,
        rated varchar,
        instroduction text,
        info text
        )
        '''
    database = sqlite3.connect(savepath)
    cursor = database.cursor()
    cursor.execute(sql)
    database.commit()
    database.close()


if __name__ == "__main__":
    main()
    print("爬取完毕！")
