import socket


class DatabaseAnalytics:
    def __init__(self):
        self.databasecrud_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect_to_databasecrud(self,databasecrud_address): # pragma: no cover 
        try:
            self.databasecrud_socket.connect(databasecrud_address)
            return True
        except:
            return False
    def kreiraj_naziv_fajla_grad(self,nazivgrada):
        x = nazivgrada.split(' ')
        naziv = ''
        for n in x:
            naziv = naziv + n
            nazivfajla = naziv + 'izvestaj.txt'
        return nazivfajla
    def run(self):  # pragma: no cover 
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
                p = data2.decode()
                if(p=='Merenja ne postoje'):
                    print('Merenja ne postoje')
                    continue
                nazivfajla = self.kreirajnazivfajlagrad(grad)
                self.upisi_u_fajl_grad(nazivfajla, grad, data2)
                print('Uspesan upis')
            elif komanda == '2':
                print('Unesite brojilo:')
                brojilo = input()
                message = 'brojilo:' + brojilo
                data = message.encode()
                self.databasecrud_socket.sendall(data)
                data2 = self.databasecrud_socket.recv(1024)
                p = data2.decode()
                if(p=='Merenja ne postoje'):
                    print('Merenja ne postoje')
                    continue
                nazivfajla = 'izvestaj' + brojilo + '.txt'
                self.upisi_u_fajl_brojilo(nazivfajla, brojilo, data2)
                print('Uspesan upis')
            elif komanda == '3':
                exit()
            else:
                print('Pogresna komanda')
                continue

    def meni(self): # pragma: no cover
        print('1 - Izvestaj o potrosnji po mesecima za odredjeni grad')
        print('2 - Izvestaj o potrosnji po mesecima za odredjeno brojilo')
        print('3 - Izlaz')

    def upisi_u_fajl_grad(self, nazivfajla, grad, data): 
        fajl = open(nazivfajla, 'w+')
        data = data.decode()
        fajl.write('Izvestaj za grad : ' + grad + '\n')
        fajl.write('Mesec  Potrosnja \n')
        linije = data.split(';')
        for linija in linije:
            t = linija.split('-')
            fajl.write(' ' + t[0] + '      ' + t[1] + '\n')
        fajl.close()

    def upisi_u_fajl_brojilo(self, nazivfajla, brojilo, data):
        fajl = open(nazivfajla, 'w+')
        data = data.decode()
        fajl.write('Izvestaj za brojilo : ' + brojilo + '\n')
        fajl.write('Mesec  Potrosnja \n')
        linije = data.split(';')
        for linija in linije:
            t = linija.split('-')
            fajl.write(' ' + t[0] + '      ' + t[1] + '\n')
        fajl.close()
