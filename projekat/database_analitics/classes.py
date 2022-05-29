import socket


class DatabaseAnalytics:
    def __init__(self, databasecrud_address):
        self.databasecrud_address = databasecrud_address
        self.databasecrud_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.databasecrud_socket.connect(databasecrud_address)


