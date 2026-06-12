#Shebang line

#!/usr/bin/python3

import sys
import time
import queue
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
parser.add_argument("-th","--threads", dest="threads",type=int, help= "No. of Threads To be Used", default=500)
parser.add_argument("-V","--verbose", dest="verbose", action= "store_true", help= "Verbose Output")
parser.add_argument("-v","--version", action="version", version= "%(prog)s 1.1", help= "Diplay %(prog)s Version")
args = parser.parse_args()


# Extracting IP given by User

try :
    target = socket.gethostbyname(args.target)
except socket.gaierror:
    print("Ip isn't Correct !")
    sys.exit()
    
start_time = time.time()

#try to get ip between given arguments and checks for errors in ports
start_port = args.start
end_port = args.end

if start_port < 1 or end_port > 65535 or start_port > end_port:
    print("Invalid Ports")
    sys.exit()

if args.verbose:
    print(f"Target IP : {args.target}")
    print(f"Port Ranges : {args.start}-{args.end}")
    print(f"Threads : {args.threads}")
    print()

#Searches for open ports and service on each port
dict_port = {}

def port_scan(port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(1) 
    try:
        if args.verbose :
            print("Scanning Port :",port)
        global con    
        con = sock.connect_ex((target,port))
        if not con:
        
            #Trying to get service on each port
            try :
                service = socket.getservbyport(port)
            except OSError:
                service = "Unknown Service"
            dict_port[port] = service
            
            # Banner Grabbing for Verbose Output
            global banner
            try:
                banner = sock.recv(1024).decode(errors="ignore")
                
            except socket.timeout:
                banner = "Unknown Banner"
                
            if not args.verbose:
                print(f"Port {port} is OPEN : {service}")
        
    finally:
        sock.close()

def thread_worker():
    while not q.empty():
        port = q.get()
        try :
            port_scan(port)
        finally:
            q.task_done()
           
threads = []

q = queue.Queue()

#threads.start() creates a thread for each port scan and store each thread created in a threads list

for i in range(start_port,end_port+1):
    q.put(i)
    
for _ in range(args.threads):
    thread = threading.Thread(target=thread_worker)
    thread.start()
    threads.append(thread)
    
#thread.join() waits for each thread to finish then end the program

for thread in threads:
    thread.join()

if args.verbose:
    print()
    print(f"Total {end_port - len(dict_port)} are CLOSED and {len(dict_port)} are OPEN :-\n")
    for i in dict_port:
        print(f"Port {i} is OPEN : {dict_port[i]}\nBanner : {banner}\n")
      
if len(dict_port) == 0:
    print()
    print(f"No OPEN Ports available in provided Port Range : {start_port}-{end_port} ")

end_time = time.time()
print()
print("Scan Performed in :",(end_time - start_time))
