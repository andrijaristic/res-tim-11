from multiprocessing import connection
from multiprocessing.sharedctypes import Value
import sys
sys.path.append('./')
import unittest
from writer.writer import Writer
from unittest.mock import Mock, patch
import datetime
from freezegun import freeze_time

class TestWriter(unittest.TestCase):

    def test_input_values_create_socket(self):
        writer = Writer()
        self.assertRaises(TypeError, writer.create_socket,"ddofjs")
        self.assertRaises(TypeError, writer.create_socket,50)
        self.assertRaises(TypeError, writer.create_socket,True)
    
    @patch("writer.writer.Writer.format_message", return_value="Send-10-5-16.06.2022;14:25:10")
    @patch("writer.writer.Writer.get_input", return_value=10)
    def test_switch_komanda(self, input, input2):
        writer = Writer()
        self.assertAlmostEqual(writer.switch_komanda(2), "On-0")
        self.assertAlmostEqual(writer.switch_komanda(3), "Off-0")
        self.assertAlmostEqual(writer.switch_komanda(4), "Exit-0")
        self.assertAlmostEqual(writer.switch_komanda(1), "Send-10-5-16.06.2022;14:25:10")
        self.assertAlmostEqual(writer.switch_komanda(5), False)

    
    def test_input_values_switch_komanda(self):
        writer = Writer()
        self.assertRaises(TypeError, writer.switch_komanda, "dsfsd")
        self.assertRaises(TypeError, writer.switch_komanda, True)


    def test_input_values_get_input(self):
        writer = Writer()
        self.assertRaises(TypeError, writer.get_input, 50)
        self.assertRaises(TypeError, writer.get_input, False)

    def test_input_values_format_message(self):
        writer = Writer()
        self.assertRaises(TypeError, writer.format_message, "sdsd", True)
        self.assertRaises(TypeError, writer.format_message, False, 10)
        self.assertRaises(TypeError, writer.format_message, 500, "asas")
        self.assertRaises(TypeError, writer.format_message, True, True)

               
    @freeze_time("2019-10-01 20:45:22")
    def test_format_message(self):
        writer = Writer()              
        self.assertEqual(writer.format_message(10, 5), "Send-10-5-01.10.2019?20:45:22")
        
    def test_input_values_send_message(self):
        writer = Writer()
        self.assertRaises(TypeError, writer.send_message,5)
        self.assertRaises(TypeError, writer.send_message,True)

    def test_send_message(self):
        writer = Writer()
        connection = Mock()
        self.assertAlmostEqual(writer.send_message("poruka", connection), True)
       
    def test_close_socket(self):
        writer = Writer()
        connection = Mock()       
        self.assertAlmostEqual(writer.close_socket(connection),True)
        connection.close.assert_called_once()
        connection.close.assert_called_with()
        self.assertAlmostEqual(writer.close_socket("connection"),False)

    def test_receive_data(self):
        writer = Writer()
        connection = Mock()
        connection.recv.return_value = "test".encode()
        self.assertAlmostEqual(writer.receive_data(connection),"test".encode())
        connection.recv.assert_called_once()
        connection.recv.assert_called_with(1024)
        connection.recv.return_value = "poruka1".encode()
        self.assertAlmostEqual(writer.receive_data(connection),"poruka1".encode())
