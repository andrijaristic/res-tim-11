import socket


class Worker:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.database_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect_to_load_balancer(self,address): # pragma: no cover
        try:
            self.server_socket.connect(address)
            return True
        except:
            return False
    def connect_to_databasecrud(self,address): # pragma: no cover
        try:
            self.database_socket.connect(address)
            return True
        except:
            return False
    def run(self): # pragma: no cover
        while True:
            data = self.receive_data(self.server_socket)
            if data:
                self.check_data(data)
                self.database_socket.sendall(data)
                self.send_m('Upesno slanje',self.server_socket)
                data2 = self.receive_reply(self.database_socket)
                if data2:
                    print(data2)
                else:
                    exit()
            else:
                exit()
    def receive_data(self,sock):
        data = sock.recv(1024)
        return data
    def check_data(self,data):
        s = data.decode()
        if s.count(';')==9 and s.count('-')==20:
            return True
        else:
            raise TypeError("Wrong format!")
    def send_m(self,message,sock):
        message = message.encode()
        sock.sendall(message)
        return True
    def receive_reply(self,sock):
        data = sock.recv(1024)
        return data

