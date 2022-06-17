from writer import Writer

if __name__ == '__main__':
    server_adresa = ('localhost', 20000)
    writer = Writer(server_adresa)
    writer.run()
         