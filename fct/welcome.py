import sys
from PyQt5 import QtWidgets, QtGui, QtCore


def window():
    """
    初次打开软件的欢迎界面
    :return:
    """
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    w.setWindowIcon(QtGui.QIcon("images\\logo.ico"))

    btn_min = QtWidgets.QPushButton(w)
    btn_min.setStyleSheet('background-color:#00ff00;border-radius:5px;')
    btn_min.setGeometry(0, 0, 23, 23)
    btn_min.setText("")
    btn_min.move(1160, 60)

    btn_close = QtWidgets.QPushButton(w)
    btn_close.setStyleSheet('background-color:#ff0000;border-radius:5px;')
    btn_close.setGeometry(0, 0, 23, 23)
    btn_close.setText("")
    btn_close.move(1200, 60)

    logo = QtWidgets.QLabel(w)
    logo.setPixmap(QtGui.QPixmap("images\Sangeetic(1).png"))
    logo.move(0, 50)

    wel = QtWidgets.QLabel(w)
    wel.setText("欢   迎")
    wel.setStyleSheet("color:#02e494;font-size:45px;font-family:微软雅黑;")
    wel.move(200, 400)

    before = QtWidgets.QLabel(w)
    before.setText("使用须知")
    before.setStyleSheet("color:#02e494;font-size:33px;font-family:微软雅黑;")
    before.move(500, 200)

    noti = QtWidgets.QLabel(w)
    noti.setText("本软件基于深度学习进行分类，由于音乐种类众多并且通\n"
                 "常一首歌中包含多种音乐风格无法涵盖所有的情况。分类\n"
                 "结果仅供参考，感谢您的使用。")
    noti.setStyleSheet("color:#fff;font-size:28px;font-family:微软雅黑;")
    noti.move(500, 300)

    next = QtWidgets.QPushButton(w)
    next.setText("进入软件")
    next.setGeometry(1050, 600, 150, 50)
    next.setStyleSheet("color:#fff;background-color:rgb(28, 37, 41);font-size:28px;font-family:微软雅黑;")
    next.clicked.connect(w.close)
    btn_min.clicked.connect(w.showMinimized)
    btn_close.clicked.connect(w.close)

    w.setStyleSheet("background-color:rgb(28, 37, 41);")
    w.setWindowTitle("欢迎")
    w.setGeometry(5, 10, 1280, 720)
    w.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    pre_move = w.frameGeometry()
    mov = QtWidgets.QDesktopWidget().availableGeometry().center()
    pre_move.moveCenter(mov)
    w.move(pre_move.topLeft())
    w.show()
    app.exec()


if __name__ == '__main__':
    window()
