import socket
import cv2
import time
import numpy as np
import pickle

def recvall(sock, count):
    buf = b''#buf是一个byte类型
    while count:
        #接受TCP套接字的数据。数据以字符串形式返回，count指定要接收的最大数据量.
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def main():
    
    dest_ip = "localhost"
    dest_port = 8080
    while True:
        #创建套接字
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #链接服务器
        tcp_socket.connect((dest_ip, dest_port))
        length = recvall(tcp_socket,16)#获得图片文件的长度,16代表获取长度
        stringData = recvall(tcp_socket, int(length))#根据获得的文件长度，获取图片文件
        stringData = pickle.loads(stringData)
        stringData = stringData['image']
        data = np.frombuffer(stringData, np.uint8)#将获取到的字符流数据转换成1维数组
        decimg=cv2.imdecode(data,cv2.IMREAD_COLOR)#将数组解码成图像
        cv2.imshow("img",decimg)
        cv2.waitKey(1)
        tcp_socket.send(("I'm Receive").encode('utf-8'))
    tcp_socket.close()
        # time.sleep(1)
    # 8. 关闭套接字
    


if __name__ == "__main__":
    main()
