# Python TCP Port Scanner
A Simple Multithreaded Port Scanner built using Socket.

It was made to understand :
- TCP Connections.
- Network Scanning.
- Open and Closed ports.
- Services on each ports.
- Socket Programming.
- Multithreading in Python.
- Service Detection
- Banner Grabbing
- Error Management

## Features Include :
- Scan Real Time custom port ranges.
- Can Scan all the 65535 Ports.
- Proper Error Handling Included.
- Multithread support that provide fast results.
- Service Detection for all the 65535 ports.
- Banner Grabbing for Open Ports.

## Technologies Used :
- Python 3.14.2
- Socket Module
- Threading Module

## How it Works :
It First takes several inputs from the user like - IP Address & Range of ports i.e. Starting Port and Ending Port.
Note - Supports Provide IPv4 address only.

Then it Attempts to connect on each port which is in the range of Start Port to End Port on the provided IP address.
- If Connection Succeeds -> Port {Number} is OPEN : <Service>
- If Connection Failed -> Port is CLOSED

## How to Use :
Step 1 : Clone the Repository

```
$ git clone https://github.com/arshshukla99/Port_Scanner
```

Step 2 : Navigate to the Project Folder

```
$ cd port_scanner.py
```

Step 3 : Run the Script 'port_scanner.py'

```
$ python3 port_scanner.py -t 192.168.43.169 -s 1 -e 1000
```

## Example Output
```
$ python3 port_scanner.py -t 192.168.43.169 -s 1 -e 1000
----------------------------------------------------------------------------------------------------
                                    Simple Port Scanner
----------------------------------------------------------------------------------------------------
Port 139 is OPEN : netbios-ssn
Port 135 is OPEN : epmap
Port 445 is OPEN : microsoft-ds
Port 623 is OPEN : asf-rmcp

Scan Performed in : 2.6426780223846436

```

## Example Screenshot 
<img width="1366" height="643" alt="image" src="https://github.com/user-attachments/assets/c833f2e1-452a-40e0-bf38-075212667c45" />



