import json
import socket
import threading
from functools import partial

import pyperclip
from PyQt5.QtWidgets import QMessageBox


# 选择服务端或客户端
def selectSide(self):
    msg_side = QMessageBox(QMessageBox.Question, "选择", "请选择创建或进入房间")
    server_button = msg_side.addButton(self.tr("创建房间"), QMessageBox.AcceptRole)
    client_button = msg_side.addButton(self.tr("进入房间"), QMessageBox.AcceptRole)
    msg_side.exec_()
    if msg_side.clickedButton() == server_button:
        checkNetwork(self)
        extractIp(self)
        server(self)
    elif msg_side.clickedButton() == client_button:
        checkNetwork(self)
        client(self)


# 检查网络连接
def checkNetwork(self):
    try:
        # 超时时间
        socket.setdefaulttimeout(5)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('www.baidu.com', 80))
    except socket.error as ex:
        QMessageBox.critical(self, "网络连接异常", "当前网络不可用，请检查您的网络状态\n" + str(ex))
        selectSide(self)


# 获取IP地址
def extractIp(self):
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    st.connect(('10.255.255.255', 1))
    self.server_ip = st.getsockname()[0]
    pyperclip.copy(self.server_ip)
    QMessageBox.information(self, "房间信息", "IP：" + self.server_ip + "，已复制到剪贴板")


# 服务端
def server(self):
    # 绑定IP端口
    self.tcp_server.bind((self.server_ip, self.server_port))
    # 最大连接数
    self.tcp_server.listen(5)
    threading.Thread(target=partial(startServerListen, self)).start()


# 服务端监听线程
def startServerListen(self):
    while True:
        try:
            print('房间创建成功, 等待对方加入...')
            self.tcp_socket, address = self.tcp_server.accept()
            print('对方已加入, 可以开始游戏')
            data = {'x': 0, 'y': 0, 'color': True}
            self.tcp_socket.sendall(json.dumps(data).encode('utf-8'))
            self.receiveData()
        except:
            break


# 客户端
def client(self):
    self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.tcp_socket.connect((self.server_ip, self.server_port))
    data = {'x': 1, 'y': 1, 'color': False}
    self.tcp_socket.sendall(json.dumps(data).encode('utf-8'))
    print('已经加入房间, 可以开始游戏')
    threading.Thread(target=partial(receiveData, self)).start()


# 接收数据
def receiveData(self):
    while True:
        data = self.tcp_socket.recv(1024)
        self.chess_coord.append(json.loads(data.decode('utf-8')))
