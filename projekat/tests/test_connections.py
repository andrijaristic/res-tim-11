import unittest
from unittest.mock import patch
from database_crud.connections import connect_to, add_database

class TestConnections(unittest.TestCase):

    @patch('os.path.dirname')
    @patch('os.path.join')
    def test_add_database(self, dirname, join):
        dirname.return_value = "projekat"
        join.return_value = "Brojila.mdf"
        self.assertEqual(add_database(), "DRIVER=ODBC Driver 17 for SQL Server;SERVER=.\SQLEXPRESS;Trusted_Connection=yes;DATABASE=Brojila;AttachDbFileName=projekat;")

    def test_connect_to(self):
        self.assertEqual(connect_to(), "DRIVER=ODBC Driver 17 for SQL Server;SERVER=.\SQLEXPRESS;Trusted_Connection=yes;DATABASE=Brojila;")