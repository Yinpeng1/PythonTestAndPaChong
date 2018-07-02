from PIL import Image
from PIL import ImageEnhance
import pytesseract
import os


def image_file_to_string(file):
    cwd = os.getcwd()
    try:
        os.chdir("C:/img/tn.png")
        return pytesseract.image_file_to_string(file)
    finally:
        os.chdir(cwd)


im = Image.open("C:/img/tn.png")
imgry = im.convert('L')  # 图像加强，二值化
sharpness = ImageEnhance.Contrast(imgry)  # 对比度增强
sharp_img = sharpness.enhance(2.0)
sharp_img.save("C:/img/tn1234.png")
# http://www.cnblogs.com/txw1958/archive/2012/02/21/2361330.html
# imgry.show()#这是分布测试时候用的，整个程序使用需要注释掉
# imgry.save("E:\\image_code.jpg")

code = pytesseract.image_to_string("C:/img/tn1234.png")  # code即为识别出的图片数字str类型
print(code)
# 打印code观察是否识别正确
