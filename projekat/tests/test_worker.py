from unittest import mock
from unittest.mock import Mock
import unittest
import socket
from worker.classes import Worker

class TestWorker(unittest.TestCase):
    def test_checkdata(self):
        worker = Worker()
        self.assertRaises(TypeError,worker.checkdata,"sadsad".encode())
        self.assertTrue(worker.checkdata,"10-10-10;10-10-10;10-10-10;10-10-10;10-10-10;10-10-10;10-10-10;10-10-10;10-10-10;10-10-10;".encode())
    def test_receivedata(self):
        worker = Worker()
        connection = Mock()
        connection.recv.return_value = "cao".encode()
        self.assertAlmostEqual(worker.receivedata(connection),"cao".encode())
        connection.recv.assert_called_once()
        connection.recv.assert_called_with(1024)
        connection.recv.return_value = "poruka".encode()
        self.assertAlmostEqual(worker.receivedata(connection),"poruka".encode())
    def test_send(self):
        worker = Worker()
        adresa = ('localhost',25000)
        connection = Mock()
        data = 'poruka'
        self.assertAlmostEqual(worker.send(data,connection),True)
        connection.sendall.assert_called_once()
    def test_receivereply(self):
        worker = Worker()
        connection = Mock()
        connection.recv.return_value = "poruka".encode()
        self.assertAlmostEqual(worker.receivereply(connection),("poruka".encode()))
        connection.recv.assert_called_once()
        connection.recv.assert_called_with(1024)
        

