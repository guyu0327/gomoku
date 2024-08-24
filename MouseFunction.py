import numpy as np

from AIAlgorithm import aiGame
from ProduceResult import checkWin


# 计算棋子坐标
def calculateCoord(self, event):
    x = event.pos().x()
    y = event.pos().y()
    # 限制点击区域
    if x < self.chessboard_move - 10 or \
            x > self.chessboard_size_move + 10 or \
            y < self.chessboard_move - 10 \
            or y > self.chessboard_size_move + 10:
        return False
    # 计算落子位置
    x = np.round((x - self.chessboard_move) / self.grid_size)
    y = np.round((y - self.chessboard_move) / self.grid_size)

    # 判断位置上是否已有棋子
    if any(coord['x'] == x and coord['y'] == y for coord in self.chess_coord):
        return False

    return {'x': x, 'y': y, 'color': self.chess_color}


# 重写后的container鼠标点击事件
def containerMouseClicked(self, event):
    coord = calculateCoord(self, event)
    if coord:
        # 将棋子坐标添加到列表中
        self.chess_coord.append(coord)
    # 切换颜色
    self.chess_color = not self.chess_color
    aiGame(self)
    # 重绘
    self.update()
    # 判断是否胜利
    checkWin(self)


# 重写后的container鼠标移动事件
def containerMouseMove(self, event):
    coord = calculateCoord(self, event)
    if coord:
        coord['calculate'] = True
        # 将棋子坐标添加到列表中
        self.advance_chess_coord = coord
        self.update()
