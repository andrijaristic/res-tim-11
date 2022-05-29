from threading import Thread
import socket

class Database:
    def __init__(self, worker_listening_address, analytics_listening_address, cnxn_str):
        self.worker_address = worker_listening_address
        self.analytics_address = analytics_listening_address
        self.conn_str = cnxn_str

        self.worker_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.worker_socket.bind(self.worker_address)
        self.worker_socket.listen(1)

        self.analytics_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.analytics_socket.bind(self.analytics_address)
        self.analytics_socket.listen(1)

    def start_listening_worker(self):
        try:
            while True:
                connection, worker_address = self.worker_socket.accept()
                new_thread = Thread(target=self.handle_worker, args=(connection,))
                new_thread.start()
        except:
            exit()

    def start_listening_analytics(self):
        try:
            while True:
                connection, analytics_address = self.analytics_socket.accept()
                new_new_thread = Thread(target=self.handle_analytics, args=(connection, analytics_address))
                new_new_thread.start()
        except:
            exit()

    def handle_worker(self, connection):
        while True:
            data = connection.recv(1024)

            if(data):
                message = data.decode()
                print(message)
                #id = message.split("-")[0]
                #value = message.split("-")[1]
                #date = message.split("-")[2]
                # Pozove CREATE metodu.
            else:
                connection.close()
                break

    def handle_analytics(self, connection, analytics_address):
        while True:
            data = connection.recv(1024)

            if(data):
                message = data.decode()
                print(message)
                # Smisliti izgled poruke koja ce biti poslata.
            else:
                connection.close()
                break
