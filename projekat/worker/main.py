from worker import Worker

if __name__ == '__main__':
    loadbalancer_address = ('localhost', 21000)
    databasecrud_address = ('localhost', 22000)
    worker = Worker()
    worker.connect_to_databasecrud(databasecrud_address)
    worker.connect_to_load_balancer(loadbalancer_address)
    worker.run()
    
