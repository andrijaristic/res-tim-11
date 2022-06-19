from json import load
from load_balancer import LoadBalancer
from threading import Thread
import socket

if __name__ == '__main__':
    try:
        server_client_address = ('localhost',20000)
        server_worker_address = ('localhost',21000)
        local_buffer = []
        client_connections = []
        worker_connections = []
        worker_availabilty = []
        load_balancer = LoadBalancer()
        client_socket = load_balancer.create_socket(server_client_address)
        client_socket.listen(1)
        new_thread = Thread(target=load_balancer.start_listening_clients, args=(client_socket,client_connections,local_buffer,worker_connections,worker_availabilty))
        new_thread.daemon = True
        new_thread.start()
        worker_socket = load_balancer.create_socket(server_worker_address)
        worker_socket.listen(1)
        worker_thread = Thread(target=load_balancer.start_listening_workers, args=(worker_socket,worker_connections,worker_availabilty))
        worker_thread.daemon = True
        worker_thread.start()
        send_thread = Thread(target=load_balancer.check_data_for_sending,args=(local_buffer,worker_connections,worker_availabilty))
        send_thread.daemon = True
        send_thread.start()
        end_thread = Thread(target=load_balancer.close_all_connections, args=(client_connections,worker_connections,worker_availabilty))
        end_thread.start()
    except:
        print('Exception')
        exit()