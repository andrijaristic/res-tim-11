from unittest import mock
from unittest.mock import Mock
import unittest
import socket
from worker.worker import Worker

class TestWorker(unittest.TestCase):
    def test_check_data(self):
        worker = Worker()
        self.assertRaises(TypeError,worker.check_data,"sadsad".encode())
        data = worker.check_data(("10-10-10;10-10-10;10-10-10;10-10-10;10-10-10;10-10-10;10-10-10;10-10-10;10-10-10;10-10-10;".encode()))
        self.assertTrue(data,'Greska')
    def test_receive_data(self):
        worker = Worker()
        connection = Mock()
        connection.recv.return_value = "cao".encode()
        self.assertAlmostEqual(worker.receive_data(connection),"cao".encode())
        connection.recv.assert_called_once()
        connection.recv.assert_called_with(1024)
        connection.recv.return_value = "poruka".encode()
        self.assertAlmostEqual(worker.receive_data(connection),"poruka".encode())
    def test_send(self):
        worker = Worker()
        adresa = ('localhost',25000)
        connection = Mock()
        data = 'poruka'
        self.assertAlmostEqual(worker.send(data,connection),True)
        connection.sendall.assert_called_once()
    def test_receive_reply(self):
        worker = Worker()
        connection = Mock()
        connection.recv.return_value = "poruka".encode()
        self.assertAlmostEqual(worker.receive_reply(connection),("poruka".encode()))
        connection.recv.assert_called_once()
        connection.recv.assert_called_with(1024)
        

