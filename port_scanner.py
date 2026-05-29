#Shebang line

#!/usr/bin/python3

import sys
import time
import socket
import argparse
import threading

print('-'*100)
print(" "*35,"Simple Port Scanner")
print("-"*100)

#Created Parser Obejct

parser = argparse.ArgumentParser(description="Python Based Fast Port Scanner", usage="%(prog)s -t TARGET [MORE_OPTIONS] ", epilog= "Example - %(prog)s -s 1 -e 65535 -t 192.168.43.229")

# Added arguments in parser for more options

parser.add_argument("-s","--start", type=int, help="Start Port", default=1)
parser.add_argument("-e","--end", type=int, help= "End Port", default= 65535)
parser.add_argument("-t","--target", dest="target", required= True, help="Target IP or Domain")
#parser.add_argument("-th","--threads", dest="threads",type=int, help= "No. of Threads To be Used", default=500)
#parser.add_argument("-V","--verbose", dest="verbose", action= "store_true", help= "Verbose Output")
parser.add_argument("-v","--version", action="version", version= "%(prog)s 1.1", help= "Diplay %(prog)s Version")
args = parser.parse_args()

# Extracting IP given by User

try :
    target = socket.gethostbyname(args.target)
except socket.gaierror:
    print("Ip isn't Correct !")
    sys.exit()

start_time = time.time()

#try to get ip between given arguments and checks for errors in ip
start_port = args.start
end_port = args.end

if start_port < 1 or end_port > 65535 or start_port > end_port:
    print("Invalid Ports")
    sys.exit()

#Searches for open ports and service on each port
def port_scan(port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        con = sock.connect_ex((target,port))
        if not con:
            try :
                service = socket.getservbyport(port)
            except OSError:
                service = "Unknown Service"
            print(f"Port {port} is OPEN : {service}")
    finally:
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
