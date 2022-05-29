from threading import Thread
from connections import *
from classes import Database
import pyodbc

def terminal_input(cnxn):
    while True:
        temp = input()
        if (temp == "x"):
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