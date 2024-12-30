import json
import socket
import threading
import pyperclip

from functools import partial
from PyQt5.QtWidgets import QMessageBox, QInputDialog


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
    # 可设置最大连接数
    self.tcp_server.listen()
    threading.Thread(target=partial(startServerListen, self)).start()


# 服务端监听线程
def startServerListen(self):
    while True:
        try:
            print('房间创建成功, 等待对方加入...')
            self.tcp_socket, address = self.tcp_server.accept()
            receiveData(self)
            self.player_ready = True
            self.chess_color_online = True
            print('对方已加入, 可以开始游戏')
        except:
            break


# 客户端
def client(self):
    self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    text, ok = QInputDialog.getText(None, "输入框", "请输入房间IP：")
    if ok and text != '':
        print("你输入的内容是：", text)
        self.server_ip = text
    else:
        print("用户取消了输入或没有输入内容")
        return selectSide(self)

    try:
        self.tcp_socket.connect((self.server_ip, self.server_port))
    except socket.error as e:
        QMessageBox.critical(self, "网络连接异常", "无法连接到服务器，请检查IP地址是否正确\n" + str(e))
        selectSide(self)

    threading.Thread(target=partial(receiveData, self)).start()
    self.player_ready = True
    self.chess_color_online = False
    print('已经加入房间, 可以开始游戏')


# 接收数据
def receiveData(self):
    from MouseFunction import render
    while True:
        try:
            data = self.tcp_socket.recv(1024)
            if data:
                self.chess_coord.append(json.loads(data.decode('utf-8')))
            else:
                break
        except socket.timeout:
            print("接收数据超时，正在重试...")
            continue
        except Exception as e:
            print(f"接收数据时发生错误：{e}")
            break
        render(self)
