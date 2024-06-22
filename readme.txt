TCP Client-Server Program Documentation

Welcome to the TCP client-server program documentation. This document provides essential information on how to run and configure the TCP communication program, which includes both reversetcpclient.py and reversetcpserver.py.

Program Overview
This program simulates a basic TCP communication between a client and a server, focusing on the process of reversing text blocks of a file sent by the client. It includes functionalities such as connection establishment, data transfer, and connection termination. The program is designed to be simple yet illustrative of key networking concepts.

Running Environment
Server: Runs on Ubuntu 20.04.6 LTS with Python version 3.8.10.
Client: Can be run on any system with Python 3.8.10 or compatible versions.

Client Program - reversetcpclient.py
How to Run
Open a terminal and run the client program using the following command format:

python reversetcpclient.py --serverIP <IP_ADDRESS> --serverPort <PORT> --fileSize <FILE_SIZE> --Lmin <MIN_BLOCK_SIZE> --Lmax <MAX_BLOCK_SIZE>
For example:

python reversetcpclient.py --serverIP 192.168.10.130 --serverPort 12345 --fileSize 1000 --Lmin 10 --Lmax 150
If no arguments are provided, the client will use default values.

Command Line Arguments
--serverIP: The IP address of the server. Default is 192.168.10.130.
--serverPort: The port on which the server is listening. Default is 12345.
--fileSize: The size of the file to be reversed. Default is 1000 characters.
--Lmin: The minimum block size for reversing. Default is 10 bytes.
--Lmax: The maximum block size for reversing. Default is 150 bytes.

Server Program - reversetcpserver.py
How to Run
On the server machine, open a terminal and start the server with:

python reversetcpserver.py
The server does not require command line arguments and will start listening for incoming connections on the default port.

Configuration Options
Buffer Size: Set by the bufferSize variable in both client and server scripts. Default is 1024 bytes.

Note
Ensure that the server is running before starting the client.
The client and server must agree on the IP address and port for successful communication.

Getting Started
1. Start the server on the designated machine.
2. On the client machine, open a terminal and navigate to the directory containing reversetcpclient.py.
3. Run the client with the desired command line arguments or use the defaults.

Additional Information
This program is for educational purposes and simulates aspects of network communication using TCP. It demonstrates the process of file block reversal upon request.

For any issues or feature requests, please create an issue on the associated GitHub repository.