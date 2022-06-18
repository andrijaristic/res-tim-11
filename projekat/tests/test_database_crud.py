from ast import Load
from audioop import add
import sys
sys.path.append('./')
import socket
import unittest
from unittest import mock
from unittest.mock import Mock, patch
from database_crud.database_crud import DatabaseCrud

class TestDatabaseCrud(unittest.TestCase):

    def test_input_values_create_socket(self):
        database_crud = DatabaseCrud()
        self.assertRaises(TypeError, database_crud.create_socket, "test")
        self.assertRaises(TypeError, database_crud.create_socket, 5)
        self.assertRaises(TypeError, database_crud.create_socket, True)

    def test_start_listening_worker(self):
        database_crud = DatabaseCrud()
        self.assertRaises(TypeError, database_crud.start_listening_worker, True)
        self.assertRaises(TypeError, database_crud.start_listening_worker, 1)

    def test_start_listening_analytics(self):        
        database_crud = DatabaseCrud()
        self.assertRaises(TypeError, database_crud.start_listening_analytics, True)
        self.assertRaises(TypeError, database_crud.start_listening_analytics, 1)

    def test_handle_worker(self):
        database_crud = DatabaseCrud()
        self.assertRaises(TypeError, database_crud.handle_worker, "test-message-worker")
        self.assertRaises(TypeError, database_crud.handle_worker, 1)    
        self.assertRaises(TypeError, database_crud.handle_worker, False)   

    def test_handle_analytics(self):
        database_crud = DatabaseCrud()
        self.assertRaises(TypeError, database_crud.handle_analytics, "test-message-analytics")
        self.assertRaises(TypeError, database_crud.handle_analytics, 1)    
        self.assertRaises(TypeError, database_crud.handle_analytics, False)  

    def test_receive_data(self):
        database_crud = DatabaseCrud()
        connection = Mock()
        connection.recv.return_value = "test-message".encode()
        self.assertAlmostEqual(database_crud.receive_data(connection), "test-message".encode())

        connection.recv.assert_called_once()
        connection.recv.assert_called_with(1024)

        connection.recv.return_value = "test-message".encode()
        self.assertAlmostEqual(database_crud.receive_data(connection), "test-message".encode())

    def test_get_message_from_data(self):
        database_crud = DatabaseCrud()
        self.assertAlmostEqual(database_crud.get_message_from_data("test-message".encode()), "test-message")
        self.assertAlmostEqual(database_crud.get_message_from_data("test-message".encode()), "test-message")
        self.assertAlmostEqual(database_crud.get_message_from_data("".encode()),"")

    def test_get_params_from_worker_message(self):
        database_crud = DatabaseCrud()
        self.assertAlmostEqual(database_crud.get_params_from_worker_message("1-200-11.01.2000"), ('1', '200', '11.01.2000'))

    def test_input_values_get_params_from_worker_message(self):
        database_crud = DatabaseCrud()
        self.assertRaises(IndexError,database_crud.get_params_from_worker_message, "1-1")
        self.assertRaises(TypeError,database_crud.get_params_from_worker_message, 1)
        self.assertRaises(TypeError,database_crud.get_params_from_worker_message, False)

    def test_get_params_from_analytics_message(self):
        database_crud = DatabaseCrud()
        self.assertAlmostEqual(database_crud.get_params_from_analytics_message("Brojilo:1"), ('Brojilo', '1'))
        self.assertAlmostEqual(database_crud.get_params_from_analytics_message("Grad:Novi Sad"), ('Grad', 'Novi Sad'))

    def test_input_values_get_params_from_analytics_message(self):
        database_crud = DatabaseCrud()
        self.assertRaises(IndexError,database_crud.get_params_from_analytics_message, "1")
        self.assertRaises(TypeError,database_crud.get_params_from_analytics_message, 1)
        self.assertRaises(TypeError,database_crud.get_params_from_analytics_message, False)

    def test_prepare_response(self):
        database_crud = DatabaseCrud()
        self.assertAlmostEqual(database_crud.prepare_response("test-message"), "test-message".encode());
        self.assertAlmostEqual(database_crud.prepare_response("msg"), "msg".encode());     
        self.assertAlmostEqual(database_crud.prepare_response(""), "".encode())  

    def test_input_values_prepare_response(self):
        database_crud = DatabaseCrud()
        self.assertRaises(TypeError,database_crud.prepare_response, 11);
        self.assertRaises(TypeError,database_crud.prepare_response, True);

    def test_send_response(self):
        database_crud = DatabaseCrud()
        connection = Mock()
        address = ('localhost', 30000)
        response = "message".encode()

        self.assertAlmostEqual(database_crud.send_response(connection, response, address), True)
        connection.sendto.assert_called_once()
        connection.sendto.assert_called_with(response, address)

    def test_input_values_send_response(self):
        database_crud = DatabaseCrud()
        self.assertRaises(TypeError, database_crud.send_response, 1, "test", 1)
        self.assertRaises(TypeError, database_crud.send_response, 1, False, 1)
        self.assertRaises(TypeError, database_crud.send_response, 1, 1, 1)

    def test_close_connection(self):
        database_crud = DatabaseCrud()
        connection = Mock()
        
        self.assertAlmostEqual(database_crud.close_connection(connection), True)
        connection.close.assert_called_once()
        connection.close.assert_called_with()