# !/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image
from PIL import ImageEnhance
import pytesseract


def identyImg():

    image = Image.open("C:/img/tn15.png")
    image2 = image.convert("RGB")
    print(image2.mode, image2.size, image2.format)
    # image.show()

    enh_bright = ImageEnhance.Brightness(image2)
    bright = 1.5
    img_bright = enh_bright.enhance(bright)
    # img_bright.show()

    enh_col = ImageEnhance.Color(img_bright)
    col = 1.5
    image_colored = enh_col.enhance(col)
    # image_colored.show()

    enh_con = ImageEnhance.Contrast(image2)
    contrast = 1.5
    enh_contrast = enh_con.enhance(contrast)
    # enh_contrast.show()

    enh_sha = ImageEnhance.Sharpness(enh_contrast)
    sharpness = 3.0
    image_sharped = enh_sha.enhance(sharpness)
    # image_sharped.show()

    image.save("handle.png")
    code = pytesseract.image_to_string(Image.open("handle.png"), lang="fontyp", config="-psm 7")
    # code = pytesseract.image_to_string(Image.open(path), lang="chi_sim3")
    return code

# server.run(port=8000, host='0.0.0.0')
if __name__ == '__main__':
    result = identyImg()
    print(result)
