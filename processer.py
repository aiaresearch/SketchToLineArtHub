import base64
import cv2
import numpy as np
import os


if __name__ == "__main__":  # not import but strightlt run the script

    a = np.random.randint(0, 225, (25, 25, 3))
    a = a.astype("uint8")
    cv2.imshow("Noise", a)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


class Processer(object):
    def __init__(self, config_dic={}):
        '''
        #self.dirs = dirs
        #self.pathself = pathself
        #self.dir_pathself = dir_pathself
        self.blur_num = 5#均值滤波核边长大小
        #gaussian二值化参数
        self.gaussian_wide = 3#阈值计算邻域
        self.gaussian_decrement = 10
        #canny边缘检测参数
        self.canny_threshold1 = 60#下阈值，边缘强度低于此者判为非边缘
        self.canny_threshold2 = 170
        self.canny_wide = 3#sobel算子大小(1,3,5,7)
        '''

        self.__dict__.update(config_dic)

    def set_config(self, config_dic={}):
        self.__dict__.update(config_dic)

    def read_in(self, img):  # 读入灰度图
        img = cv2.imread(img,
                         cv2.IMREAD_GRAYSCALE)
        return img

    def read_in_fold(self, fold_path):
        img_lib = os.listdir(fold_path)  # 读取该文件夹中文件名
        pic_lib = []
        for i in img_lib:
            pic_lib.append(self.read_in(fold_path+'/'+i))
        return pic_lib

    def read_in_html(self, img):
        img = cv2.imdecode(np.fromstring(
            img.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        return img

    def read_in_base64(self, img):
        print(img.type)
        print(img)
        img = img.split(',', maxsplit=1)[1]
        img = base64.b64decode(img)  # base64解码
        img_array = np.frombuffer(img, np.uint8)  # 转换np序列
        img = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)  # 转换Opencv格式

        return img

    def out_base64(self, cv2_image):
        image = cv2.imencode('.jpg', cv2_image)[1]
        base64_data = str(base64.b64encode(image))[2:-1]

        return base64_data

    def median_blur(self, img):  # 中值模糊
        img = cv2.medianBlur(img, self.blur_num)  # denoise by medianBlur
        return img

    def method_color(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                if img[x, y, 0] < 254:
                    img[x, y, 0] = self.color[0]
                if img[x, y, 1] < 254:
                    img[x, y, 1] = self.color[1]
                if img[x, y, 2] < 254:
                    img[x, y, 2] = self.color[2]

        return img

    def method_binarization(self, img):  # 高斯自适应二值化
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, self.gaussian_wide, self.gaussian_decrement)
        return img

    def method_canny(self, img):  # canny应用
        img = 255 - cv2.Canny(img,
                              self.canny_threshold1, self.canny_threshold2, self.canny_wide)
        return img

    def method_sobel(self, img):  # sobel应用
        img = self.median_blur(img)
        imgx = cv2.Sobel(img, cv2.CV_8U, 1, 0, self.soble_size)
        imgy = cv2.Sobel(img, cv2.CV_8U, 0, 1, self.soble_size)
        img = 255 - cv2.addWeighted(imgx, 0.5, imgy, 0.5, 0)
        if self.flag_binary == True:
            img = cv2.threshold(img, self.binary_threshold, 255, cv2.THRESH_BINARY)[
                1]  # 此简单二值化函数返回2值元组
        return img

    def method_laplacian(self, img):
        img = self.median_blur(img)
        img = 255 - cv2.Laplacian(img, cv2.CV_8U)
        if self.flag_binary == True:
            img = cv2.threshold(img, self.binary_threshold, 255, cv2.THRESH_BINARY)[
                1]  # 此简单二值化函数返回2值元组
        return img

    def img_save(self, img, img_name, dir_path):
        cv2.imwrite(dir_path + '/default/%s' % img_name, img)

    def img_imshow(self, img, img_name, dir_path):
        cv2.namedWindow("'Esc' to exit,'s' to save", cv2.WINDOW_NORMAL)
        cv2.imshow("'Esc' to exit,'s' to save", img)
        k = cv2.waitKey(0)
        if k == 27:
            cv2.destroyAllWindows()
        elif k == ord('s'):  # wait for 's' key to save and exit
            self.img_save(img, img_name, dir_path)
            cv2.destroyAllWindows()
        return
