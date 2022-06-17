import socket
from time import sleep
from tkinter.tix import Tree


class Worker:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.database_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connecttoloadbalancer(self,address): # pragma: no cover
        try:
            self.server_socket.connect(address)
            return True
        except:
            return False
    def connecttodatabasecrud(self,address): # pragma: no cover
        try:
            self.database_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.database_socket.connect(address)
            return True
        except:
            return False
    def run(self): # pragma: no cover
        while True:
            data = self.receivedata(self.server_socket)
            if data:
                self.checkdata(data)
                self.database_socket.sendall(data)
                self.send('Upesno slanje',self.database_socket)
                data2 = self.receivereply(self.database_socket)
                if data2:
                    print(data2)
            else:
                exit()
    def receivedata(self,sock):
        data = sock.recv(1024)
        return data
    def checkdata(data):
        s = data.decode()
        if s.count(';')==10 and s.count('-')==20:
            return True
        else:
            raise TypeError("Wrong format!")
    def send(self,message,sock):
        try:
            message = message.encode()
            sock.sendall(message)
            return True
        except:
            return False
    def receivereply(self,sock):
        data = sock.recv(1024)
        return data

