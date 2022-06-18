from crud_operations import CrudOperations

from threading import Thread
from time import sleep
import socket
import coverage

class DatabaseCrud:
    def __init__(self):
        self.crud_operations = CrudOperations()

    def create_socket(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(address)
        sock.listen(1)
        return sock

    def start_listening_worker(self, worker_socket, cnxn): # pragma: no cover
        try:
            while True:
                connection, worker_address = worker_socket.accept()
                new_thread = Thread(target=self.handle_worker, args=(connection, cnxn))
                new_thread.start()
        except:
            exit()

    def start_listening_analytics(self, analytics_socket, cnxn): # pragma: no cover
        try:
            while True:
                connection, analytics_address = analytics_socket.accept()
                new_new_thread = Thread(target=self.handle_analytics, args=(connection, analytics_address, cnxn))
                new_new_thread.start()
        except:
            exit()

    def handle_worker(self, connection, cnxn): # pragma: no cover
        while True:
            data = self.receive_data(connection)

            if(data):
                buffer = []
                message = self.get_message_from_data(data)
                buffer = message.split(";")

                for message in buffer:
                    id, value, date = self.get_params_from_worker_message(message)
                    self.crud_operations.create_brojilo_potrosnja(cnxn, id, value, date)
                    sleep(0.2)
            else:
                connection_closed = self.close_connection(connection)
                if (connection_closed):
                    break
                print("Failed to close connection.\n")

    def handle_analytics(self, connection, analytics_address, cnxn): # pragma: no cover
        while True:
            data = self.receive_data(connection)

            if(data):
                message = self.get_message_from_data(data)
                field, value = self.get_params_from_analytics_message(message)
                response = ""

                if (field.lower() == "brojilo"):
                    response = self.crud_operations.read_brojilo_potrosnja_id(cnxn, value)
                elif (field.lower() == "grad"):
                    response = self.crud_operations.read_brojilo_potrosnja_grad(cnxn, value)

                response = self.prepare_response(response)

                send_response = self.send_response(connection, response, analytics_address)
                if send_response == False:
                    print(f"Failed to send response to DATABASE_ANALYTICS.\nResponse: {response}")

            else:
                connection_closed = self.close_connection(connection)
                if (connection_closed):
                    break
                print("Failed to close connection.\n")

    def receive_data(self, connection):
        return connection.recv(1024)

    def get_message_from_data(self, data):
        return data.decode()

    def get_params_from_worker_message(self, message):
        if type(message) is not str:
            raise TypeError('Message must be string')
        return message.split("-")[0], message.split("-")[1], message.split("-")[2]

    def get_params_from_analytics_message(self, message):
        if type(message) is not str:
            raise TypeError('Message must be string')
        return message.split(":")[0], message.split(":")[1]

    def prepare_response(self, response):
        if type(response) is not str:
            raise TypeError('Response must be string')
        return response.encode()

    def send_response(self, connection, response, address):
        if type(response) is not bytes:
            raise TypeError('Reply must be bytes')
        
        try:
            connection.sendto(response, address)
            return True
        except Exception:
            return False

    def close_connection(self, connection):
        try:
            connection.close()
            return True
        except Exception:
            return False