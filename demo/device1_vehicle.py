# -*- encoding: utf-8 -*-
'''
消息传送demo
包括订阅topic

发布消息
'''

import logging
import time
import threading
from IoT_device.client import IoTClientConfig, IotClient
import base64
import pickle
# 日志设置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
i = 0


def run():
    # 客户端配置
    client_cfg = IoTClientConfig(server_ip='9904a57d85.st1.iotda-device.cn-north-4.myhuaweicloud.com',
                                 device_id='66d3024ef1d7e406fa978968_decive1_vehicle',
                                 secret='12345678', is_ssl=False)
    # 创建设备
    iot_client = IotClient(client_cfg)
    iot_client.connect()  # 建立连接

    '''
    发送自定义topic消息
    '''

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
            location = [123,123,123,['abc']]
            iot_client.publish_message(r'/test/M2M/device1', str(change2base64(location)))

            time.sleep(10)


    # 订阅自定义topic
    time.sleep(2)
    topic = r'/test/M2M/GUI'
    iot_client.subscribe(topic)
    # logger.info('订阅主题: {}'.format(topic))
    # 设备接收平台下发消息的回调函数
    time.sleep(1)

    def message_callback(device_message):
        print("收到消息")
        received_content = device_message.content
        #receive_topic = device_message.topic
        print(change2original(received_content))
        #print(change2original(receive_topic))



    # 设置平台下发自定义topic消息响应的回调
    iot_client.set_user_topic_message_callback(message_callback)
    # logger.debug('回调函数已设置')







    # 创建线程来定时发布消息
    periodic_thread = threading.Thread(target=publish_periodically)
    periodic_thread.daemon = True  # 设置守护线程，这样可以在主线程结束时自动退出
    periodic_thread.start()
    iot_client.start()  # 线程启动

if __name__ == '__main__':
    run()
