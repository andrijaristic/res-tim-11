from ast import Load
import sys
sys.path.append('./')
import unittest
from unittest import mock
from unittest.mock import Mock, MagicMock, patch
from database_crud.crud_operations import CrudOperations


class TestCrudOperations(unittest.TestCase):
    
    def set_dbc(self, fetchone):
        dbc = mock.MagicMock(spec=['cursor'],
                         **{'cursor.return_value': mock.MagicMock(
                             spec=['execute', 'fetchone',],
                             **{'fetchone.return_value': fetchone})})

        dbc.close = mock.MagicMock
        dbc.commit = mock.MagicMock

        return dbc

    def test_check_if_exists(self):
        dbc = self.set_dbc(None)
        crud_operations = CrudOperations()

        self.assertEqual(crud_operations.check_if_exists(dbc, 1), None)
        dbc.cursor().execute.assert_called_once()
        dbc.cursor().execute.assert_called_with("SELECT * FROM Informacije WHERE Id = 1")

        dbc.cursor.return_value.fetchone.return_value = 1
        self.assertEqual(crud_operations.check_if_exists(dbc, 1), 1)
        dbc.cursor().execute.assert_called_with("SELECT * FROM Informacije WHERE Id = 1")

    def test_delete_brojilo_info(self):
        dbc = self.set_dbc(1)   
        crud_operations = CrudOperations()

        self.assertEqual(crud_operations.delete_brojilo_info(dbc, 10), True)
        dbc.cursor().execute.assert_called_with('DELETE FROM Informacije WHERE Id = 10')

        dbc.cursor.return_value.fetchone.return_value = 1  
        self.assertEqual(crud_operations.delete_brojilo_info(dbc, 1), True)
        dbc.cursor().execute.assert_called_with('DELETE FROM Informacije WHERE Id = 1')

        dbc.cursor.return_value.fetchone.return_value = None 
        self.assertEqual(crud_operations.delete_brojilo_info(dbc, 22), False)
        dbc.cursor().execute.assert_called_with('SELECT * FROM Informacije WHERE Id = 22')

        dbc.cursor.return_value.fetchone.return_value = 1
        dbc.cursor().execute.return_value = Exception 
        self.assertRaises(Exception, crud_operations.delete_brojilo_info(dbc, 10))
        dbc.cursor().execute.assert_called_with('DELETE FROM Informacije WHERE Id = 10')

    def test_update_brojilo_info(self):
        dbc = self.set_dbc(1)   
        crud_operations = CrudOperations()

        self.assertEqual(crud_operations.update_brojilo_info(dbc,  1, 'A', 'A', 'A', 10, 100, 'A'), True)   

        dbc.cursor.return_value.fetchone.return_value = None   
        self.assertEqual(crud_operations.update_brojilo_info(dbc,  1, 'A', 'A', 'A', 10, 100, 'A'), False)  

    def test_create_brojilo_info(self):
        dbc = self.set_dbc(None)
        crud_operations = CrudOperations()

        self.assertEqual(crud_operations.create_brojilo_info(dbc, 1, 'A', 'A', 'A', 10, 100, 'A'), True)
        dbc.cursor().execute.assert_called_with("INSERT INTO Informacije VALUES (1, 'A', 'A', 'A', 10, 100, 'A')")

        dbc.cursor.return_value.fetchone.return_value = 1
        self.assertEqual(crud_operations.create_brojilo_info(dbc, 1, 'A', 'A', 'A', 10, 100, 'A'), False)
        dbc.cursor().execute.assert_called_with('SELECT * FROM Informacije WHERE Id = 1')
    
    def test_create_brojilo_potrosnja(self):
        dbc = self.set_dbc(None)
        crud_operations = CrudOperations()

        self.assertEqual(crud_operations.create_brojilo_potrosnja(dbc, 1, 220, "01.01.2000?11:10:59"), True)
        dbc.cursor().execute.assert_called_with("INSERT INTO Potrosnja VALUES (1, 220, '2000-01-01 11:10:59')")

        dbc.cursor.return_value.fetchone.return_value = 1
        self.assertEqual(crud_operations.create_brojilo_potrosnja(dbc, 1, 220, "01.01.2000?11:10:59"), False)
        dbc.cursor().execute.assert_called_with("SELECT * FROM Potrosnja WHERE Id = 1 AND Datum = '2000-01-01 11:10:59'")

    def test_read_brojilo_potrosnja_id(self):
        dbc = mock.MagicMock()
        crud_operations = CrudOperations()

        dbc.cursor.return_value.fetchall.return_value = [(220, 1), (420, 5)]
        self.assertEqual(crud_operations.read_brojilo_potrosnja_id(dbc, 1), "220-January;420-May")

        dbc.cursor.return_value.fetchall.return_value = []
        self.assertEqual(crud_operations.read_brojilo_potrosnja_id(dbc, 1), "Merenja ne postoje")

    def test_read_brojilo_potrosnja_grad(self):
        dbc = mock.MagicMock()
        crud_operations = CrudOperations()

        dbc.cursor.return_value.fetchall.return_value = [(1, 220, 1), (2, 420, 5)]
        self.assertEqual(crud_operations.read_brojilo_potrosnja_grad(dbc, "Novi Sad"), "1-220-January;2-420-May")

        dbc.cursor.return_value.fetchall.return_value = []
        self.assertEqual(crud_operations.read_brojilo_potrosnja_grad(dbc, "Trstenik"), "Merenja ne postoje")
