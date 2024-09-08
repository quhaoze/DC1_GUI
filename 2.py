#request：包含前端发送过来的所有请求数据

from flask import Flask,render_template,request

# 用当前脚本名称实例化Flask对象，方便flask从该脚本文件中获取需要的内容
app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
#url映射的函数，要传参则在上述route（路由）中添加参数申明
#不带参数时，最大区别仅仅是第一行方法名不同，一个是GET，一个是POST
#带参数时报文的区别呢？在约定中，GET 方法的参数应该放在 url 中，POST 方法参数应该放在 body 中

#下面这个函数与上面那个相绑定
def index():
    if request.method == 'GET':
        # 想要html文件被该函数访问到，首先要创建一个templates文件，将html文件放入其中
        # 该文件夹需要被标记为模板文件夹，且模板语言设置为jinja2
        return render_template('2.html')
    # 此处欲发送post请求，需要在对应html文件的form表单中设置method为post
    elif request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        return name+" "+password

if __name__=='__main__':
    app.run()

