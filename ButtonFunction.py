from functools import partial

from PyQt5.QtWidgets import QPushButton, QMessageBox

from AIAlgorithm import selectSquads
from OnlineFunction import selectSide


# 初始化按钮
def initButton(self):
    buttons = [
        {
            'text': '选择模式',
            'clicked': partial(selectMode, self)
        },
        {
            'text': '重新开始',
            'clicked': partial(startGame, self)
        },
        {
            'text': '悔棋',
            'clicked': partial(regret, self)
        },
        {
            'text': '认输',
            'clicked': partial(giveUp, self)
        }]

    for i, info in enumerate(buttons):
        button = QPushButton(self.container)
        button.setText(info['text'])
        button.setGeometry(self.button_x, self.button_y + self.button_height * i, self.button_width,
                           self.button_height)
        button.clicked.connect(partial(info['clicked']))


# 选择模式
def selectMode(self):
    msg = QMessageBox(QMessageBox.Question, "选择", "请选择游戏模式")
    single_button = msg.addButton(self.tr("单机"), QMessageBox.AcceptRole)
    ai_button = msg.addButton(self.tr("人机"), QMessageBox.AcceptRole)
    online_button = msg.addButton(self.tr("联机"), QMessageBox.AcceptRole)
    deepseek_button = msg.addButton(self.tr("DeepSeek"), QMessageBox.AcceptRole)
    exit_button = msg.addButton(self.tr("退出"), QMessageBox.AcceptRole)
    msg.exec_()
    if msg.clickedButton() == exit_button:
        exit()
    elif msg.clickedButton() == single_button:
        self.game_mode = 0
    elif msg.clickedButton() == ai_button:
        self.game_mode = 1
    elif msg.clickedButton() == online_button:
        self.game_mode = 2
    elif msg.clickedButton() == deepseek_button:
        self.game_mode = 3
    startGame(self)
    if self.game_mode == 2:
        selectSide(self)


# 开始游戏
def startGame(self):
    self.chess_coord = []
    self.chess_color = True
    self.status.showMessage("等待黑方落子")
    self.update()
    # 如果游戏模式为人机或DeepSeek，则需要选择黑白方
    if self.game_mode == 1 or self.game_mode == 3:
        selectSquads(self)


# 悔棋
def regret(self):
    if len(self.chess_coord) > 0:
        self.chess_coord.pop()
        if self.game_mode == 1 and len(self.chess_coord) > 0:
            self.chess_coord.pop()
        self.update()


# 认输
def giveUp(self):
    QMessageBox.information(self, "游戏结束",
                            f"{'黑方' if self.chess_color else '白方'}认输，恭喜{'黑方' if not self.chess_color else '白方'}胜利！",
                            QMessageBox.Yes, QMessageBox.Yes)
    startGame(self)
