#Shebang line

#!/usr/bin/python3

import csv
import sys
import time
import json
import queue
import socket
import argparse
import threading
from colorama import Fore, Style

print('-'*100)
print(" "*35,"Simple Port Scanner")
print("-"*100)

#Created Parser Object

parser = argparse.ArgumentParser(description="Python Based Fast Port Scanner", usage="%(prog)s -t TARGET [MORE_OPTIONS] ", epilog= "Example - %(prog)s -s 1 -e 65535 -t 192.168.43.229")

# Added arguments in parser for more options

parser.add_argument("-s","--start", type=int, help="Start Port", default=1)
parser.add_argument("-e","--end", type=int, help= "End Port", default= 65535)
parser.add_argument("-t","--target", dest="target", required= True, help="Target IP or Domain")
parser.add_argument("-th","--threads", dest="threads",type=int, help= "No. of Threads To be Used", default=500)
parser.add_argument("-V","--verbose", dest="verbose", action= "store_true", help= "Verbose Output")
parser.add_argument("-v","--version", action="version", version= "%(prog)s 1.4", help= "Diplay %(prog)s Version")
parser.add_argument("-j","--json", dest="json", help = "Explort JSON Output")
parser.add_argument("-o","--output", dest="output", help = "Export Output (To a .csv file)")
args = parser.parse_args()

# Extracting IP given by User

try :
    target = socket.gethostbyname(args.target)
except socket.gaierror:
    print(Fore.LIGHTRED_EX + "Ip isn't Correct !" + Style.RESET_ALL)
    sys.exit()
    
start_time = time.time()

#try to get ip between given arguments and checks for errors in ports
start_port = args.start
end_port = args.end

if start_port < 1 or end_port > 65535 or start_port > end_port:
    print(Fore.LIGHTRED_EX + "Invalid Ports" + Style.RESET_ALL)
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
        con = sock.connect_ex((target,port))
        if not con:
        
            #Trying to get service on each port
            try :
                service = socket.getservbyport(port)
            except OSError:
                service = "Unknown Service"
                
            if not args.verbose:
                print(f"Port {port} is " + Fore.LIGHTGREEN_EX + f"OPEN" + Style.RESET_ALL + Fore.CYAN + f" : {service}" + Style.RESET_ALL)

            try:
                if port in [21,22,25,110]:
                    banner = sock.recv(1024).decode(errors="ignore")
                
                elif port == 80:
                    request = f"GET / HTTP/1.1\r\nHost: {args.target}\r\n\r\n"
                    sock.sendall(request.encode())
                    banner = sock.recv(1024).decode(errors="ignore")
               
                else:
                    banner = "Unknown Banner"
                    
            except socket.timeout:
                banner = "Unknown Banner"
            dict_port[port] = {"service" : service,
                               "banner" : banner}
            
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

#Coloured Outputs Using Colorama

if args.verbose:
    print(f"\nTotal Ports Scanned : {end_port - start_port + 1}")
    print(f"Total {(end_port - start_port) - len(dict_port) + 1} are CLOSED and {len(dict_port)} are OPEN :-\n")
    for i in sorted(dict_port):
        print(f"Port {i} is " + Fore.GREEN + "OPEN" + Style.RESET_ALL + " : " + Fore.YELLOW + f"{dict_port[i]['service']}" + Style.RESET_ALL + "\nBanner : " + Fore.LIGHTBLUE_EX + f"{dict_port[i]['banner']}\n" + Style.RESET_ALL)
      
if len(dict_port) == 0:
    print()
    print(Fore.LIGHTRED_EX + f"No OPEN Ports" + Style.RESET_ALL +f" available in provided Port Range : {start_port}-{end_port}")

end_time = time.time()
print()
print("Scan Performed in :",(end_time - start_time))

#Saving output of the Whole Scan in JSON File
if args.json:
    json_file = args.json
    if json_file.endswith(".json"):
        with open(f"{args.json}", "w") as f:
            json.dump(dict_port, f, indent=2)
            print(f"\nFile {args.json} " + Fore.LIGHTGREEN_EX + "EXPORT SUCCESSFUL" + Style.RESET_ALL + " Saved to this Current Path :)")
    else:
        print(f"\n{args.json} should contain " + Fore.LIGHTRED_EX + ".json" + Style.RESET_ALL + " extension")
        print("EXPORT Unsuccessful :/")

#Saving Output of the Whole scan in CSV file
if args.output:
    if (args.output).endswith(".csv"):
        with open(f"{args.output}", "w", newline='') as f:
            fobj = csv.writer(f)
            fobj.writerow(["Port","Service","Banner"])
            for i in dict_port:
                fobj.writerow([i,dict_port[i]["service"],dict_port[i]["banner"]])
            print(f"\nFile {args.output} " + Fore.LIGHTGREEN_EX + "EXPORT SUCCESSFUL" + Style.RESET_ALL + " Saved to this Current Path :)")
