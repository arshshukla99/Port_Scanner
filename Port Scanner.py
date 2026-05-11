import socket
import threading

ip = input("Enter your target IP Address: ")
s_port = int(input("Enter the Starting Port Number: "))
e_port = int(input("Enter the End Port Number : "))

try:
    target_ip = socket.gethostbyname(ip)

except ConnectionRefusedError:
    print("Port is Closed")
    
except socket.timeout:
    print("Connection Time Out :/")
    
except socket.gaierror:
    print("Invalid Ip")

def scan_tcp(pt):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #print(f"Port {pt} is Scanning for TCP...")
    sock.settimeout(1)
    con = sock.connect_ex((target_ip, pt))
    if not con :
        print(f"Port {pt} is OPEN :)")
    sock.close()

for pt in range (s_port, e_port + 1) :
    thread = threading.Thread(target = scan_tcp,args= (pt,))
    thread.start()

def scan_udp(pu):
    sock2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock2.settimeout(1)
    #print(f"Scanning ports {pu} for UDP...")
    con2 = sock2.connect_ex((target_ip,pu))
    if not con2 :
        print(f"Port {pu} is OPEN for UDP")
    sock2.close()

for pu in range(s_port,e_port+1):
    thread2 = threading.Thread(target = scan_udp,args= (pu,))
    thread2.start()