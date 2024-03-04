import subprocess
from flask import Flask, render_template, request, redirect, url_for, jsonify
import processer
import json
import cv2
import os, sys
import socket
with open('parameter/parameter.txt', 'r') as file:
    content = file.read()

dir_pathself = os.path.split(os.path.realpath(__file__))[0]
print(dir_pathself)
p_dic = {'blur_num':5,#中值滤波核边长大小
         #gaussian二值化参数
         'gaussian_wide':3,#阈值计算邻域
         'gaussian_decrement':10,#计算得阈值作差
         #canny边缘检测参数
         'canny_threshold1':60,#下阈值，边缘强度低于此者判为非边缘
         'canny_threshold2':170,
         'canny_wide':3,#sobel算子大小(1,3,5,7)
         #sobel边缘检测参数及laplacian边缘检测参数
         'soble_size':5,
         'flag_binary':True,#在使用soble和laplacian边缘检测后是否将灰度图二值化
         'binary_threshold':240,#二值化阈值，亮度高于此则为白
         #method_color函数参数
         'color':[0,0,0],#线条颜色
         #method
         'method':'laplacian' 
         }

p_dic.update(json.loads(content))

Pcer = processer.Processer(p_dic)
Pcer.set_config(p_dic)

app = Flask(__name__, template_folder=  'templates')

def get_local_ip():
    # 创建一个套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # 连接到一个外部的IP地址和端口
        s.connect(("8.8.8.8", 80))
        
        # 获取本地IP地址
        local_ip = s.getsockname()[0]
    except socket.error as e:
        print("获取本地IP地址失败:", e)
        local_ip = "无法获取本地IP地址"
    finally:
        s.close()
    
    return local_ip

ip = get_local_ip()

url = 'http://127.0.0.1:5000/start'
command = f'start {url}'
subprocess.run(command, shell=True)



@app.route('/')
def index():
    return render_template('drawing.html', url = 'http://'+ip+':5000/setting')

@app.route('/start')
def index1():
    #ip_json = jsonify(ip=ip)  
    return render_template('start.html', url = 'http://'+ip+':5000/')  


@app.route('/setting')
def index2():
    parameter_dict = {
            "mean-filter-size": 5,
            "gaussian-wide": 25,
            "gaussian-decrement": 10,
            "canny-threshold1": 60,
            "canny-threshold2": 170,
            "canny-wide": 1,
            "color": [0, 0, 0]
            }
    return render_template('main.html',
    url = 'http://'+ip+':5000/',
    parameter_dict=parameter_dict)




@app.route('/dict', methods=['POST'])
def save_dict():
    para_dict = request.form.get('para_dict')

    selected_p = json.loads(para_dict)
    print(selected_p['color'])
    
    Pcer.set_config(selected_p)

    return jsonify({'message': "参数更新完毕"})
    
@app.route('/api/endpoint', methods=['POST'])
def process_image():
    print('sth')
    image_file = request.files.get('imageFile')
    print(image_file)

    # 处理接收到的图像文件

    img = Pcer.read_in_html(image_file)
    # 使用cv2进行了图像处理，得到了处理后的图像image
    
    if Pcer.method == 'sobel':img = Pcer.method_sobel(img)
    elif Pcer.method == 'laplacian':img = Pcer.method_laplacian(img)
    elif Pcer.method == 'canny':img = Pcer.method_canny(img)
    else:img = Pcer.method_binarization(img)

    image = Pcer.method_color(img)

    # 将图像转换为Base64编码的字符串
    processed_image_base64 = Pcer.out_base64(image)
    print(Pcer.method)

    # 返回处理后的图像数据
    return jsonify({'processedImage': processed_image_base64})


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
