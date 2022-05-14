# coding=utf-8


from flask import Flask, render_template,request
import datetime

app = Flask(__name__)


# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


# @app.route("/user/<name>")
# # 用户访问网址时，输入url中的name当做参数传给函数
# def welcome(name):
#     return "你好，%s" % name


# @app.route("/user/<int:id>")
# 用户访问网址时，输入url中的name当做参数传给函数
# def welcome(id):
# return "你好，%d" % id
# 路由路径不能重复，用户只能通过唯一路径来访问特定函数


# 返回给用户渲染后的网页文件
@app.route("/")
def html():
    time = datetime.date.today()
    data = ['甲', '乙', '丙']
    task = {"学习内容": "爬虫", "内容": "数据可视化"}
    # 注意，字典类型的key不可重复，但value可以
    return render_template("demo.html", var=time, list=data, task=task)
# 向html文件传递参数，方便实现返回动态网页


# 表单提交
@app.route('/form/register')
def form():
    return render_template("test/form.html")


# 接收表单提交的路由
# 默认为get方式访问，但form.html中表单提交方式为post，需进行设定
@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method=='POST':
        result = request.form  # request.form将提交表单变成字典返回，注意，此时表单中的key为提交表单的input中的name属性，value为输入值
        return render_template("test/result.html", result=result)


if __name__ == '__main__':
    app.run()
    #     开启debug模式，使修改后不用暂停服务或重新运行也能得到实时反馈且显示错误信息更详细
