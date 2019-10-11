#-------------------------------------------------------------------------------
# Name:        FTP client
# Author:      Brandon Griggs
#-------------------------------------------------------------------------------

import socket
import os


def client_program():
    host = "127.0.0.2"  # as both code is running on same pc
    port = 8080  # socket server port number

    client_socket = socket.socket()  # instantiate
    message = input(" -> ")  # take input
    msg = message.split(" ")
    print(msg[0])
    while msg[0].lower().strip() != 'quit':
        if msg[0].lower().strip() == 'connect':
            client_socket.connect((msg[1], int(msg[2])))  # connect to the server
            print("Connection made")
        if msg[0].lower().strip() == 'store':
            client_socket.send(bytes(message,'utf-8'))
            filename=msg[1]
            f = open(filename,'rb')
            l = f.read(1024)
            while (l):
                client_socket.send(l)
                l = f.read(1024)
            f.close()
            print('File stored')

        if msg[0].lower().strip() == 'retrieve':
            client_socket.send(bytes(message,'utf-8'))
            filename=msg[1]
            f = open(filename,"w")
            data = client_socket.recv(1024).decode()
            f.write(data)
            f.close()
            print('file retrieved')

        if msg[0].lower().strip() == 'list':
            client_socket.send(bytes(message,'utf-8'))
            data = client_socket.recv(1024).decode()
            print(data)

        message = input(" -> ")  # again take input
        msg = message.split(" ")

    client_socket.close()  # close the connection
    print('connection terminated')


if __name__ == '__main__':
    client_program()
