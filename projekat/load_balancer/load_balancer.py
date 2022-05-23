from json import load
from classes import LoadBalancer
from threading import Thread

if __name__ == '__main__':
    server_client_address = ('localhost',20000)
    server_worker_address = ('localhost',21000)
    load_balancer = LoadBalancer(server_client_address,server_worker_address)
    new_thread = Thread(target=load_balancer.start_listening_clients)
    new_thread.daemon = True
    new_thread.start()
    worker_thread = Thread(target=load_balancer.start_listening_workers)
    worker_thread.daemon = True
    worker_thread.start()
    end_thread = Thread(target=load_balancer.close_all_connections)
    end_thread.start()