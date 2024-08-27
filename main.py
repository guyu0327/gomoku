from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow


def main():
    app = QApplication([])
    # 创建主窗口
    MainWindow()
    # 进入事件循环
    app.exec_()


if __name__ == "__main__":
    main()
