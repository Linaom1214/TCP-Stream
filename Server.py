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
    
    dest_ip = ""
    dest_port = 8080
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((dest_ip,dest_port)) # 绑定本机IP
    tcp_socket.listen(128) 
    new_client_socket, client_addr = tcp_socket.accept()
    while True:
        start =time.time()
        length = recvall(new_client_socket,16)#获得图片文件的长度,16代表获取长度
        stringData = recvall(new_client_socket, int(length))#根据获得的文件长度，获取图片文件
        stringData = pickle.loads(stringData)
        stringData = stringData['image']
        data = np.frombuffer(stringData, np.uint8)#将获取到的字符流数据转换成1维数组
        decimg=cv2.imdecode(data,cv2.IMREAD_COLOR)#将数组解码成图像
        canny = cv2.Canny(decimg, 50, 150)
        cv2.imshow("img",canny)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        use_time = time.time() - start
        fps = 1 / use_time     
        new_client_socket.send(str(fps).encode('utf-8'))
    tcp_socket.close()
    


if __name__ == "__main__":
    main()
