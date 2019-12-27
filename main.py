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


# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html
def showKeypoints():
    img1 = cv2.imread('resources/Aerial1.jpg', 0)
    img2 = cv2.imread('resources/Aerial2.jpg', 0)

    # Initiate SIFT detector
    sift = cv2.xfeatures2d_SIFT.create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    kp1 = sorted(kp1, key=lambda x: x.size, reverse=True)[:7]
    kp2 = sorted(kp2, key=lambda x: x.size, reverse=True)[:7]

    img1 = cv2.drawKeypoints(img1, kp1, None, (0, 255, 0))
    cv2.imwrite('output/FeatureAerial1.jpg', img1)
    img2 = cv2.drawKeypoints(img2, kp2, None, (0, 255, 0))
    cv2.imwrite('output/FeatureAerial2.jpg', img2)

    plt.figure(figsize=(4, 6))
    plt.xticks([]), plt.yticks([])
    plt.imshow(img1), plt.show()
    plt.figure(figsize=(4, 6))
    plt.xticks([]), plt.yticks([])
    plt.imshow(img2), plt.show()


def showMatchedKeypoints():
    img1 = cv2.imread('resources/Aerial1.jpg', 0)
    img2 = cv2.imread('resources/Aerial2.jpg', 0)
    img1_f = cv2.imread('output/FeatureAerial1.jpg')
    img2_f = cv2.imread('output/FeatureAerial2.jpg')

    # Initiate SIFT detector
    sift = cv2.xfeatures2d_SIFT.create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = zip(*[(kp, des) for kp, des in sorted(zip(*sift.detectAndCompute(
        img1, None)), key=lambda pair: pair[0].size, reverse=True)])
    kp2, des2 = zip(*[(kp, des) for kp, des in sorted(zip(*sift.detectAndCompute(
        img2, None)), key=lambda pair: pair[0].size, reverse=True)])

    kp1 = np.asarray(kp1[:7])
    des1 = np.asarray(des1[:7])
    kp2 = np.asarray(kp2[:7])
    des2 = np.asarray(des2[:7])

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = []
    for m, n in matches[:7]:
        if m.distance < .75 * n.distance:
            good.append([m])

    # cv2.drawMatchesKnn expects list of lists as matches.
    img3 = cv2.drawMatchesKnn(
        img1_f, kp1, img2_f, kp2, good, None, (0, 255, 0), flags=2)

    plt.figure(figsize=(8, 6))
    plt.xticks([]), plt.yticks([])
    plt.imshow(img3), plt.show()


if __name__ == '__main__':
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
        os.path.dirname(PyQt5.__file__), 'Qt', 'plugins', 'platforms')
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_main()
    ui.setupUi(Widget)

    ui.pushButton.clicked.connect(showDisparity)
    ui.pushButton_2.clicked.connect(showNCC)
    ui.pushButton_3.clicked.connect(showKeypoints)
    ui.pushButton_4.clicked.connect(showMatchedKeypoints)

    Widget.show()
    sys.exit(app.exec_())
