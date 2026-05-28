#Shebang line

#!/usr/bin/python3

import sys
import time
import socket
import threading

#Adds graphics Initially

print('-'*100)
print(" "*35,"Simple Port Scanner")
print("-"*100)

usage = " Give arguments in the Following Format : \n\npython3 port_scanner.py TARGET_IP START_PORT END_PORT"

#Checks if there are 4 arguments given by the user or not
if len(sys.argv) != 4 :
    print(usage)
    sys.exit()

#try to get ip between given arguments and checks for errors in ip
try :
    target = socket.gethostbyname(sys.argv[1])
except socket.gaierror:
    print("Ip isn't Correct !")

start_time = time.time()

start_port = int(sys.argv[2])
end_port = int(sys.argv[3])

#searches for open ports and service on each port
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

#threads.start() creates a thread for each port scan and store each thread created in a threads list
for port in range(start_port,end_port+1):
    thread = threading.Thread(target=port_scan,args=(port,))
    thread.start()
    threads.append(thread)

#thread.join() waits for each thread to finish then end the program
for thread in threads:
    thread.join()

print()

end_time = time.time()   
print("Scan Performed in :",(end_time - start_time))
