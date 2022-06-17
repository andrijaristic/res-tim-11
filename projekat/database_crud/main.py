from threading import Thread
from connections import connect_to, add_database
from database_crud import DatabaseCrud
from database_management import TerminalOperations
import pyodbc

if __name__ == '__main__':
    try:
        connection_str = add_database()
        cnxn = pyodbc.connect(connection_str)
    except:
        connection_str = connect_to()
        cnxn = pyodbc.connect(connection_str)

    try:
        worker_listening_address = ('localhost', 22000)
        analytics_listening_address = ('localhost', 23000)

        database = DatabaseCrud()
        worker_socket = database.create_socket(worker_listening_address)
        analytics_socket = database.create_socket(analytics_listening_address)

        worker_thread = Thread(target=database.start_listening_worker, args=(worker_socket, cnxn))
        worker_thread.daemon = True
        worker_thread.start()

        analytics_thread = Thread(target=database.start_listening_analytics, args=(analytics_socket, cnxn))
        analytics_thread.daemon = True
        analytics_thread.start()

        terminal_operations = TerminalOperations()
        terminal_thread = Thread(target=terminal_operations.terminal_input, args=(cnxn,))
        terminal_thread.start()
    except:
        print("Exception")
        exit()