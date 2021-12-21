import socket
import cv2
import numpy as np
import time
import pickle

def send_file_2_client(new_client_socket, frame):
    frame =  frame.tobytes()
    data = {
        'image':frame,
        'position':10
    }
    data = pickle.dumps(data)
    new_client_socket.send(str.encode(str(len(data)).ljust(16)))
    new_client_socket.send(data)
    receive = new_client_socket.recv(1024)
    print(receive)



def main():
    #(创建套接字 socket)
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #(绑定本地信息 bind)  客户端不绑定
    tcp_server_socket.bind(("", 8080))
    # 响铃模式(让默认的套接字由主动变为被动 listen)
    tcp_server_socket.listen(128)
    cap = cv2.VideoCapture(0)
    rect, frame = cap.read()
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),15]
    while True:
        rect, frame = cap.read()
        # 4. 等待别人的电话到来(等待客户端的链接 accept)
        # new_client_socket 通信套接字
        new_client_socket, client_addr = tcp_server_socket.accept()
        # 5. 调用发送文件函数，完成为客户端服务
        # frame  = cv2.resize(frame,(128,128))
        frame = np.array(frame,dtype=np.uint8)
        _, frame  = cv2.imencode('.jpg', frame, encode_param)
        send_file_2_client(new_client_socket, frame)
        # 6. 关闭套接字
        new_client_socket.close()
        # time.sleep(0.1)
    tcp_server_socket.close()


if __name__ == "__main__":
    main()
