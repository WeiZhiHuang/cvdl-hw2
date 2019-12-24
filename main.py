import os
import sys
import cv2
import PyQt5
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from Ui_main import Ui_Form as Ui_main


# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_depthmap/py_depthmap.html#code
def showDisparity():
    imgL = cv2.imread('resources/imL.png', 0)
    imgR = cv2.imread('resources/imR.png', 0)

    stereo = cv2.StereoBM_create(numDisparities=64, blockSize=9)
    disparity = stereo.compute(imgL, imgR)
    plt.imshow(disparity, 'gray')
    plt.show()


if __name__ == '__main__':
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
        os.path.dirname(PyQt5.__file__), 'Qt', 'plugins', 'platforms')
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_main()
    ui.setupUi(Widget)

    ui.pushButton.clicked.connect(showDisparity)

    Widget.show()
    sys.exit(app.exec_())
