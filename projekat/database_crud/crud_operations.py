class CrudOperations():
    def __init__(self):
        self.months_name = {
            "January" : 1,
            "February" : 2,
            "March" : 3,
            "April" : 4, 
            "May" : 5,
            "June" : 6, 
            "July" : 7, 
            "August" : 8,
            "September" : 9, 
            "October" : 10, 
            "November" : 11,
            "December" : 12    
        }

        self.months_number = {
            1 : "January",
            2 : "February",
            3 : "March",
            4 : "April", 
            5 : "May",
            6 : "June", 
            7 : "July", 
            8 : "August",
            9 : "September", 
            10 : "October", 
            11 : "November",
            12 : "December"       
        }

    def check_if_exists(self, cnxn, id):
        cur = cnxn.cursor()
        cur.execute(f"SELECT * FROM Informacije WHERE Id = {id}")
        num = cur.fetchone()
        return num

    # UPDATE
    def update_brojilo_info(self, cnxn, id, ime, prz, ulica, ubroj, pbroj, grad):
        update_query = """\
        UPDATE Informacije
        SET
            Ime = ?, Prz = ?, Ulica = ?, Ubroj = ?, Pbroj = ?, Grad = ?    
        WHERE 
            Id = ?
        """

        #cur = cnxn.cursor()
        num = self.check_if_exists(cnxn, id)
        cur = cnxn.cursor()
        if num != None:
            cur.execute(update_query, (ime, prz, ulica, ubroj, pbroj, grad, id))
            cnxn.commit()
            print(f"Uspesno azurirano brojilo [{id}]")
            
            return True
        else:
            print(f"Neuspesno azuriranje! ID [{id}] ne postoji.")  
            return False  

    # DELETE
    def delete_brojilo_info(self, cnxn, id):
        cur = cnxn.cursor()
        num = self.check_if_exists(cnxn, id)
        
        if num != None:
            try:
                cur.execute(f"DELETE FROM Informacije WHERE Id = {id}")
                cnxn.commit()
                print(f"Uspesno obrisano brojilo [{id}].")
                return True
            except Exception:
                print("- - - - - - - - - - - - - - - - - - - - - - - -"+
                "\nNemoguce brisanje brojila. Vec postoje merenja.\n"+
                "- - - - - - - - - - - - - - - - - - - - - - - -")
                return False
        else:
            print(f"Neuspesno brisanje! ID [{id}] ne postoji.")   
            return False    

    # CREATE
    def create_brojilo_info(self, cnxn, id, ime, prz, ulica, ubroj, pbroj, grad):
        cur = cnxn.cursor()
        num = self.check_if_exists(cnxn, id)

        if num == None:
            insert_part = f"{id}, '{ime}', '{prz}', '{ulica}', {ubroj}, {pbroj}, '{grad}'"
            cur.execute(f"INSERT INTO Informacije VALUES ({insert_part})")
            cnxn.commit()
            print(f"Uspesno dodavanje informacije o brojilu [{id}]")
            return True
        else:
            print(f"Neuspelo dodavanje! ID [{id}] vec postoji.") 
            return False      


    def create_brojilo_potrosnja(self, cnxn, id, potrosnja, datum_vreme):
        cur = cnxn.cursor()

        datum = datum_vreme.split('?')[0]
        vreme = datum_vreme.split('?')[1]
        
        dan = datum.split('.')[0]
        mesec = datum.split('.')[1]
        godina = datum.split('.')[2]

        sat = vreme.split(':')[0]
        minut = vreme.split(':')[1]
        sekunda = vreme.split(':')[2]

        cur.execute(f"SELECT * FROM Potrosnja WHERE Id = {id} AND Datum = '{godina}-{mesec}-{dan} {sat}:{minut}:{sekunda}'")
        num = cur.fetchone()
        if num == None:
            try:
                cur.execute(f"INSERT INTO Potrosnja VALUES ({id}, {potrosnja}, '{godina}-{mesec}-{dan} {sat}:{minut}:{sekunda}')")
                cnxn.commit()
                return True
            except Exception as ex:
                return False
        return False

    # READ
    def read_brojilo_potrosnja_id(self, cnxn, value):
        cur = cnxn.cursor()
        try:
            cur.execute(f"SELECT Ptr, Month(Datum) FROM Potrosnja P WHERE Id = {value} ORDER BY Month(Datum)")
        except Exception:
            return "Merenja ne postoje"

        items = cur.fetchall()
        response = ""

        if not items:
            return "Merenja ne postoje"

        ptr_by_month = {}
        for ptr, mesec in items:
            if mesec in ptr_by_month:
                ptr_by_month[mesec] += ptr
            else:
                ptr_by_month[mesec] = ptr

        for i, el in enumerate(ptr_by_month):
            response += f"{ptr_by_month[el]}-{self.months_number[el]};"

        response = response[:-1]     
        return response

    def read_brojilo_potrosnja_grad(self, cnxn, value):
        cur = cnxn.cursor()
        try:
            cur.execute(f"SELECT Ptr, Month(Datum) FROM Potrosnja P, Informacije I WHERE P.Id = I.Id AND I.Grad = '{value}' ORDER BY Month(Datum)")
        except Exception:
            return "Merenja ne postoje"

        items = cur.fetchall()
        response = ""

        if not items:
            return "Merenja ne postoje"

        ptr_by_month = {}
        for ptr, mesec in items:
            if mesec in ptr_by_month:
                ptr_by_month[mesec] += ptr
            else:
                ptr_by_month[mesec] = ptr


        for i, el in enumerate(ptr_by_month):
            response += f"{ptr_by_month[el]}-{self.months_number[el]};"

        response = response[:-1]
        return response