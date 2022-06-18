from crud_operations import CrudOperations

class TerminalOperations: 
    def __init__(self): # pragma: no cover 
        self.crud_operations = CrudOperations()

    def meni(self): 
        print("\n=======================")
        print("1. Create row")
        print("2. Delete row")
        print("3. Update row") 
        print("X. Exit")
        print("=======================")

    def input_params(self):
        ime = input("Ime: ")
        prz = input("Prezime: ")
        ulica = input("Ulica: ")
        ubroj = input("Broj ulice: ")
        pbroj = input("Postanski kod: ")
        grad = input("Grad: ")

        return ime, prz, ulica, ubroj, pbroj, grad

    def input_option(self):
        option = input("Option: ")
        return option

    def input_id(self):
        id = input("Id: ")
        return id

    def terminal_input(self, cnxn): # pragma: no cover 
        while True:
            self.meni()
            temp = self.input_option()
            if (temp == "1"):
                id = self.input_id()
                if (self.crud_operations.check_if_exists(cnxn, id) != None):
                    print(f"Vec postoji brojilo sa ID:[{id}]")
                else:
                    ime, prz, ulica, ubroj, pbroj, grad = self.input_params()
                    self.crud_operations.create_brojilo_info(cnxn, id, ime, prz, ulica, ubroj, pbroj, grad)
            elif (temp == "2"):
                id = self.input_id()
                self.crud_operations.delete_brojilo_info(cnxn, id)
            elif (temp == "3"):
                id = self.input_id()
                if (self.crud_operations.check_if_exists(cnxn, id) != None):
                    ime, prz, ulica, ubroj, pbroj, grad = self.input_params()
                    self.crud_operations.update_brojilo_info(cnxn, id, ime, prz, ulica, ubroj, pbroj, grad)
                else:
                    print(f"Ne postoji brojilo sa ID:[{id}]")
            elif (temp.lower() == "x"):
                exit()