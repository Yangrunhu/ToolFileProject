#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2021/5/26 8:57
# @Author  : Silent_YangRun
# @Site    : 
# @File    : optical_character_recognition.py
# @Software: PyCharm

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 对图片进行切割
img = Image.open("./TestToolDirectory/test_img3.jpg")

cropped = img.crop((0, img.size[0] / 1.15, img.size[0], img.size[1] - 610))  # (left, upper, right, lower)
# cropped.show()
cropped.save('./TestToolDirectory/2.jpg')

# 分割图片
image = cv2.imread('./TestToolDirectory/2.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换了灰度化
ret, img = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)  # 将灰度图像二值化
img = 255 - img
cv2.imshow("img", img)
cv2.waitKey()

# 腐蚀图片
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (7, 7))
img = cv2.dilate(img, kernel)
h, w = img.shape
cv2.imshow("img", img)
cv2.waitKey()


# 垂直反向投影
def vProject(binary):
    h, w = binary.shape
    # 创建 w 长度都为0的数组
    w_w = [0] * w
    for i in range(w):
        for j in range(h):
            if binary[j, i] == 255:
                w_w[i] += 255
    plt.plot(range(w), w_w)
    plt.show()
    return w_w


w_w = vProject(img)
position = []
# w_start,w_end是记录垂直投影后白色块的x轴开始坐标和x轴结束坐标
# wstart,wend是记录白色块的开始标志和结束标志，开始记录时wstart=1,结束时wend=1
wstart, wend, w_start, w_end = 0, 0, 0, 0
for j in range(len(w_w)):
    if w_w[j] > 0 and wstart == 0:
        w_start = j
        wstart = 1
        wend = 0
    if w_w[j] == 0 and wstart == 1:
        w_end = j
        wstart = 0
        wend = 1

    # 当确认了起点和终点之后保存坐标[x1,y1,x2,y2]
    if wend == 1:
        position.append([w_start, 0, w_end, h - 1])
        wend = 0

# 其中(x1,y1)为左边的点，(x2,y2)为右边的点
for p in position:
    cv2.rectangle(image, (p[0], p[1]), (p[2], p[3]), (255, 0, 255), 2)
cv2.imshow('image', image)
cv2.waitKey(0)

# 定义橘色识别模型
lower_orange = np.array([11, 43, 46])
upper_orange = np.array([25, 255, 255])
# RGB 转 HSV 颜色模型
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 低于lower_orange/高于upper_orange的值，图像值为0
# 在此之间的值变成255，即涂白色
mask = cv2.inRange(hsv, lower_orange, upper_orange)
cv2.imshow('image', mask)
cv2.waitKey(0)

binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]  # 将灰度图像二值化
binary = cv2.dilate(binary, None, iterations=2)  # 图像膨胀

# cv2的版本不同,findContours的返回值个数也不一样，此处是为了兼容不同版本
if int(cv2.__version__[0]) > 2:
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
else:
    _, contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 3-求轮廓的面积
# sum = 0
# space = img.shape[0] * img.shape[1]
# for cts in contours:
#     sum += cv2.contourArea(cts)
# print("面积占比:", sum / space)
# if sum / space > 0.3:  # 这里假定是30%，
#     print("get orange SUCCESS！")

# 注意图片块用[y1,y2,x1,x2]来获取
# img = image[imgPos[1]:imgPos[3],imgPos[0]:imgPos[2]]
