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
import numpy as np
import cv2
import pickle

# 日志设置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
i = 0


def run():
    # 客户端配置
    client_cfg = IoTClientConfig(server_ip='b302707e19.st1.iotda-device.cn-north-4.myhuaweicloud.com',
                                 device_id='66b860c0f1d7e406fa9395f9_M2M_DEVICE1',
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

    def publish_periodically():
        while True:
            location = [123, 123, 123]
            iot_client.publish_message(r'/test/M2M/device2/location', change2base64(location))

            direct = 234
            iot_client.publish_message(r'/test/M2M/device2/direct', change2base64(direct))

            battery = 99
            iot_client.publish_message(r'/test/M2M/device2/battery', change2base64(battery))

            work_mode = 1
            iot_client.publish_message(r'/test/M2M/device2/work_mode', change2base64(work_mode))

            time.sleep(10)

    # 订阅自定义topic
    time.sleep(2)
    topic = r'/test/M2M/GUI'
    iot_client.subscribe(topic)
    # logger.info('订阅主题: {}'.format(topic))
    # 设备接收平台下发消息的回调函数
    time.sleep(1)

    def message_callback(device_message):
        global i
        received_string = device_message.content
        receive_topic = device_message.topic
        print("进入中断")
        print(receive_topic)
        print(received_string)

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
