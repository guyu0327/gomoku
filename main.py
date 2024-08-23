from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow


def main():
    app = QApplication([])
    form = MainWindow()
    # 显示窗口
    form.show()
    # 进入事件循环
    app.exec_()


if __name__ == "__main__":
    main()
