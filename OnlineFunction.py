import json
import socket

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
        # extractIp(self)
        server(self)
    elif msg_side.clickedButton() == client_button:
        checkNetwork(self)


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
    self.serverIp = st.getsockname()[0]
    pyperclip.copy(self.serverIp)
    QMessageBox.information(self, "房间信息", "IP：" + self.serverIp + "，已复制到剪贴板")


# 服务端
def server(self):
    while True:  # 无限循环，持续监听
        # 创建socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定监听IP端口
        print((self.serverIp, self.serverPort))
        server_socket.bind((self.serverIp, self.serverPort))
        # 设置最大连接数
        server_socket.listen(5)
        server_socket.settimeout(10000)
        print(u'waiting for connect...')
        try:
            # 接受连接
            connect, (host, port) = server_socket.accept()
            print(f"Connected by {host}:{port}")

            while True:  # 持续接收数据
                data = connect.recv(1024)
                if not data:
                    break  # 如果没有接收到数据，跳出循环，关闭连接
                print(data.decode('utf-8'))
                self.chess_coord.append(json.loads(data.decode('utf-8')))
                self.update()
        except socket.timeout:
            print("Waiting for a connection...")
        finally:
            # 关闭连接
            connect.close()

    # 结束socket（注意：这里的关闭操作实际上永远不会执行，因为while True是无限循环）
    server_socket.close()
