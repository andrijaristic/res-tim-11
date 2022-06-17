import socket
import datetime

class Writer:
    def __init__(self, server_adresa):
        self.server_adresa = server_adresa
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.server_adresa)

# initial commit

    def run(self):
        while(True):
            print("1 - Slanje podataka\n2 - Paljenje Worker komponente\n3 - Gasenje Worker komponente\n4 - Zatvaranje konekcije\nOdaberite komandu: ",end="")               
            try:
                komanda = int(input())
                poruka = ""
                if(komanda == 1):
                    poruka = self.input_and_validate_data()
                elif(komanda == 2):
                    poruka = "On-0"
                elif(komanda == 3):
                    poruka = "Off-0"
                elif(komanda == 4):
                    poruka = "Exit-0"
                else:
                    print("Zadata komanda ne postoji!")
                if(poruka != ""):                                               
                    poruka = poruka.encode()
                    self.sock.sendall(poruka)
                    odgovor = self.sock.recv(1024)
                    if(odgovor):
                        poruka = odgovor.decode()
                        print(poruka)
                    else:
                        self.sock.close()
                        break    
            except ValueError:
                print("Morate uneti broj")
            except:
                print("Greska! Poruka nije uspesno poslata!")

    def input_and_validate_data(self):
        try:
            print("Unesite ID brojila: ",end="")
            id = int(input())
            print("Unesite vrednost: ",end="")
            value = int(input())
            e = datetime.datetime.now()
            datum_vreme = e.strftime("%d.%m.%Y;%H:%M:%S")
            return "Send-" + str(id) + "-" + str(value) + "-" + str(datum_vreme)
        except ValueError:
            print("Greska. Vrednosti moraju biti celobrojne.")
            return ""
        except:
            print("Greska!")
            return ""

