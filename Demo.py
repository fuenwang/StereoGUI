import os
import sys
import cv2
import glob
import Stereo
import functools
import numpy as np
from PyQt4 import QtCore, QtGui

DEMO_ROOT = '%s/demo' % os.path.abspath(os.path.dirname(__file__))


class FrameMacro:

    def __init__(self, path, height, width):
        self.width = width
        self.height = height
        self.frame_lst = sorted(glob.glob('%s/*' % path))
        self.idx = 0

    def Next(self):
        if self.idx < len(self.frame_lst):
            idx = self.idx
            self.idx += 1
        else:
            idx = 0
            self.idx = 0
        return self.frame_lst[idx]


def PlayFrame_thread(label, macro):
    path = macro.Next()
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (macro.width, macro.height))
    pixmap = Stereo.toPixmap(img)
    label.setPixmap(pixmap)


def PlayFrame(obj):
    obj.clearLayout()
    h, w = Stereo.Geometry(obj)

    frame_path = '%s/video' % DEMO_ROOT
    frameMacro = FrameMacro(frame_path, h, w)

    layout = QtGui.QHBoxLayout(obj)
    layout.setContentsMargins(0, 0, 0, 0)

    label = QtGui.QLabel(obj)
    layout.addWidget(label)
    timer = QtCore.QTimer(obj)
    obj.timer.append(timer)
    timer.timeout.connect(functools.partial(
        PlayFrame_thread, label, frameMacro))
    timer.start(200)

def CaptureWebcam_thread(label, capture, h, w):
    img = capture.read()
    img = cv2.resize(img[1], (w, h))
    label.setPixmap(Stereo.toPixmap(img))

def CaptureWebcam(obj):
    obj.clearLayout()
    h, w = Stereo.Geometry(obj)
    try:
        capture = cv2.VideoCapture(0)
    except:
        return 
    layout = QtGui.QHBoxLayout(obj)
    layout.setContentsMargins(0, 0, 0, 0)

    label = QtGui.QLabel(obj)
    layout.addWidget(label)
    timer = QtCore.QTimer(obj)
    timer.timeout.connect(functools.partial(CaptureWebcam_thread, label, capture, h, w))
    obj.timer.append(timer)
    timer.start(50)














