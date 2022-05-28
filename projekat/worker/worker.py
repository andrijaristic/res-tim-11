from classes import Worker

if __name__ == '__main__':
    loadbalancer_address = ('localhost', 21000)
    databasecrud_address = ('localhost', 22000)
    worker = Worker(loadbalancer_address,databasecrud_address)
    worker.run()
