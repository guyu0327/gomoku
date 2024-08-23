from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication

from ButtonFunction import initButton, selectMode
from ProduceResult import ctrlChess
from UserInterface import initUI, drawChessboard


# 主窗口
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # 获取桌面尺寸
        self.desktop = QApplication.desktop()
        self.screen_rect = self.desktop.screenGeometry()
        # 设置主窗口比例
        self.main_width = int(self.screen_rect.width() * 0.45)
        self.main_height = int(self.screen_rect.height() * 0.55)
        # 设置主窗口位置
        self.main_move_x = (self.screen_rect.width() - self.main_width) // 2
        self.main_move_y = (self.screen_rect.height() - self.main_width) // 2
        # 状态栏
        self.status = self.statusBar()

        # 整体容器
        self.container = QWidget(self)
        # 重写他的鼠标点击事件
        self.container.mousePressEvent = self.mouseClicked

        # 正方形棋盘位置大小
        self.chessboard_size = int(self.main_height * 0.9)
        self.chessboard_move = int(self.chessboard_size - self.chessboard_size * 0.95)
        self.chessboard_size_move = self.chessboard_size + self.chessboard_move
        # 正方形网格间距
        self.grid_size = self.chessboard_size / 15

        # 按钮大小
        self.button_width = int(self.main_width * 0.2)
        self.button_height = int(self.main_height * 0.05)
        # 按钮位置
        self.button_x = self.chessboard_size_move + (
                (self.main_width - self.chessboard_size_move) / 2 - self.button_width / 2)
        self.button_y = self.main_height / 3

        # 棋子坐标
        self.chess_coord = []
        # 棋子颜色
        self.chess_color = True
        # 棋子大小
        self.chess_size = self.grid_size / 1.2

        # 游戏模式 0：单机 1：人机 2：联机
        self.game_mode = 0

        # 初始化UI
        initUI(self)
        # 初始化按钮
        initButton(self)
        # 选择游戏模式
        selectMode(self)

    # 重写绘图事件
    def paintEvent(self, event):
        drawChessboard(self)

    # 重写鼠标点击事件
    def mouseClicked(self, event):
        ctrlChess(self, event)
