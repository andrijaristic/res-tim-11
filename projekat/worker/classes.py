import socket


class Worker:
    def __init__(self, address, databasecrud_address):
        self.address = address
        self.databasecrud_address = databasecrud_address
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server_socket.bind(self.address)
        #self.server_socket.listen(1)
        self.server_socket.connect(address)
        self.database_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.database_socket.bind(self.databasecrud_address)
        self.database_socket.listen(1)
        #self.database_socket.connect(databasecrud_address)


    def run(self):
        connection,x = self.database_socket.accept()
       # self.server_socket.connect(self.address)
        while True:
            data = self.server_socket.recv(1024)
            if data:
                # print(data.decode())
                connection.sendall(data)
                message = 'Uspesno slanje'
                message = message.encode()
                self.server_socket.sendall(message)
                data2 = connection.recv(1024)
                if data2:
                    print('Uspesno slanje')
                else:
                    print('Neuspesno slanje')
            else:
                exit()
