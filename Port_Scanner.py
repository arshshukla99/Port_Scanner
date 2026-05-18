import socket
import threading
import time
import sys

print("-"*100)
print(" "*35,"Simple Port Scanner")
print("-"*100)

start_time = time.time()

ip = input("Enter your target IP Address: ")
start_port = int(input("Enter the Starting Port Number: "))
end_port = int(input("Enter the End Port Number : "))

try:
    target_ip = socket.gethostbyname(ip)
    
except socket.gaierror:
    print("Invalid Ip :/")
    sys.exit()

def scan_tcp(port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(1)
    con = sock.connect_ex((target_ip, port))
    if not con :
        try:
            service = socket.getservbyport(port)
        except OSError:
            service = "Unknown"
        print(f"Port {port} is OPEN : {service}")
    sock.close()

threads = []

for port in range (start_port, end_port + 1) :
    thread = threading.Thread(target = scan_tcp, args= (port,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

end_time = time.time()

print("Total Time Taken :",(end_time - start_time),"sec")
