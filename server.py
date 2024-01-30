#Author : Sara Mehravar
#stuent ID : 251185394

import socket
import os
import sys
from _thread import *
import threading

from socket import AF_INET, SOCK_STREAM

#we want server to read the third command line argumenent which in the example given for assignment is 3
max_connections = int(sys.argv[2])
serverSocket = socket.socket(AF_INET, SOCK_STREAM)

#we want server port to be the seond command line arguement which in the example provided in the assignment is 9200
#first the server binds and then listens
serverPort = int(sys.argv[1])
serverSocket.bind(("127.0.0.1", serverPort))
print('Server started on port', serverPort)
serverSocket.listen(max_connections)
server_running = True

#making another function
#we can add all these lines inside the function in the while,try loop but we need them to be in another function
#because of threading
#the program will first go through while loop and once threading.thread calls this function, program will go through the code inside this function
def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()

        #checking if the message is not none which means that the message has been received
        if message is not None:
            print("Received message:", message)

        # Parse the GET request
        #splitting the message into 2 sides (before HTTP/1.1 and after http/1.1)
        request = message.split("HTTP/1.1")
        #we want the part before HTTP/1.1 ad we are splitting it into beofre / and after /
        request = request[0].split("/")
        #we want after /
        filename = request[1]
        #this will give the file name

        #opening the file and reading it
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                fileData = file.read()
                print(fileData)

            # Create the HTTP response
            response = f'HTTP/1.1 200 OK\r\n\r\n'.encode() + fileData
            connectionSocket.send(response)
            print('Connection established')

        else:
            # in case file has not been found
            response = 'HTTP/1.1 404 Not Found\r\n\r\nFile not found.'.encode()
            connectionSocket.send(response)
            print("File not found:", filename)

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the client connection
        connectionSocket.close()
        print('Connection closed')



try:
    while True:
        connectionSocket, addr = serverSocket.accept()
        print('Connection accepted')

        #threading.Thread(); function name and the arguement that the function accepts.
        #threading so that server can handle multiple clients at the same time.
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
        client_thread.start()

except Exception as e:
    print("Error:", e)

finally:
    serverSocket.close();
    print("server closed")



