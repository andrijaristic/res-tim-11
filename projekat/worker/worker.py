from classes import Worker

if __name__ == '__main__':
    loadbalancer_address = ('localhost', 21000)
    databasecrud_address = ('localhost', 22000)
    worker = Worker()
    worker.connecttodatabasecrud(databasecrud_address)
    worker.connecttoloadbalancer(loadbalancer_address)
    worker.run()
    