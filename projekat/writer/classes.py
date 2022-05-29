import socket
import datetime

class Writer:
    def __init__(self, server_adresa):
        self.server_adresa = server_adresa
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        while(True):
            print("1 - Slanje podataka\n2 - Paljenje Worker komponente\n3 - Gasenje Worker komponente\n4 - Zatvaranje konekcije\nOdaberite komandu: ",end="")               
            try:
                komanda = int(input())
                poruka = ""
                if(komanda == 1):
                    poruka = ""
                elif(komanda == 2):
                    poruka = "On-0"
                elif(komanda == 3):
                    poruka = "Off-0"
                elif(komanda == 4):
                    poruka = "Exit-0"
                else:
                    print("Zadata komanda ne postoji!")
                   
            except ValueError:
                print("Morate uneti broj")
            except:
                print("Greska! Poruka nije uspesno poslata!")

    

