#!/usr/bin/python3

import sys
import time
import socket
import threading

print('-'*100)
print(" "*35,"Simple Port Scanner")
print("-"*100)

usage = " Give arguments in the Following Format : \n\npython3 port_scanner.py TARGET_IP START_PORT END_PORT"

if len(sys.argv) != 4 :
    print(usage)
    sys.exit()

try :
    target = socket.gethostbyname(sys.argv[1])
except socket.gaierror:
    print("Ip isn't Correct !")

start_time = time.time()

start_port = int(sys.argv[2])
end_port = int(sys.argv[3])

def port_scan(port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(1)
    con = sock.connect_ex((target,port))
    if not con:
        try :
            service = socket.getservbyport(port)
        except OSError:
            print("Unknown Service")
        print(f"Port {port} is OPEN : {service}")
    sock.close()

threads = []

for port in range(start_port,end_port+1):
    thread = threading.Thread(target=port_scan,args=(port,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print()

end_time = time.time()   
print("Scan Performed in :",(end_time - start_time))
