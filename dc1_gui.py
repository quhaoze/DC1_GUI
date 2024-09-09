# request：包含前端发送过来的所有请求数据
import logging
import time
import threading
from IoT_device.client import IoTClientConfig, IotClient
import base64
import pickle
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

client_cfg = IoTClientConfig(server_ip='9904a57d85.st1.iotda-device.cn-north-4.myhuaweicloud.com',
                             device_id='66d3024ef1d7e406fa978968_device3_GUI',
                             secret='12345678', is_ssl=False)
iot_client = IotClient(client_cfg)
iot_client.connect()  # 建立连接


def change2base64(a):
    serialized_1 = pickle.dumps(a)
    base_64_a = base64.b64encode(serialized_1)
    return base_64_a


def change2original(a):
    receive_data = base64.b64decode(a)
    list_2 = pickle.loads(receive_data)
    return list_2


def publish_periodically():
    while True:
        work_mode = 1
        iot_client.publish_message(r'/test/M2M/GUI/device1', str(change2base64(work_mode)))
        # change2base64这个函数本身是没有问题的，但是publish——message是需要传入str的，这里做一下强制转换就行
        time.sleep(100)


# 订阅自定义topic
time.sleep(2)
topic_list = [r'/test/M2M/device1']
iot_client.subscribe(topic_list)
# logger.info('订阅主题: {}'.format(topic))
# 设备接收平台下发消息的回调函数
time.sleep(1)


def message_callback(device_message):
    print("收到消息")
    received_content = device_message.content
    # receive_topic = device_message.topic
    print(change2original(eval(received_content)))


# 设置平台下发自定义topic消息响应的回调
iot_client.set_user_topic_message_callback(message_callback)
# logger.debug('回调函数已设置')

# 创建线程来定时发布消息
periodic_thread = threading.Thread(target=publish_periodically)
periodic_thread.daemon = True  # 设置守护线程，这样可以在主线程结束时自动退出
periodic_thread.start()
iot_client.start()  # 线程启动

# 用当前脚本名称实例化Flask对象，方便flask从该脚本文件中获取需要的内容
app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print("客户端已连接")
    emit('server_message_locate', {'data': '已经连接到websocket服务器'})
    emit('server_message_battery', {'data': '已经连接到websocket服务器'})
    emit('server_message_workmode', {'data': '已经连接到websocket服务器'})


@app.route("/", methods=['GET', 'POST'])
# url映射的函数，要传参则在上述route（路由）中添加参数申明
# 不带参数时，最大区别仅仅是第一行方法名不同，一个是GET，一个是POST
# 带参数时报文的区别呢？在约定中，GET 方法的参数应该放在 url 中，POST 方法参数应该放在 body 中

# 下面这个函数与上面那个相绑定
def index():
    if request.method == 'GET':
        # 想要html文件被该函数访问到，首先要创建一个templates文件，将html文件放入其中
        # 该文件夹需要被标记为模板文件夹，且模板语言设置为jinja2
        return render_template('DC1.html')
    # 此处欲发送post请求，需要在对应html文件的form表单中设置method为post
    elif request.method == 'POST':
        command1 = request.form.get('command1')
        command2 = request.form.get('command2')
        print(command1)
        print(command2)
        if command1 == "1" and command2 == "1":
            iot_client.publish_message(r'/test/M2M/GUI/device1', "按下了按钮1")
            print("已向华为云平台发送消息：按下了按钮1")
        return "Commands received", 200


if __name__ == '__main__':
    app.run()
