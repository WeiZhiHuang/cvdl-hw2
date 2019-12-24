import os
import sys
import cv2
import PyQt5
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from Ui_main import Ui_Form as Ui_main


# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_depthmap/py_depthmap.html
def showDisparity():
    imgL = cv2.imread('resources/imL.png', 0)
    imgR = cv2.imread('resources/imR.png', 0)

    stereo = cv2.StereoBM_create(numDisparities=64, blockSize=9)
    disparity = stereo.compute(imgL, imgR)
    plt.imshow(disparity, 'gray')
    plt.xticks([]), plt.yticks([])
    plt.show()


# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
def showNCC():
    img_rgb = cv2.imread('resources/ncc_img.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('resources/ncc_template.jpg', 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = .97
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    plt.imshow(res, cmap='gray')
    plt.xticks([]), plt.yticks([])
    plt.show()
    plt.imshow(cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB))
    plt.xticks([]), plt.yticks([])
    plt.show()



if __name__ == '__main__':
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
        os.path.dirname(PyQt5.__file__), 'Qt', 'plugins', 'platforms')
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_main()
    ui.setupUi(Widget)

    ui.pushButton.clicked.connect(showDisparity)
    ui.pushButton_2.clicked.connect(showNCC)

    Widget.show()
    sys.exit(app.exec_())
