import unittest
from unittest.mock import patch
from database_crud.connections import connect_to, add_database

class TestConnections(unittest.TestCase):

    @patch('os.path.dirname')
    def test_add_database(self, dirname):
        dirname.return_value = "projekat"
        self.assertEqual(add_database(), "DRIVER=ODBC Driver 17 for SQL Server;SERVER=.\SQLEXPRESS;Trusted_Connection=yes;DATABASE=Brojila;AttachDbFileName=projekat\Brojila.mdf;")

    def test_connect_to(self):
        self.assertEqual(connect_to(), "DRIVER=ODBC Driver 17 for SQL Server;SERVER=.\SQLEXPRESS;Trusted_Connection=yes;DATABASE=Brojila;")