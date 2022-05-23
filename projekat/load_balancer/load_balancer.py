from classes import LoadBalancer
from threading import Thread

if __name__ == '__main__':
    server_client_address = ('localhost',20000)
    load_balancer = LoadBalancer(server_client_address)
    new_thread = Thread(target=load_balancer.start_listening_clients)
    new_thread.daemon = True
    new_thread.start()
    end_thread = Thread(target=load_balancer.close_all_connections)
    end_thread.start()