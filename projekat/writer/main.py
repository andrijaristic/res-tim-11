from writer import Writer

if __name__ == '__main__':
    server_adresa = ('localhost', 20000)
    writer = Writer()
    socket = writer.create_socket(server_adresa)
    writer.run(socket)
         