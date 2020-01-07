import os, stat
import urllib.request


img_url = "http://ceb2pub.chinaport.gov.cn/verifyCode/creator"
file_path = 'D:/capture/test'
file_name = "capture"


for i in range(800):
    try:
        # 是否有这个路径
        if not os.path.exists(file_path):
            # 创建路径
            os.makedirs(file_path)
            # 获得图片后缀
        file_suffix = os.path.splitext(img_url)[1]
        print(file_suffix)
        # 拼接图片名（包含路径）
        filename = '{}{}{}{}'.format(file_path, os.sep, i, ".jpg")
        print(filename)
        # 下载图片，并保存到文件夹中
        urllib.request.urlretrieve(img_url, filename=filename)

    except IOError as e:
        print("IOError")
    except Exception as e:
        print("Exception")
