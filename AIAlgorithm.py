from random import choice

import numpy as np
from PyQt5.QtWidgets import QMessageBox


# 选择阵容
def selectSquads(self):
    msg_squads = QMessageBox(QMessageBox.Question, "选择", "请选择您的阵容")
    msg_squads.addButton(self.tr("黑子"), QMessageBox.AcceptRole)
    white = msg_squads.addButton(self.tr("白子"), QMessageBox.AcceptRole)
    msg_squads.exec_()
    # 玩家选择白方，则人机执黑先行
    if msg_squads.clickedButton() == white:
        aiGame(self)


# 人机对战AI算法
def aiGame(self):
    ai_coord = strategy(self)
    self.chess_coord.append({'x': ai_coord[0], 'y': ai_coord[1], 'color': self.chess_color})
    # 切换颜色
    self.chess_color = not self.chess_color


# 开始计算
def strategy(self):
    # 将黑白坐标拆分 ([白方坐标],[黑方坐标])
    board = ([], [])
    for coord in self.chess_coord:
        if coord['color']:
            board[0].append((coord['x'], coord['y']))
        else:
            board[1].append((coord['x'], coord['y']))

    # 将坐标转换成二维数组 1: 我方 -1: 敌方 0: 空位
    table = np.zeros([self.chessboard, self.chessboard])
    for i in range(self.chessboard):
        for j in range(self.chessboard):
            if self.chess_color:
                if (i, j) in board[0]:
                    table[i, j] = -1
                elif (i, j) in board[1]:
                    table[i, j] = 1
            else:
                if (i, j) in board[0]:
                    table[i, j] = 1
                elif (i, j) in board[1]:
                    table[i, j] = -1

    # 判断自己是否先手
    if len(board[0]) == 0 and len(board[1]) == 0:
        return 7, 7
    else:
        score_table = {}
        for i in range(self.chessboard):
            for j in range(self.chessboard):
                if table[i, j] == 0:
                    table[i, j] = 1
                    score_table[(i, j)] = heuristic(self, table)
                    table[i, j] = 0
        self_position = randomChoose(score_table)
        return self_position[0], self_position[1]


# 计分规则
def score(five_tuple):
    if len(five_tuple) != 5:
        print("ERROR")
        return None
    if 1 in five_tuple and -1 in five_tuple:
        return 0
    elif sum(five_tuple) == 0:
        return 7
    elif sum(five_tuple) == -1:
        return -35
    elif sum(five_tuple) == -2:
        return -800
    elif sum(five_tuple) == -3:
        return -15000
    elif sum(five_tuple) == -4:
        return -800000
    elif sum(five_tuple) == -5:
        return -10000000
    elif sum(five_tuple) == 5:
        return 10000000
    elif sum(five_tuple) == 1:
        return 15
    elif sum(five_tuple) == 2:
        return 400
    elif sum(five_tuple) == 3:
        return 1800
    elif sum(five_tuple) == 4:
        return 100000


# 计分
def heuristic(self, table):
    sum_score = 0
    for i in range(self.chessboard):
        for j in range(self.chessboard):
            if j + 4 < self.chessboard:
                sum_score += score(tuple(table[i, j:j + 5]))
            if i + 4 < self.chessboard:
                sum_score += score(tuple(table[i:i + 5, j]))
            if i + 4 < self.chessboard and j + 4 < self.chessboard:
                five_tuple = []
                for k in range(5):
                    five_tuple.append(table[i + k, j + k])
                sum_score += score(tuple(five_tuple))
            if i + 4 < self.chessboard and j - 4 >= 0:
                five_tuple = []
                for k in range(5):
                    five_tuple.append(table[i + k, j - k])
                sum_score += score(tuple(five_tuple))
    return sum_score


# 选择最高分位置
def randomChoose(score_table):
    max_value = max(score_table.items(), key=lambda x: x[1])[1]
    positions = []
    for item in score_table.items():
        if item[1] == max_value:
            positions.append(item[0])
    return choice(positions)
