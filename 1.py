import os
import json
import time
from pywebio import STATIC_PATH, config
import pywebio

from PIL import Image
from pywebio.platform import path_deploy, path_deploy_http
from torchvision import transforms
import matplotlib.pyplot as plt

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import put_input, pin_wait_change, pin
from pywebio.session import info as session_info

folder_path = './himg/'
index = 0


def saveimgA(r, name):
    typeA = "行程卡"
    img_name = folder_path + name + typeA + '.jpg'

    with open(img_name, 'wb') as file:  # 以byte形式将图片数据写入
        file.write(r)
        file.flush()
        file.close()  # 关闭文件

    return img_name


def saveimgB(r, name):
    global index
    typeb = "穗康码"
    img_name = folder_path + name + typeb + '.jpg'
    index = index + 1

    with open(img_name, 'wb') as file:  # 以byte形式将图片数据写入
        file.write(r)
        file.flush()
        file.close()  # 关闭文件

    return img_name


def saveimgC(r, name):
    global index
    typeb = "核酸证明"
    img_name = folder_path + name + typeb + '.jpg'
    index = index + 1

    with open(img_name, 'wb') as file:  # 以byte形式将图片数据写入
        file.write(r)
        file.flush()
        file.close()  # 关闭文件

    return img_name


@config(theme="dark", title='19计科4班返校签到')
def main():
    put_markdown(' # 计科4班返校签到 ')
    put_markdown((""" 
## code by zxk 


![](https://pic.imgdb.cn/item/6245732a27f86abb2a5b2ae0.gif)

## ReadMe

声明:本网站保证仅收集同学们的返校信息,无任何病毒 放心使用 
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
请同学们按照顺序，输入姓名-上传行程卡-穗康码 即可
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
如果图片上传错误,不要退出页面 ,重新在页面上传一次既可,会覆盖之前的图片。











## 上传界面




    """), )
    name = input('请输入姓名', type=TEXT)
    put_success(name + "已签到")

    file = open("./himg/qiandao.txt", mode='a')
    file.write(name + '\n')
    while True:
        data = input_group("上传界面-注意顺序", [
            file_upload("上传行程卡 ", placeholder='在此上传行程卡', accept="image/*", multiple=False, name="imgsA"),
            file_upload("上传穗康码", placeholder='在此上传穗康码', accept="image/*", multiple=False, name="imgsB"),
            file_upload("上传核酸结果", placeholder='在此上传核酸证明', accept="image/*", multiple=False, name="imgsC")
        ], )
        print(data['imgsA']['filename'])
        # imgsA= file_upload("上传行程卡 ", placeholder='同学们不要重复上传', accept="image/*", multiple=False)
        # imgsB= file_upload("上传穗康码", placeholder='同学们不要重复上传', accept="image/*", multiple=False)
        # print(imgsA)
        # 'filename': 文件名，
        # 'content'：文件二进制数据(bytes
        # object),
        # 'mime_type': 文件的MIME类型,
        # 'last_modified': 文件上次修改时间(时间戳)
        out1 = saveimgA(data['imgsA']['content'], name)
        out2 = saveimgB(data['imgsB']['content'], name)
        out3 = saveimgC(data['imgsC']['content'], name)
        with put_loading(shape='border', color='primary'):
            time.sleep(4)

        put_collapse('行程卡上传结果', [
            put_image(data['imgsA']['content'], ),
            put_text(name + "行程卡")

        ], open=False)

        put_collapse('穗康码上传结果', [

            put_image(data['imgsB']['content'], ),
            put_text(name + "穗康码")

        ], open=False)

        put_collapse('核酸证明上传结果', [

            put_image(data['imgsC']['content'], ),
            put_text(name + "核酸证明")

        ], open=False)

        put_text("谢谢！！ 请打开折叠内容检查是否上传正确，无误后可以关闭网站。0_0")


if __name__ == '__main__':
    start_server(main, debug=True, auto_open_webbrowser=True, port=8084)

