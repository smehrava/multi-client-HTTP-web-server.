#Author : Sara Mehravar
#stuent ID : 251185394

from socket import socket, AF_INET, SOCK_STREAM
import sys

serverIP = '127.0.0.1'
#we want server to read the second command line argumenent which in the example given for assignment is 9200
serverPort = int(sys.argv[1])

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))
print("Connection established")

try:
    #we want server to read the third command line argumenent which in the example given for assignment is hello.html
    fileName = sys.argv[2]
    # +   +
    #get request
    message = f'GET /{fileName} HTTP/1.1\r\nHOST:{serverIP}\r\n\r\n'
    clientSocket.send(message.encode())
    output = clientSocket.recv(1024)

    #if the file has been found:
    if b'HTTP/1.1 200 OK' in output:
        fileData = output.split(b'\r\n\r\n')[1]
        response = fileData.decode()
        print(response)
        #saving the content of the html file in another file named save.html
        with open("save.html", "w") as file:
            file.write(response)
            print("Content saved to save.html")

        #making sure the file has been succesfully made and it contains the content from hello.html
        with open("save.html","rb") as file:
            print(file.read())

    #in case file has not been found, printing file not found
    elif b'HTTP/1.1 404 Not Found' in output:
        print("File not found.")

except Exception as e:
    print("Error:", e)

finally:
    clientSocket.close()
    print('Connection closed')
