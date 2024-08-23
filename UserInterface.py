from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor, QBrush, QPainter


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


# 绘制棋盘
def drawChessboard(self):
    painter = QPainter(self)
    # 使用抗锯齿
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.HighQualityAntialiasing)
    # 设置画笔
    painter.setPen(QPen(QColor("black")))
    # 设置画刷
    painter.setBrush(QBrush(QColor("black")))

    # 绘制方格线
    for i in range(15):
        # 设置线的粗细
        pen = QPen(QColor("black"), 2) if i == 3 or i == 11 else QPen(QColor("black"), 1)
        painter.setPen(pen)
        # 纵向线
        painter.drawLine(self.grid_size * i + self.chessboard_move,
                         self.chessboard_move,
                         self.grid_size * i + self.chessboard_move,
                         self.chessboard_size_move)
        # 横向线
        painter.drawLine(self.chessboard_move,
                         self.grid_size * i + self.chessboard_move,
                         self.chessboard_size_move,
                         self.grid_size * i + self.chessboard_move)

    # 绘制四个点
    dot_move1 = self.grid_size * 3
    dot_move2 = self.grid_size * 11
    dot_move3 = self.grid_size * 7
    dot_size = 10
    points = [(dot_move1, dot_move1),
              (dot_move2, dot_move1),
              (dot_move2, dot_move2),
              (dot_move1, dot_move2),
              (dot_move3, dot_move3)]
    for x, y in points:
        x += self.chessboard_move - dot_size / 2
        y += self.chessboard_move - dot_size / 2
        painter.drawEllipse(x, y, dot_size, dot_size)

    # 绘制预落子
    if self.advance_chess_coord:
        drawChess(self, painter, self.advance_chess_coord)

    # 绘制棋子
    for coord in self.chess_coord:
        drawChess(self, painter, coord)


# 绘制棋子
def drawChess(self, painter, coord):
    # 普通棋子
    brush = QBrush(QColor("black")) if coord.get('color', True) else QBrush(QColor("white"))
    # 胜利后棋子
    pen = QPen(QColor("yellow"), 2) if coord.get('outline', False) else QPen(QColor("black"), 1)
    # 预落下棋子
    if coord.get('calculate', False):
        brush = QBrush(QColor(0, 0, 0, 20))
        pen.setStyle(Qt.DashLine)

    painter.setBrush(brush)
    painter.setPen(pen)

    painter.drawEllipse(coord['x'] * self.grid_size + self.chessboard_move - self.chess_size / 2,
                        coord['y'] * self.grid_size + self.chessboard_move - self.chess_size / 2,
                        self.chess_size,
                        self.chess_size)
