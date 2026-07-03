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

try:
    import nmap
except ImportError:
    nmap = None

os_name = None
#Created Parser Obejct

parser = argparse.ArgumentParser(description="Python Based Fast Port Scanner", usage="%(prog)s -t TARGET [MORE_OPTIONS] ", epilog= "Example - %(prog)s -s 1 -e 65535 -t 192.168.43.229")

# Added arguments in parser for more options

parser.add_argument("-s","--start", type=int, help="Start Port", default=1)
parser.add_argument("-e","--end", type=int, help= "End Port", default= 65535)
parser.add_argument("-t","--target", dest="target", required= True, help="Target IP or Domain")
parser.add_argument("-th","--threads", dest="threads",type=int, help= "No. of Threads To be Used", default=200)
parser.add_argument("-V","--verbose", dest="verbose", action= "store_true", help= "Verbose Output")
parser.add_argument("-v","--version", action="version", version= "%(prog)s 1.4", help= "Diplay %(prog)s Version")
parser.add_argument("-j","--json", dest="json", help = "Export JSON Output")
parser.add_argument("-o","--output", dest="output", help = "Export Output (To a .csv file)")
parser.add_argument("-O","--os-detect", action="store_true", help = "Attempt OS fingerprinting using nmap")
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

#Searches for open ports and service on each port and store it in the dictionary
dict_port = {}

def port_scan(port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(0.3) 
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
                if port in [21,22,25,110,3306]:
                    banner = sock.recv(1024).decode(errors="ignore")
                
                elif port == 80:
                    request = f"GET / HTTP/1.1\r\nHost: {args.target}\r\n\r\n"
                    sock.sendall(request.encode())
                    banner = sock.recv(1024).decode(errors="ignore")
                
                '''if port == 443:
                    try :
                        import ssl
                        context = ssl.create_default_context()
                        sock_context = context.wrap_sockets(sock,server_hostname=args.target)
                    
                        request = f"GET / HTTP/1.1\r\n'''
               
                else:
                    banner = "Unknown Banner"
                    
            except socket.timeout:
                banner = "Unknown Banner"
                
            lock = threading.Lock()
            
            with lock:
                dict_port[port] = {"service" : service,
                                   "banner" : banner }
            
    finally:
        sock.close()

# Threads function
def thread_worker():
    while not q.empty():
        port = q.get()
        
        try :
            port_scan(port)

        finally:
            q.task_done()

#Function for OS Detection
def os_detect(target):
    if nmap is None:
        return "python-nmap isn't installed :/\nTry Installing it with : 'pip install python-nmap'"
    
    try:
        nm = nmap.PortScanner()
        nm.scan(hosts=target, arguments="-O --osscan-guess")
        
        if 'osmatch' in nm[target] and len(nm[target]['osmatch'])>0:    # len(nm[ip]['osmatch']) is to check the length is osmatch have anything int the list or not
            return nm[target]['osmatch'][0]['name']      # Bcz Data Structure of nm = { '192.168.29.90' : { 'osmatch' : [ { name: Linux, accuracy : 95 } ] } }
        
        return "Unknown OS"  #Only executes if one of above 'if' conditions is False.
    
    except Exception as e:
        return f"OS Detection Failed : {e}" 

#NOTE : Function ends immediately after one return is occured and the other written code after that will not execute.
           
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

#prints OS of the Target IP
if args.os_detect:
    if len(dict_port) != 0:
        print("Performing OS Detection...")
        os_name = os_detect(target)
        if os_name == "python-nmap isn't installed :/\nTry Installing it with : 'pip install python-nmap'" or os_name.startswith("OS Detection Failed"):
            print(f"\n{os_name}")
        else:
            print(f"\nOS : {os_name}")
    else:
        print(Fore.LIGHTRED_EX + "WARNING !" + Style.RESET_ALL + " No Open Ports Found. OS Detection may be inaccurate.")
        print("Performing OS Detection...")
        os_name = os_detect(target)
        if os_name == "python-nmap isn't installed :/\nTry Installing it with : 'pip install python-nmap'" or os_name.startswith("OS Detection Failed"):
            print(f"\n{os_name}")
        else:
            print(f"\nOS : {os_name}")
            
if len(dict_port) == 0:
    print()
    print(Fore.LIGHTRED_EX + f"No OPEN Ports" + Style.RESET_ALL +f" available in provided Port Range : {start_port}-{end_port}")

end_time = time.time()
print()
print("Scan Performed in :",(end_time - start_time))

#Export JSON Output
if args.json:
    json_file = args.json
    if json_file.endswith(".json"):
        with open(f"{args.json}", "w") as f:
            if args.os_detect:
                export_data = { 'OS' : os_name, "Ports" : dict_port }
                json.dump(export_data, f, indent=4)
            else :
                export_data = {"Ports": dict_port}
                json.dump(export_data,f,indent=2)
                
            print(f"\nFile {args.json} " + Fore.LIGHTGREEN_EX + "EXPORT SUCCESSFUL" + Style.RESET_ALL + " Saved to this Current Path :)")
    else:
        print(f"\n{args.json} should contain " + Fore.LIGHTRED_EX + ".json" + Style.RESET_ALL + " extension")
        print("EXPORT Unsuccessful :/")
        
#Export CSV Output
if args.output:
    if (args.output).endswith(".csv"):
        with open(f"{args.output}", "w", newline='') as f:
            fobj = csv.writer(f)
            if args.os_detect:
                fobj.writerow([])
                fobj.writerow(["OS", os_name])
                            
            fobj.writerow(["Port","Service","Banner"])
            for i in dict_port:
                fobj.writerow([i,dict_port[i]["service"],dict_port[i]["banner"]])
                
            print(f"\nFile {args.output} " + Fore.LIGHTGREEN_EX + "EXPORT SUCCESSFUL" + Style.RESET_ALL + " Saved to this Current Path :)")

