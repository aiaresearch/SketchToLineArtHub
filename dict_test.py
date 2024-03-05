class Processer():
    def __init__(self, config_dic={}):
        self.canny_thres1 = 2
        self.canny_thres2 = 3
        self.__dict__.update(config_dic)

    def process(self, img_path):
        print(f"INFO: Processing image in {img_path} with canny_thres1={
              self.canny_thres1} canny_thres2={self.canny_thres2}")


if __name__ == '__main__':
    p = Processer(config_dic={'canny_thres1': 4})
    p.process("./example.jpg")
