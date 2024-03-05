import processer
import os
import json

pathself = os.path.abspath(__file__)  # 当前脚本绝对路径
dir_pathself = os.path.dirname(pathself)  # 当前脚本所处文件夹绝对路径

with open('parameter\\parameter.txt', 'r') as file:
    content = file.read()

p_dic = {'blur_num': 5,  # 中值滤波核边长大小
         # gaussian二值化参数
         'gaussian_wide': 3,  # 阈值计算邻域
         'gaussian_decrement': 10,  # 计算得阈值作差
         # canny边缘检测参数
         'canny_threshold1': 60,  # 下阈值，边缘强度低于此者判为非边缘
         'canny_threshold2': 170,
         'canny_wide': 3,  # sobel算子大小(1,3,5,7)
         # sobel边缘检测参数及laplacian边缘检测参数
         'soble_size': 5,
         'flag_binary': True,  # 在使用soble和laplacian边缘检测后是否将灰度图二值化
         'binary_threshold': 240,  # 二值化阈值，亮度高于此则为白
         # method_color函数参数
         'color': [0, 100, 0],  # 线条颜色
         # method
         'method': 'laplacian'
         }

p_dic.update(json.loads(content))

method_list = ['高斯自适应阈值二值化', 'laplacian', 'sobel', 'canny']
Pcer = processer.Processer(p_dic)
Pcer.set_config(p_dic)
dirs = os.listdir()  # 当前脚本所在文件夹所含文件

img_lib = os.listdir(dir_pathself + '/' + 'bin')
img_order_list = []
for a in range(0, len(img_lib)):
    img_order_list.append('(%s)' % a + img_lib[a])  # 将图片名读入列表


def para_set():
    global p_dic
    if input('Do u set the method(y/n)当前为:%s:' % p_dic['method']) == 'y':
        for i in range(len(method_list)):
            print('%s-->' % str(i) + method_list[i])
        try:
            p_dic['method'] = method_list[int(input('Select the num:'))]
        except:
            None
    if input('Do u set the parameter(y/n):') == 'y':
        print('不改项回车跳过,显示数为当前值')
        if p_dic['method'] == '高斯自适应阈值二值化':
            try:
                p_dic['blur_num'] = int(
                    input('均值滤波卷积核(1,3,5,7)当前为:%s:' % p_dic['blur_num']))
            except:
                None
            try:
                p_dic['guassian_wide'] = int(
                    input('高斯二值化采样区(3-30):%s:' % p_dic['guassian_wide']))
            except:
                None
            try:
                p_dic['gaussian_decrement'] = int(
                    input('高斯二值化阈值差量:%s:' % p_dic['gaussian_decrement']))
            except:
                None
        elif p_dic['method'] == 'canny':
            try:
                p_dic['canny_threshold1'] = int(
                    input('canny低阈值(50-110):%s:' % p_dic['canny_threshold1']))
            except:
                None
            try:
                p_dic['canny_threshold2'] = int(
                    input('canny高阈值(150-200)%s:' % p_dic['canny_threshold2']))
            except:
                None
            try:
                p_dic['canny_wide'] = int(
                    input('canny卷积核:%s:' % p_dic['canny_wide']))
            except:
                None
        elif p_dic['method'] == 'laplacian' or p_dic['method'] == 'sobel':
            try:
                p_dic['soble_size'] = int(
                    input('sobel卷积核:%s:' % p_dic['soble_size']))
            except:
                None
            if input('laplacian or sobel处理是否启用二值化(y/n):%s:' % p_dic['flag_binary']) == 'y':
                p_dic['flag_binary'] = True
                try:
                    p_dic['binary_threshold'] = int(
                        input('二值化阈值:%s:' % p_dic['binary_threshold']))
                except:
                    None
            else:
                p_dic['flag_binary'] = False
    print(p_dic)
    Pcer.set_config(p_dic)


def select():
    for i in range(len(img_order_list)):
        print(img_order_list[i])
    try:
        o_num = int(input('order number of picture u want(from 0 to n):'))
    except:
        o_num = 0
    return o_num


def process(img, method):

    if method == '高斯自适应阈值二值化':
        img = Pcer.method_binarization(img)
    elif method == 'sobel':
        img = Pcer.method_sobel(img)
    elif method == 'laplacian':
        img = Pcer.method_laplacian(img)
    elif method == 'canny':
        img = Pcer.method_canny(img)

    img = Pcer.method_color(img)

    return img


def main():
    global p_dic
    while 1:
        para_set()
        selection = img_lib[select()]
        img = Pcer.read_in('bin\\' + selection)

        img = process(img, p_dic['method'])
        Pcer.img_imshow(img, 'sket' + selection, dir_pathself)

        if input("One more time by input'y':") != 'y':
            return 'Goodbye'


main()


'''
example = cv2.imread('bin/trash.png',\
                    cv2.IMREAD_GRAYSCALE)
example1 = Pcer.method_binarization(example)

result = Pcer.read_in_fold('bin')

a = Pcer.method_laplacian(result[8])
a = Pcer.method_color(a)

cv2.imshow('c', a) 
cv2.waitKey(0)

def main():
    while True:
        None
'''
