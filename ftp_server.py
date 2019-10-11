#-------------------------------------------------------------------------------
# Name:        FTP server
# Author:      Brandon Griggs
#-------------------------------------------------------------------------------

import socket, threading
import os


class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
    def run(self):
        msg = ''
        while True:
            msg = ''
            sendstring = ''
            data = self.csocket.recv(2048)
            message = data.decode()
            msg = message.split(' ')
            if (len(message)>0):
                if (msg[0]=="quit"):
                    print("socket closed")
                    self.csocket.close()
                    break
                elif(msg[0]=='retrieve'):
                    reqFile = msg[1]
                    file_to_read = open(reqFile,"rb")
                    l = file_to_read.read()
                    while (l):
                        self.csocket.send(l)
                        l = file_to_read.read()
                    print ('Send Successful')
                    file_to_read.close()
                elif(msg[0]=='store'):
                    reqFile = msg[1]
                    file_to_write = open(reqFile,"w")
                    l = self.csocket.recv(1024).decode()
                    file_to_write.write(l)
                    file_to_write.close()
                    print('File stored')
                elif(msg[0]=='list'):
                    files = os.listdir(os.curdir)
                    smg = ""
                    for f in files:
                        smg = smg + '\n' + f
                    print(smg)
                    self.csocket.send(smg.encode('utf-8'))
                    print('List shared')
        print ("user disconnected...")
LOCALHOST = "127.0.0.2"
PORT = 8080
server = socket.socket()
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
