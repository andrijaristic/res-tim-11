import socket
import datetime

class Writer:      
    def create_socket(self, adresa):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(adresa)
        return sock

    def run(self, socket):
        while(True):                                    
            komanda = self.get_input("1 - Slanje podataka\n2 - Paljenje Worker komponente\n3 - Gasenje Worker komponente\n4 - Zatvaranje konekcije\nOdaberite komandu: ")
            poruka = self.switch_komanda(komanda)               
            self.send_message(poruka, socket)           


    def send_message(self ,poruka, socket):
        if(type(poruka) != str):
            raise TypeError("Poruka treba da bude string!")
        try:
            if(poruka):                                               
                poruka = poruka.encode()
                socket.sendall(poruka)
                odgovor = socket.recv(1024)
                if(odgovor):
                    poruka = odgovor.decode()
                    print(poruka)
                else:
                    socket.close()
                return True
            else:
                return False
        except:
            print("Greska!")
            return False
                

    def switch_komanda(self, komanda):
        if(type(komanda) != int):
            raise TypeError("Komanda nije int!")
        if(komanda == 1):
            id = self.get_input("Unesite ID brojila: ")          
            value = self.get_input("Unesite vrednost: ")
            poruka = self.format_message(id, value)
            return poruka
        elif(komanda == 2):
            poruka = "On-0"
            return poruka
        elif(komanda == 3):
            poruka = "Off-0"
            return poruka
        elif(komanda == 4):
            poruka = "Exit-0"
            return poruka
        else:
            print("Zadata komanda ne postoji!")
            return False


    def format_message(self, id, value):
        if(type(id) != int):
            raise TypeError("ID nije int!")
        if(type(value) != int):
            raise TypeError("Vrednost nije int!")
        try:                   
            e = datetime.datetime.now()
            datum_vreme = e.strftime("%d.%m.%Y;%H:%M:%S")
            return "Send-" + str(id) + "-" + str(value) + "-" + str(datum_vreme)       
        except:
            print("Greska!")
            return False


    def get_input(self, text):
        if(type(text) != str):
            raise TypeError("Text treba da bude string!")
        try:
            return int(input(text))
        except ValueError:
            print("Greska. Vrednosti moraju biti celobrojne.")
            return False

    