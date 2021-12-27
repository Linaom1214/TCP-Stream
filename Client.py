import socket
import cv2
import numpy as np
import pickle


def send_file_2_client(new_client_socket, frame):
    frame = frame.tobytes()
    data = {
        'image': frame,
    }
    data = pickle.dumps(data)
    new_client_socket.send(str.encode(str(len(data)).ljust(16)))
    new_client_socket.send(data)


def main():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.connect(("192.168.1.103", 8080))  # 连接服务器 发送端为客服端
    cap = cv2.VideoCapture(0)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 5]
    # 等待客户端连接主机
    while cap.isOpened():
        rect, frame = cap.read()
        frame = np.array(frame, dtype=np.uint8)
        _, frame = cv2.imencode('.png', frame, encode_param)
        send_file_2_client(tcp_server_socket, frame)
        receive = tcp_server_socket.recv(1024)
        print(receive)
    tcp_server_socket.close()

if __name__ == "__main__":
    main()
