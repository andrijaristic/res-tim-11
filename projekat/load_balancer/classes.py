from threading import Thread
import socket
import os
import threading
import time


class LoadBalancer:
    def __init__(self):
        self.mutex_buffer = threading.Semaphore(1)
        self.mutex_worker = threading.Semaphore(1)

    def create_socket(self,adresa):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(adresa)
        sock.listen(1)
        return sock

    def start_listening_clients(self,client_socket,client_connections,local_buffer,worker_connections,worker_availabilty):
        print('Listening for client requests')
        try:
            while True:
                connection, client_address = client_socket.accept()
                client_connections.append(connection)
                new_thread = Thread(target=self.handle_client, args=(connection,client_address,client_connections,local_buffer,worker_connections,worker_availabilty))
                new_thread.start()
        except:
            exit()

    def start_listening_workers(self,worker_socket,worker_connections,worker_availabilty):
        try:
            while True:
                connection, worker_address = worker_socket.accept()
                worker_connections.append(connection)
                worker_availabilty.append(True)
        except:
            exit()

    def handle_client(self,connection,client_address,client_connections,local_buffer,worker_connections,worker_availabilty):
        while True:
            data = self.receive_data(connection)
            if(data):
                message = self.get_message_from_data(data)
                command = self.get_command_from_message(message)
                if(command.lower() == "send"):
                    command_parameters = self.get_parameters_from_message(message)
                    self.mutex_buffer.acquire()
                    data_stored = self.store_data(local_buffer,command_parameters)
                    self.mutex_buffer.release()
                    reply = self.generate_send_reply(data_stored,local_buffer)
                    prepared_reply = self.prepare_reply(reply)
                    reply_sent = self.send_reply_to_client(connection,client_address,prepared_reply)
                    if(reply_sent == False):
                        print('Failed to send reply to the client, reply : ' + reply)
                elif(command.lower() == "exit"):
                    connection_closed = self.close_client_connection(connection,client_connections)
                    if(connection_closed):
                        break
                    print('Failed to close a connection')
                elif(command.lower() == "on"):
                    dir = os.path.dirname(__file__)
                    file_name = os.path.join(dir,'..','worker','worker.py')
                    worker_started = self.start_worker(file_name)
                    reply = self.generate_on_reply(worker_started)
                    prepared_reply = self.prepare_reply(reply)
                    reply_sent = self.send_reply_to_client(connection,client_address,prepared_reply)
                    if(reply_sent == False):
                        print('Failed to send reply to the client, reply : ' + reply)
                elif(command.lower() == "off"):
                    all_workers_available = self.check_worker_availabilty(worker_availabilty)
                    worker_turned_off = False
                    if(all_workers_available):
                        self.mutex_worker.acquire()
                        index = self.find_available_worker(worker_availabilty)
                        worker_turned_off = self.turn_off_worker(index,worker_connections,worker_availabilty)
                        self.mutex_worker.release()
                    reply = self.generate_off_reply(all_workers_available,worker_turned_off)
                    prepared_reply = self.prepare_reply(reply)
                    reply_sent = self.send_reply_to_client(connection,client_address,prepared_reply)
                    if(reply_sent == False):
                        print('Failed to send reply to the client, reply : ' + reply)
                else:
                    reply = "Unknown command"
                    prepared_reply = self.prepare_reply(reply)
                    reply_sent = self.send_reply_to_client(connection,client_address,prepared_reply)
                    if(reply_sent == False):
                        print('Failed to send reply to the client, reply : ' + reply)
            else:
                connection_closed = self.close_client_connection(connection,client_connections)
                if(connection_closed):
                    break
                print('Failed to close a connection')

    def receive_data(self,connection):
        return connection.recv(1024)

    def get_message_from_data(self,data):
        return data.decode()

    def get_command_from_message(self,message):
        return message.split("-")[0]

    def get_parameters_from_message(self,message):
        return message.split("-")[1] + "-" + message.split("-")[2] + "-" + message.split("-")[3]

    def generate_send_reply(self,data_stored,local_buffer):
        if type(data_stored) != bool:
            raise TypeError('data_stored must be a bool')
        reply = ""
        if(data_stored):
            reply = "Data stored " + str(len(local_buffer))
        else:
            reply = "Local buffer is full"
        return reply

    def generate_on_reply(self,worker_started):
        if type(worker_started) != bool:
            raise TypeError('worker_started must be a bool')
        reply = ""
        if(worker_started):
            reply = "New worker started working"
        else:
            reply = "Failed to start a new worker"
        return reply

    def generate_off_reply(self,all_workers_available,worker_turned_off):
        if type(all_workers_available) != bool:
            raise TypeError('all_workers_available must be a bool')
        if type(worker_turned_off) != bool:
            raise TypeError('worker_turned_off must be a bool')
        reply = ""
        if(all_workers_available == False):
            reply = "Cannot turn off workers while they are working"
        else:
            if(worker_turned_off):
                reply = "Worker turned off"
            else:
                reply = "Failed to turn off a worker"
        return reply

    def prepare_reply(self,reply):
        if type(reply) != str:
            raise TypeError('Reply is not a string')
        return reply.encode()

    def store_data(self,local_buffer,data):
        if(len(local_buffer) >= 10):
            return False
        if type(data) != str:
            raise TypeError('Data is not a string')
        local_buffer.append(data)
        return True
        
    def send_reply_to_client(self,connection,client_address,reply):
        try:
            connection.sendto(reply,client_address)
            return True
        except:
            return False

    def close_client_connection(self,connection,client_connections):
        try:
            client_connections.remove(connection)
            connection.close()
            return True
        except:
            return False

    def start_worker(self,file_name):
        try:
            os_thread = Thread(target=self.start_worker_app, args=(file_name,))
            os_thread.start()
            return True
        except:
            return False

    def find_available_worker(self,worker_availabilty):
        for i in range(len(worker_availabilty)):
            if(worker_availabilty[i]):
                return i
        return -1

    def turn_off_worker(self,index,worker_connections,worker_availabilty):
        try:
            worker = worker_connections[index]
            del worker_connections[index]
            del worker_availabilty[index]
            worker.close()
            return True
        except:
            return False

    def check_data_for_sending(self,local_buffer,worker_connections,worker_availabilty):
        while True:
            self.mutex_buffer.acquire()
            if(len(local_buffer) >= 10):
                self.mutex_worker.acquire()
                index = self.find_available_worker(worker_availabilty)
                if(index == -1):
                    self.mutex_buffer.release()
                    self.mutex_worker.release()
                    time.sleep(1)
                    continue
                worker = self.get_worker(index,worker_connections)
                message = self.convert_data_to_message(local_buffer)
                self.mutex_buffer.release()
                prepared_message = self.prepare_reply(message)
                message_sent = self.send_message_to_worker(index,worker,worker_availabilty,prepared_message)
                if(message_sent):
                    data = self.receive_data(worker)
                    if(data):
                        worker_availabilty[index] = True
                        worker_reply = self.get_message_from_data(data)
                        print(worker_reply)
                    else:
                        print('Error receiver reply from worker, turning it off : ')
                        worker_turned_off = self.turn_off_worker(index,worker_connections,worker_availabilty)
                        if(worker_turned_off):
                            print('Worker turned off')
                        else:
                            print('Failed to turn off worker')
                else:
                    print('Failed to send message to the worker')
                self.mutex_worker.release()
            self.mutex_buffer.release()
            time.sleep(1)
            
    def send_message_to_worker(self,index,worker,worker_availabilty,message):
        try:
            worker.sendall(message)
            worker_availabilty[index] = False
            return True
        except:
            return False

    def convert_data_to_message(self,local_buffer):
        message = ""
        for i in range(len(local_buffer)):
            if(i == len(local_buffer) - 1):
                message += local_buffer[i]
            else:
                message += local_buffer[i] + ";"
        local_buffer.clear()
        return message;

    def get_worker(self,index,worker_connections):
        if type(index) != int:
            raise TypeError('Index must be an integer')
        if(index == -1):
            raise IndexError('Index out of range') 
        return worker_connections[index]

    def start_worker_app(self, file_name):
        os.system(file_name)

    def check_worker_availabilty(self,worker_availabilty):
        for available in worker_availabilty:
            if (available == False):
                return False
        return True

    def close_all_connections(self, client_connections,worker_connections,worker_availabilty):
        try:
            while True:
                message = input()
                if(len(client_connections) != 0):
                    print('There are clients connected to the load balancer')
                    continue
                if(message.lower() == 'end'):
                    break
            for x in client_connections:
                x.close()
            client_connections.clear()
            for x in worker_connections:
                x.close()
            worker_connections.clear()
            worker_availabilty.clear()
        except:
            exit()