# Python TCP Port Scanner
A Simple Multithreaded Port Scanner built using Socket.

It was made to understand :
- TCP Connections.
- Network Scanning.
- Open and Closed ports.
- Services on each ports.
- Socket Programming.
- Multithreading in Python.

## Features Include :
- Scan Real Time custom port ranges.
- Can Scan all the 65535 Ports.
- Proper Error Handling Included.
- Multithread support that provide fast results.

## Technologies Used :
- Python 3.14.2
- Socket Module
- Threading Module

## How it Works :
It First takes several inputs from the user like - IP Address & Range of ports i.e. Starting Port and Ending Port.
Note - Supports Provide IPv4 address only.

Then it Attempts to connect on each port which is in the range of Start Port to End Port on the provided IP address.
- If Connection Succeeds -> Port {Number}is OPEN : <Service>
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
$ python3 port_scanner.py
```

## Example Output
```
$ python3 port_scanner.py
Enter your target IP Address: 192.xxx.xx.xx
Enter the Starting Port Number: 1
Enter the End Port Number : 1000
Port 53 is OPEN : domain
Port 80 is OPEN : http
Port 443 is OPEN : https
Total Time Taken : 11.538471221923828 sec
```

