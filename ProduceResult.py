import numpy as np
from itertools import product
from PyQt5.QtWidgets import QMessageBox

from ButtonFunction import startGame


# 控制落子
def ctrlChess(self, event):
    x = event.pos().x()
    y = event.pos().y()
    # 限制点击区域
    if x < self.chessboard_move - 10 or \
            x > self.chessboard_size_move + 10 or \
            y < self.chessboard_move - 10 \
            or y > self.chessboard_size_move + 10:
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
    checkWin(self)


# 判断是否胜利
def checkWin(self):
    # 判断是否五子连珠
    linking_coords = checkLink(self)
    if linking_coords:
        color = linking_coords[-1]['color']
        QMessageBox.information(self, "游戏结束", f"恭喜{'黑方' if color else '白方'}胜利！",
                                QMessageBox.Yes, QMessageBox.Yes)
        startGame(self)
        return
    # 判断棋盘空间是否已满
    if len(self.chess_coord) == 225:
        QMessageBox.information(self, "游戏结束", f"棋盘已满，平局结束！",
                                QMessageBox.Yes, QMessageBox.Yes)
        startGame(self)
        return


# 计算连接数
def checkLink(self):
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
                new_coord['outline'] = True
                linking_coords.append(new_coord)

        if len(linking_coords) == 5:
            self.chess_coord.extend(linking_coords)
            self.update()
            return linking_coords

    return False
