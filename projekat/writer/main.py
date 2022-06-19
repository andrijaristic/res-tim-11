from writer import Writer

if __name__ == '__main__':
    try:
        server_adresa = ('localhost', 20000)
        writer = Writer()
        socket = writer.create_socket(server_adresa)
        writer.run(socket)
    except:
        print("Greska main")
        exit()
         