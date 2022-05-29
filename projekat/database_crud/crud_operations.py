
monthsName = {
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

monthsNumber = {
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

def input_params():
    ime = input("Ime: ")
    prz = input("Prezime: ")
    ulica = input("Ulica: ")
    ubroj = input("Broj ulice: ")
    pbroj = input("Postanski kod: ")
    grad = input("Grad: ")

    return ime, prz, ulica, ubroj, pbroj, grad

def update_brojilo_info(conn_str):
    cursor = conn_str.cursor()
    count = 0

    id = input("Id: ")
    cursor.execute(f"SELECT * FROM Informacije WHERE id = {id}")
    # Provera da li postoji id.
    for el in cursor:
        count += 1
    
    if (count > 0):
        ime, prz, ulica, ubroj, pbroj, grad = input_params()

        # Drugacije Update javlja sintaksu gresku.
        update_query = """\
        UPDATE Informacije
        SET
            Ime = ?, Prz = ?, Ulica = ?, Ubroj = ?, Pbroj = ?, Grad = ?    
        WHERE 
            Id = ?
        """

        cursor.execute(update_query, (ime, prz, ulica, ubroj, pbroj, grad, id))
        conn_str.commit()
        print(f"Uspesno azurirano brojilo [{id}]")
    else:
        print(f"Neuspesno azuriranje! ID [{id}] ne postoji.")

def delete_brojilo_info(conn_str):
    cursor = conn_str.cursor()
    count = 0

    id = input("Id: ")
    cursor.execute(f"SELECT * FROM Informacije WHERE id = {id}")
    # Provera da li postoji id.
    for el in cursor:
        count += 1

    if (count > 0):
        cursor.execute(f"DELETE FROM Informacije WHERE id = {id}")
        conn_str.commit()
        print(f"Uspesno obrisano brojilo [{id}].")
    else:
        print(f"Neuspesno brisanje! ID [{id}] ne postoji.")

# Novo.
def create_brojilo_info(conn_str):
    cursor = conn_str.cursor()
    count = 0

    id = input("Id: ")

    cursor.execute("SELECT * FROM Informacije")
    for el in cursor:
        count += 1

    if (count > 0):
        ime, prz, ulica, ubroj, pbroj, grad = input_params()
        input_part = f"{id}, '{ime}', {prz}', '{ulica}', {ubroj}, {pbroj}, '{grad}'"
        cursor.execute(f"INPUT INTO Informacije VALUES ({input_part})")
        conn_str.commit()
        print(f"Uspesno dodavanje informacije o brojilu [{id}]")
    else:
        print(f"Neuspelo dodavanje! ID [{id}] vec postoji.")

# Novo.
# cursor.execute(f"SELECT * FROM Informacije WHERE id = {id} AND Month(datum) = {months[mesec]}")
def create_brojilo_potrosnja(conn_str, id, potrosnja, datum):
    cursor = conn_str.cursor()
    count = 0

    dan = datum.split('.')[0]
    mesec = datum.split('.')[1]
    godina = datum.split('.')[2]

    cursor.execute(f"SELECT * FROM Potrosnja WHERE Id = {id} AND Datum = '{godina}-{mesec}-{dan}'") 
    for el in cursor:
        count += 1
#   INSERT INTO Potrosnja VALUES (2, 230.50, (convert(date, '23-February-12', 5)))
    if (count == 0):
        #print("Insert radimo")
        #cursor.execute(f"INSERT INTO Potrosnja VALUES ({id}, {potrosnja}, (convert(date, '{dan}-{mesec}-{godina}', 5)))")
        try:
            cursor.execute(f"INSERT INTO Potrosnja VALUES ({id}, {potrosnja}, '{godina}-{mesec}-{dan}')")
            conn_str.commit()
        except:
            print("FK-Exception")

# Value = Prosledjena vrednost (Posle :)
# Brojilo:IdBrojila || Grad:NazivGrada

# Potrosnja po mesecima za konkretno brojilo.
def read_brojilo_potrosnja_id(conn_str, value):
    cursor = conn_str.cursor()
    cursor.execute(f"SELECT Ptr, Month(Datum) FROM Potrosnja WHERE id = {value} Order by Month(Datum)")
    response = ""
    
    for ptr, mesec in cursor:
        response += f"{ptr}-{monthsNumber[mesec]};"

    response = response[:-1]
    return response

# Potrosnja po mesecima za odredjen grad.
def read_brojilo_potrosnja_grad(conn_str, value):
    cursor = conn_str.cursor()
    cursor.execute(f"SELECT P.Id, Ptr, Month(Datum) FROM Potrosnja P, Informacije I WHERE P.Id = I.Id AND I.Grad = '{value}' ORDER BY Month(Datum)")
    response = ""
    
    for id, ptr, mesec in cursor:
        response += f"{id}-{ptr}-{monthsNumber[mesec]};"

    response = response[:-1]
    return response;