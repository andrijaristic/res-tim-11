import os

def add_database():
    db_path = os.path.abspath("Brojila.mdf")
    connection_str = (
        r'DRIVER=ODBC Driver 17 for SQL Server;'
        r'SERVER=.\SQLEXPRESS;'
        r'Trusted_Connection=yes;'
        r'DATABASE=Brojila;'
        f'AttachDbFileName={db_path};'
    )
    return connection_str

def connect_to():
    connection_str = (
        r'DRIVER=ODBC Driver 17 for SQL Server;'
        r'SERVER=.\SQLEXPRESS;'
        r'Trusted_Connection=yes;'
        r'DATABASE=Brojila;'
    )
    return connection_str

