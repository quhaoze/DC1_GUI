from flask import Flask

# 用当前脚本名称实例化Flask对象，方便flask从该脚本文件中获取需要的内容
app = Flask(__name__)

#程序实例需要知道每个url请求所对应的运行代码是谁。
#所以程序中必须要创建一个url请求地址到python运行函数的一个映射。
#处理url和视图函数之间的关系的程序就是"路由"，在Flask中，路由是通过@app.route装饰器(以@开头)来表示的
@app.route("/")
def index():
    return "Hello World!"
#url映射的函数，要传参则在上述route（路由）中添加参数申明
# 直属的第一个作为视图函数被绑定，第二个就是普通函数
# 路由与视图函数需要一一对应
# def not():
#     return "Not Hello World!"


# methods参数用于指定允许的请求格式
# 常规输入url的访问就是get方法
@app.route("/hello", methods=['GET', 'POST'])
def hello():
    return "Hello World! test2"


# 注意路由路径不要重名，映射的视图函数也不要重名
@app.route("/hi", methods=['POST'])
def hi():
    return "Hi World!"


# 可以在路径内以/<参数名>的形式指定参数，默认接收到的参数类型是string

'''#######################
以下为框架自带的转换器，可以置于参数前将接收的参数转化为对应类型
string 接受任何不包含斜杠的文本
int 接受正整数
float 接受正浮点数
path 接受包含斜杠的文本
########################'''

#get请求是这样的，数据完全位于URL里面，但是post就不是了，浏览器里面输入网址，属于get请求
@app.route("/index/<int:id>", )
def index2(id):
    if id == 1:
        return 'first'
    elif id == 2:
        return 'second'
    elif id == 3:
        return 'thrid'
    else:
        return 'hello world!'


# 启动一个本地开发服务器，激活该网页
app.run()

