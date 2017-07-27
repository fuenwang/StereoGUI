import os
import sys
import cv2
import time
import random
import threading
import functools
import numpy as np
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
from PyQt4 import QtCore, QtGui


def toPixmap(img):
    try:
        h, w, c = img.shape
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    except:
        h, w = img.shape
        c = 3
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    pixmap = QtGui.QImage(img.data, w, h, c * w, QtGui.QImage.Format_RGB888)
    return QtGui.QPixmap.fromImage(pixmap)


def Geometry(obj):
    height = obj.frameGeometry().height()
    width = obj.frameGeometry().width()

    return [height, width]


def ChangeFigure(label1, label2, pixmap1, pixmap2):
    idx = random.choice([0, 1])
    if idx == 0:
        label1.setPixmap(pixmap1)
        label2.setPixmap(pixmap2)
    else:
        label1.setPixmap(pixmap2)
        label2.setPixmap(pixmap1)


def ShowStereo(obj):
    obj.clearLayout()
    height, width = Geometry(obj)
    #lst = obj.getOpenFileNames()
    lst = ['/Users/fu-en.wang/Desktop/Classroom1-imperfect/imL.png',
           '/Users/fu-en.wang/Desktop/Classroom1-imperfect/imR.png']
    if len(lst) != 2:
        print 'Image List Error!'
    else:
        left_name = lst[0]
        right_name = lst[1]

        left = cv2.imread(left_name, cv2.IMREAD_COLOR)
        right = cv2.imread(right_name, cv2.IMREAD_COLOR)

        h, w, _ = left.shape
        toH = int(0.5 * height)
        toW = int(0.5 * width)

        left = cv2.resize(left, (toW, toH))
        right = cv2.resize(right, (toW, toH))
        l_pixmap = toPixmap(left)
        r_pixmap = toPixmap(right)

        l_label = QtGui.QLabel()
        l_label.setPixmap(l_pixmap)

        r_label = QtGui.QLabel()
        r_label.setPixmap(r_pixmap)

        vlayout_top = QtGui.QHBoxLayout()
        vlayout_top.setSpacing(0)
        vlayout_top.setContentsMargins(0, 0, 0, 0)
        vlayout_top.addWidget(l_label)
        vlayout_top.addWidget(r_label)

        layout = QtGui.QVBoxLayout(obj)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addLayout(vlayout_top)

        timer = QtCore.QTimer(obj)
        obj.timer.append(timer)
        timer.timeout.connect(functools.partial(
            ChangeFigure, l_label, r_label, l_pixmap, r_pixmap))
        timer.start(100)


def ShowDisparity(obj):
    obj.clearLayout()
    height, width = Geometry(obj)
    #lst = obj.getOpenFileNames()
    lst = ['/Users/fu-en.wang/Desktop/Classroom1-imperfect/imL.png',
           '/Users/fu-en.wang/Desktop/Classroom1-imperfect/imR.png']
    if len(lst) != 2:
        print 'Image List Error!'
    else:
        left_name = lst[0]
        right_name = lst[1]

        left = cv2.imread(left_name, cv2.IMREAD_COLOR)
        right = cv2.imread(right_name, cv2.IMREAD_COLOR)

        left_gray = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
        right_gray = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
        stereo = cv2.StereoBM(preset=0, ndisparities=16, SADWindowSize=5)
        disparity = stereo.compute(
            left_gray, right_gray, disptype=cv2.CV_32FC1)

        h, w, _ = left.shape
        toH = int(0.5 * height)
        toW = int(0.5 * width)

        disparity[disparity == -1] = 0
        disparity /= (disparity.max() / 255.0)
        disparity = disparity.astype(np.uint8)
        disparity_bone = cv2.applyColorMap(disparity, cv2.COLORMAP_BONE)
        disparity_winter = cv2.applyColorMap(disparity, cv2.COLORMAP_AUTUMN)

        left = cv2.resize(left, (toW, toH))
        right = cv2.resize(right, (toW, toH))
        disparity_bone = cv2.resize(disparity_bone, (toW, toH))
        disparity_winter = cv2.resize(disparity_winter, (toW, toH))
        l_pixmap = toPixmap(left)
        r_pixmap = toPixmap(right)
        disparity_bone_pixmap = toPixmap(disparity_bone)
        disparity_winter_pixmap = toPixmap(disparity_winter)

        l_label = QtGui.QLabel()
        l_label.setPixmap(l_pixmap)

        r_label = QtGui.QLabel()
        r_label.setPixmap(r_pixmap)

        disparity_label1 = QtGui.QLabel()
        disparity_label1.setPixmap(disparity_bone_pixmap)
        disparity_label2 = QtGui.QLabel()
        disparity_label2.setPixmap(disparity_winter_pixmap)

        vlayout_top = QtGui.QHBoxLayout()
        vlayout_top.setSpacing(0)
        vlayout_top.setContentsMargins(0, 0, 0, 0)
        vlayout_top.addWidget(l_label)
        vlayout_top.addWidget(r_label)

        vlayout_bot = QtGui.QHBoxLayout()
        vlayout_bot.setSpacing(0)
        vlayout_bot.setContentsMargins(0, 0, 0, 0)
        vlayout_bot.addWidget(disparity_label1)
        vlayout_bot.addWidget(disparity_label2)

        layout = QtGui.QVBoxLayout(obj)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addLayout(vlayout_top)
        layout.addLayout(vlayout_bot)
