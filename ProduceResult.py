from itertools import product
from PyQt5.QtWidgets import QMessageBox

from ButtonFunction import startGame


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
