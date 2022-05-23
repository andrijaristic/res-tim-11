from threading import Thread
import socket


class LoadBalancer:
    def __init__(self,server_client_address):
        self.server_client_address = server_client_address
        self.buffer = []
        self.client_connections = []
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.bind(self.server_client_address)
        self.client_socket.listen(1)

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


    def close_all_connections(self):
        while True:
            message = input()
            if(message.lower() == 'end'):
                break
        for x in self.client_connections:
            x.close()
        # TO DO : close worker connections