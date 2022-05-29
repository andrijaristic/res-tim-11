from threading import Thread
from connections import *
from classes import Database
from crud_operations import *
import pyodbc

def meni():
    print("\n=======================")
    print("1. Create row")
    print("2. Delete row")
    print("3. Update row") 
    print("X. Exit")
    print("=======================")

def terminal_input(cnxn):
    while True:
        meni()
        temp = input("Option: ")
        if (temp == "1"):
            create_brojilo_info(cnxn)
        elif (temp == "2"):
            delete_brojilo_info(cnxn)
        elif (temp == "3"):
            update_brojilo_info(cnxn)
        elif (temp.lower() == "x"):
            exit()

def main():
    try:
        connection_str = add_database()
        cnxn = pyodbc.connect(connection_str)
    except:
        connection_str = connect_to()
        cnxn = pyodbc.connect(connection_str)

    worker_listening_address = ('localhost', 22000)
    analytics_listening_address = ('localhost', 23000)

    database = Database(worker_listening_address, analytics_listening_address, cnxn)

    worker_thread = Thread(target=database.start_listening_worker)
    worker_thread.daemon = True
    worker_thread.start()

    analytics_thread = Thread(target=database.start_listening_analytics)
    analytics_thread.daemon = True
    analytics_thread.start()

    terminal_thread = Thread(target=terminal_input, args=(cnxn,))
    terminal_thread.start()

if __name__ == '__main__':
    main()