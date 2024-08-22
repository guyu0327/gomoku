import numpy as np

from itertools import product
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QFrame


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

        # 正方形棋盘
        self.chessboard = QFrame(self.container)
        # 正方形棋盘位置大小
        self.chessboard_size = int(self.main_height * 0.9)
        self.chessboard_move = int(self.chessboard_size - self.chessboard_size * 0.95)
        # 正方形网格间距
        self.grid_size = self.chessboard_size / 15

        # 棋子坐标
        self.chess_coord = []
        # 棋子颜色
        self.chess_color = True
        # 棋子大小
        self.chess_size = 40

        # 初始化UI
        self.initUI()

    # 初始化UI
    def initUI(self):
        # 主窗口大小
        self.resize(self.main_width, self.main_height)
        # 固定主窗口大小
        self.setFixedSize(self.width(), self.height())
        # 主窗口居中
        self.move(self.main_move_x, self.main_move_y)
        # 状态栏和标题
        self.status.showMessage('请开始游戏')
        self.setWindowTitle('五子棋')

        # 创建容器
        self.setCentralWidget(self.container)
        # 重写他的鼠标点击事件
        self.container.mousePressEvent = self.mouse_clicked

        # 创建正方形棋盘
        self.chessboard.setFrameShape(QFrame.StyledPanel)
        # 设置正方形棋盘位置和大小
        self.chessboard.setFixedSize(self.chessboard_size, self.chessboard_size)
        self.chessboard.move(self.chessboard_move, self.chessboard_move)

    # 重写绘制事件
    def paintEvent(self, event):
        painter = QPainter(self)
        # 使用抗锯齿
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # 绘制棋盘
        self.draw_chessboard(painter)

    # 绘制棋盘
    def draw_chessboard(self, painter):
        # 设置画笔
        painter.setPen(QPen(QColor("black")))
        # 设置画刷
        painter.setBrush(QBrush(QColor("black")))

        # 绘制方格线
        for i in range(16):
            # 设置线的粗细
            pen = QPen(QColor("black"), 2) if i % 5 == 0 else QPen(QColor("black"), 1)
            painter.setPen(pen)
            # 纵向线
            painter.drawLine(self.grid_size * i + self.chessboard_move,
                             self.chessboard_move,
                             self.grid_size * i + self.chessboard_move,
                             self.chessboard_move + self.chessboard_size)
            # 横向线
            painter.drawLine(self.chessboard_move,
                             self.grid_size * i + self.chessboard_move,
                             self.chessboard_move + self.chessboard_size,
                             self.grid_size * i + self.chessboard_move)

        # 绘制四个点
        dot_move = self.grid_size * 5
        dot_size = 10
        points = [(dot_move, dot_move),
                  (dot_move * 2, dot_move),
                  (dot_move * 2, dot_move * 2),
                  (dot_move, dot_move * 2)]
        for x, y in points:
            x += self.chessboard_move - dot_size / 2
            y += self.chessboard_move - dot_size / 2
            painter.drawEllipse(x, y, dot_size, dot_size)

        # 绘制棋子
        for coord in self.chess_coord:
            self.draw_chess(painter, coord)

    # 绘制棋子
    def draw_chess(self, painter, coord):
        color = QColor("black") if coord['color'] else QColor("white")
        painter.setBrush(QBrush(color))
        painter.drawEllipse(coord['x'] * self.grid_size + self.chessboard_move - self.chess_size / 2,
                            coord['y'] * self.grid_size + self.chessboard_move - self.chess_size / 2,
                            self.chess_size,
                            self.chess_size)

    # 鼠标点击事件
    def mouse_clicked(self, event):
        x = event.pos().x()
        y = event.pos().y()
        # 限制点击位置
        if x < self.chessboard_move - 10 or \
                x > self.chessboard_move + self.chessboard_size + 10 or \
                y < self.chessboard_move - 10 \
                or y > self.chessboard_move + self.chessboard_size + 10:
            return
        # 计算落子位置
        x = np.round((x - self.chessboard_move) / self.grid_size)
        y = np.round((y - self.chessboard_move) / self.grid_size)

        # 判断位置上是否已有棋子
        if any(coord['x'] == x and coord['y'] == y for coord in self.chess_coord):
            return
        # 将棋子坐标添加到列表中
        self.chess_coord.append({'x': x, 'y': y, 'color': self.chess_color})
        # 切换颜色
        self.chess_color = not self.chess_color
        # 重绘
        self.update()
        # 判断是否胜利
        self.check_win()

    # 判断是否胜利
    def check_win(self):
        linking_coords = self.check_link()
        if linking_coords:
            print(f"颜色{linking_coords[-1]['color']}赢了")
            print(f"应该高亮的棋子: {linking_coords}")

    # 判断连接数
    def check_link(self):
        last_coord = self.chess_coord[-1]
        directions = [
            (1, 0),  # 垂直方向
            (0, 1),  # 水平方向
            (1, 1),  # 右对角线
            (-1, 1)  # 左对角线
        ]

        for direction, method in product(directions, range(5)):
            linking_coords = []
            for i in range(5):
                new_coord = {
                    'x': last_coord['x'] + direction[0] * (i - method),
                    'y': last_coord['y'] + direction[1] * (i - method),
                    'color': last_coord['color']
                }
                if new_coord in self.chess_coord:
                    linking_coords.append(new_coord)

            if len(linking_coords) == 5:
                return linking_coords

        return False


def main():
    app = QApplication([])
    form = MainWindow()
    # 显示窗口
    form.show()
    # 进入事件循环
    app.exec_()


if __name__ == "__main__":
    main()