from threading import Thread
import socket


class LoadBalancer:
    def __init__(self,server_client_address,server_worker_address):
        self.server_client_address = server_client_address
        self.server_worker_address = server_worker_address
        self.buffer = []
        self.client_connections = []
        self.worker_connections = []
        self.worker_availabilty = []
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.bind(self.server_client_address)
        self.client_socket.listen(1)
        self.worker_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.worker_socket.bind(self.server_worker_address)
        self.worker_socket.listen(1)

    def start_listening_clients(self):
        print('Listening for client rquests')
        try:
            while True:
                connection, client_address = self.client_socket.accept()
                self.client_connections.append(connection)
                new_thread = Thread(target=self.handle_client, args=(connection,client_address))
                new_thread.start()
        except:
            exit()

    def start_listening_workers(self):
        try:
            while True:
                connection, worker_address = self.worker_socket.accept()
                self.worker_connections.append(connection)
                self.worker_availabilty.append(True)
        except:
            exit()

    def handle_client(self,connection,client_address):
        while True:
            data = connection.recv(1024)
            if(data):
                message = data.decode()
                command = message.split("-")[0]
                if(command.lower() == "send"):
                    command_parameters = message.split("-")[1] + "-" + message.split("-")[2]
                    self.buffer.append(command_parameters)
                    reply = "Primljeno"
                    reply = reply.encode()
                    connection.sendto(reply,client_address)
                    if(len(self.buffer) == 10):
                        # TO DO : send data to worker
                            pass
                elif(command.lower() == "exit"):
                    connection.close()
                    self.client_connections.remove(connection)
                    break
                # TO DO : add cases for other command types
            else:
                connection.close()
                self.client_connections.remove(connection)
                break

    def find_available_worker(self):
        for i in range(len(self.worker_availabilty)):
            if(self.worker_availabilty[i]):
                return i
        return -1

    def close_all_connections(self):
        while True:
            message = input()
            if(message.lower() == 'end'):
                break
        for x in self.client_connections:
            x.close()
        self.client_connections.clear()
        for x in self.worker_connections:
            x.close()
        self.worker_connections.clear()
        self.worker_availabilty.clear()