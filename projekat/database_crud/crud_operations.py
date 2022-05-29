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