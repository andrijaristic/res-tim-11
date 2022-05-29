import socket


class DatabaseAnalytics:
    def __init__(self, databasecrud_address):
        self.databasecrud_address = databasecrud_address
        self.databasecrud_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.databasecrud_socket.connect(databasecrud_address)


    def run(self):
        while True:
            self.meni()
            komanda = input()
            if komanda == '1':
                print('Unesite grad:')
                grad = input()
                message = 'grad:' + grad
                data = message.encode()
                self.databasecrud_socket.sendall(data)
                data2 = self.databasecrud_socket.recv(1024)
                x = grad.split(' ')
                naziv = ''
                for n in x:
                    naziv = naziv + n
                nazivfajla = naziv + 'izvestaj.txt'
                fajl = open(nazivfajla, 'w+')
                self.upisiufajlgrad(fajl, grad, data2)
                print('Uspesan upis')
            elif komanda == '2':
                print('Unesite brojilo:')
                brojilo = input()
                message = 'brojilo:' + brojilo
                data = message.encode()
                self.databasecrud_socket.sendall(data)
                data2 = self.databasecrud_socket.recv(1024)
                nazivfajla = 'izvestaj' + brojilo + '.txt'
                fajl = open(nazivfajla, 'w+')
                self.upisiufajlbrojilo(fajl, brojilo, data2)
                print('Uspesan upis')
            else:
                exit()

    def meni(self):
        print('1 - Izvestaj o potrosnji po mesecima za odredjeni grad')
        print('2 - Izvestaj o potrosnji po mesecima za odredjeno brojilo')
        print('3 - Izlaz')

    def upisiufajlgrad(self, fajl, grad, data):
        data = data.decode()
        fajl.write('Izvestaj za grad : ' + grad + '\n')
        fajl.write('Mesec  Potrosnja \n')
        linije = data.split(';')
        for linija in linije:
            t = linija.split('-')
            fajl.write(' ' + t[0] + '      ' + t[1] + '\n')

    def upisiufajlbrojilo(self, fajl, brojilo, data):
        data = data.decode()
        fajl.write('Izvestaj za brojilo : ' + brojilo + '\n')
        fajl.write('Mesec  Potrosnja \n')
        linije = data.split(';')
        for linija in linije:
            t = linija.split('-')
            fajl.write(' ' + t[0] + '      ' + t[1] + '\n')
