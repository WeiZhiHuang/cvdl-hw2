import os
import sys
import cv2
import PyQt5
# import matplotlib
# import matplotlib.pyplot as plt
from PyQt5 import QtGui, QtWidgets, QtTest
from Ui_main import Ui_Form as Ui_main

if __name__ == '__main__':
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
        os.path.dirname(PyQt5.__file__), 'Qt', 'plugins', 'platforms')
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_main()
    ui.setupUi(Widget)

    # ui.pushButton_5.clicked.connect(augmentedReality)

    Widget.show()
    sys.exit(app.exec_())
