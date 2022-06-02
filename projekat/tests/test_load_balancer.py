from ast import Load
import sys
sys.path.append('./')
import unittest
from load_balancer.load_balancer import LoadBalancer
import socket

class TestLoadBalancer(unittest.TestCase):
    
    def test_create_socket(self):
        load_balancer = LoadBalancer()
        self.assertRaises(TypeError,load_balancer.create_socket,"asdf")
        self.assertRaises(TypeError,load_balancer.create_socket,5)
        self.assertRaises(TypeError,load_balancer.create_socket,True)

    def test_start_listening_clients(self):
        load_balancer = LoadBalancer()
        self.assertRaises(TypeError,load_balancer.start_listening_clients,True)
        self.assertRaises(TypeError,load_balancer.start_listening_clients,3)

    def test_start_listening_workers(self):
        load_balancer = LoadBalancer()
        self.assertRaises(TypeError,load_balancer.start_listening_workers,True)
        self.assertRaises(TypeError,load_balancer.start_listening_workers,0)

    def test_handle_client(self):
        load_balancer = LoadBalancer()
        self.assertRaises(TypeError,load_balancer.handle_client,"cao")
        self.assertRaises(TypeError,load_balancer.handle_client,5)
        self.assertRaises(TypeError,load_balancer.handle_client,False)

    def test_receive_data(self):
        load_balancer = LoadBalancer()
        adresa = ('localhost',40000)
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(adresa)
        sock.listen(1)
        sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock2.connect(adresa)
        connection, client_address = sock.accept()
        sock2.sendall("cao".encode())
        self.assertAlmostEqual(load_balancer.receive_data(connection),"cao".encode())
        sock2.sendall("poruka".encode())
        self.assertAlmostEqual(load_balancer.receive_data(connection),"poruka".encode())
        sock2.sendall("asdf".encode())
        self.assertNotEqual(load_balancer.receive_data(connection),"f".encode())

    def test_get_message_from_data(self):
        load_balancer = LoadBalancer()
        self.assertAlmostEqual(load_balancer.get_message_from_data("cao".encode()),"cao")
        self.assertAlmostEqual(load_balancer.get_message_from_data("pozdrav".encode()),"pozdrav")
        self.assertAlmostEqual(load_balancer.get_message_from_data("".encode()),"")

    def test_get_command_from_message(self):
        load_balancer = LoadBalancer()
        self.assertAlmostEqual(load_balancer.get_command_from_message("Send-1"),"Send")
        self.assertAlmostEqual(load_balancer.get_command_from_message("Exit"),"Exit")
        self.assertAlmostEqual(load_balancer.get_command_from_message("On-0"),"On")
        self.assertRaises(TypeError,load_balancer.get_command_from_message,1)
        self.assertRaises(TypeError,load_balancer.get_command_from_message,True)

    def test_get_parameters_from_message(self):
        load_balancer = LoadBalancer()
        self.assertAlmostEqual(load_balancer.get_parameters_from_message("Test-1-123-Cao"),"1-123-Cao")
        self.assertAlmostEqual(load_balancer.get_parameters_from_message("1-1-1-1"),"1-1-1")
        self.assertRaises(IndexError,load_balancer.get_parameters_from_message,"1-1")
        self.assertRaises(TypeError,load_balancer.get_parameters_from_message,1)
        self.assertRaises(TypeError,load_balancer.get_parameters_from_message,False)

    def test_generate_send_reply(self):
        load_balancer = LoadBalancer()
        self.assertAlmostEqual(load_balancer.generate_send_reply(True,[1,2,3]),"Data stored 3")
        self.assertAlmostEqual(load_balancer.generate_send_reply(True,[2]),"Data stored 1")
        self.assertAlmostEqual(load_balancer.generate_send_reply(True,[1,5,2,4,1,1,5,2,3,1]),"Data stored 10")
        self.assertAlmostEqual(load_balancer.generate_send_reply(False,[1,2,3]),"Local buffer is full")
        self.assertRaises(TypeError,load_balancer.generate_send_reply,1,[1,2,3])
        self.assertRaises(TypeError,load_balancer.generate_send_reply,"Asdf",[1,2,3])

    def test_generate_on_reply(self):
        load_balancer = LoadBalancer()
        self.assertAlmostEqual(load_balancer.generate_on_reply(True),"New worker started working")
        self.assertAlmostEqual(load_balancer.generate_on_reply(False),"Failed to start a new worker")
        self.assertRaises(TypeError,load_balancer.generate_on_reply,-1);
        self.assertRaises(TypeError,load_balancer.generate_on_reply,"asdf");

    def test_generate_off_reply(self):
        load_balancer = LoadBalancer()
        self.assertAlmostEqual(load_balancer.generate_off_reply(True,True),"Worker turned off")
        self.assertAlmostEqual(load_balancer.generate_off_reply(True,False),"Failed to turn off a worker")
        self.assertAlmostEqual(load_balancer.generate_off_reply(False,True),"Cannot turn off workers while they are working")
        self.assertAlmostEqual(load_balancer.generate_off_reply(False,False),"Cannot turn off workers while they are working")
        self.assertRaises(TypeError,load_balancer.generate_off_reply,1,True)
        self.assertRaises(TypeError,load_balancer.generate_off_reply,1,"True")
        self.assertRaises(TypeError,load_balancer.generate_off_reply,True,"asdf")
        self.assertRaises(TypeError,load_balancer.generate_off_reply,True,1)

    def test_prepare_reply(self):
        load_balancer = LoadBalancer()
        self.assertAlmostEqual(load_balancer.prepare_reply("poruka"),"poruka".encode())
        self.assertAlmostEqual(load_balancer.prepare_reply("cao"),"cao".encode())
        self.assertAlmostEqual(load_balancer.prepare_reply(""),"".encode())
        self.assertRaises(TypeError,load_balancer.prepare_reply,11);
        self.assertRaises(TypeError,load_balancer.prepare_reply,True);

    def test_store_data(self):
        load_balancer = LoadBalancer()
        self.assertAlmostEqual(load_balancer.store_data([1,2,3,1,2,3,1,2,3,1,2,3],"asdf"),False)
        self.assertAlmostEqual(load_balancer.store_data([1,2,3,1,1,2,3],"asdf"),True)
        self.assertAlmostEqual(load_balancer.store_data([],"asdf"),True)
        self.assertRaises(TypeError,load_balancer.store_data,[1,2],1)
        self.assertRaises(TypeError,load_balancer.store_data,[],True)

    def test_send_reply_to_client(self):
        load_balancer = LoadBalancer()
        adresa = ('localhost',40000)
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(adresa)
        sock.listen(1)
        sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock2.connect(adresa)
        connection, client_address = sock.accept()
        self.assertAlmostEqual(load_balancer.send_reply_to_client(sock2,adresa,"asdf".encode()),True)
        self.assertAlmostEqual(load_balancer.send_reply_to_client(connection,client_address,"asdf".encode()),True)
        self.assertAlmostEqual(load_balancer.send_reply_to_client(sock2,"adresa","asdf".encode()),False)
        self.assertAlmostEqual(load_balancer.send_reply_to_client(sock,client_address,"asdf".encode()),False)
        self.assertRaises(TypeError,load_balancer.send_reply_to_client,1,1,"asdf")
        self.assertRaises(TypeError,load_balancer.send_reply_to_client,1,1,False)

    def test_close_client_connection(self):
        load_balancer = LoadBalancer()
        adresa = ('localhost',40000)
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(adresa)
        sock.listen(1)
        sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock2.connect(adresa)
        connection, client_address = sock.accept()
        client_connections = [connection]
        self.assertAlmostEqual(load_balancer.close_client_connection(connection,client_connections),True)
        self.assertAlmostEqual(load_balancer.close_client_connection(sock,client_connections),False)
        self.assertAlmostEqual(load_balancer.close_client_connection(sock2,[sock2]),True)
        self.assertAlmostEqual(load_balancer.close_client_connection(connection,[]),False)

    def test_start_worker(self):
        load_balancer = LoadBalancer()
        self.assertAlmostEqual(load_balancer.start_worker("123"),True)
        self.assertRaises(TypeError,load_balancer.start_worker,1)
        self.assertRaises(TypeError,load_balancer.start_worker,False)

    def test_find_available_worker(self):
        load_balancer = LoadBalancer()
        self.assertAlmostEqual(load_balancer.find_available_worker([True,False,True]),0)
        self.assertAlmostEqual(load_balancer.find_available_worker([False,False,False]),-1)
        self.assertAlmostEqual(load_balancer.find_available_worker([False,False,True]),2)
        self.assertAlmostEqual(load_balancer.find_available_worker([]),-1)

    def test_turn_off_worker(self):
        load_balancer = LoadBalancer()
        adresa = ('localhost',40000)
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(adresa)
        sock.listen(1)
        sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock2.connect(adresa)
        connection, client_address = sock.accept()
        client_connections = [connection]
        self.assertAlmostEqual(load_balancer.turn_off_worker(0,client_connections,[True]),True)
        self.assertAlmostEqual(load_balancer.turn_off_worker(0,client_connections,[]),False)
        self.assertAlmostEqual(load_balancer.turn_off_worker(2,client_connections,[True]),False)
        self.assertAlmostEqual(load_balancer.turn_off_worker(0,[],[True]),False)
        self.assertRaises(TypeError,load_balancer,"asdf",client_connections,[True])
        self.assertRaises(TypeError,load_balancer,True,client_connections,[True])

    def test_check_data_for_sending(self):
        load_balancer = LoadBalancer()
        self.assertRaises(TypeError,load_balancer.check_data_for_sending,1)
        self.assertRaises(IndexError,load_balancer.check_data_for_sending,[1,1,1,1,1,1,1,1,1,1],[],[True])

    def test_send_message_to_worker(self):
        load_balancer = LoadBalancer()
        adresa = ('localhost',40000)
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(adresa)
        sock.listen(1)
        sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock2.connect(adresa)
        connection, client_address = sock.accept()
        self.assertAlmostEqual(load_balancer.send_message_to_worker(0,connection,[True],"asdf".encode()),True)
        self.assertAlmostEqual(load_balancer.send_message_to_worker(1,connection,[True],"asdf".encode()),False)
        self.assertAlmostEqual(load_balancer.send_message_to_worker(0,sock,[True],"asdf".encode()),False)
        self.assertRaises(TypeError,load_balancer.send_message_to_worker,1,connection,[True],"asdf")
        self.assertRaises(TypeError,load_balancer.send_message_to_worker,1,connection,[True],False)
        self.assertRaises(TypeError,load_balancer.send_message_to_worker,1,connection,[True],1)

    def test_convert_data_to_message(self):
        load_balancer = LoadBalancer()
        self.assertAlmostEqual(load_balancer.convert_data_to_message(["cao","pozdrav"]),"cao;pozdrav")
        self.assertAlmostEqual(load_balancer.convert_data_to_message(["1","2","3","4"]),"1;2;3;4")
        self.assertAlmostEqual(load_balancer.convert_data_to_message(["cao"]),"cao")

    def test_get_worker(self):
        load_balancer = LoadBalancer()
        self.assertAlmostEqual(load_balancer.get_worker(1,[True,False]),False)
        self.assertAlmostEqual(load_balancer.get_worker(2,[3,2,1]),1)
        self.assertAlmostEqual(load_balancer.get_worker(0,["asdf"]),"asdf")
        self.assertRaises(TypeError,load_balancer.get_worker,True,[])
        self.assertRaises(TypeError,load_balancer.get_worker,"asfd",[])
        self.assertRaises(IndexError,load_balancer.get_worker,-1,[1])
        self.assertRaises(IndexError,load_balancer.get_worker,5,[True])
        self.assertRaises(IndexError,load_balancer.get_worker,0,[])

    def test_start_worker_app(self):
        load_balancer = LoadBalancer()
        self.assertRaises(TypeError,load_balancer.start_worker_app,1)
        self.assertRaises(TypeError,load_balancer.start_worker_app,True)

    def test_check_worker_availabilty(self):
        load_balancer = LoadBalancer()
        self.assertAlmostEqual(load_balancer.check_worker_availabilty([True,False]),False)
        self.assertAlmostEqual(load_balancer.check_worker_availabilty([True]),True)
        self.assertAlmostEqual(load_balancer.check_worker_availabilty([True,True,True,False]),False)
        self.assertAlmostEqual(load_balancer.check_worker_availabilty([False,False]),False)
        self.assertAlmostEqual(load_balancer.check_worker_availabilty([True,True,True,True]),True)
        self.assertAlmostEqual(load_balancer.check_worker_availabilty([]),True)

    def test_close_all_connections(self):
        load_balancer = LoadBalancer()
        self.assertRaises(TypeError,load_balancer.close_all_connections,1)
        self.assertRaises(TypeError,load_balancer.close_all_connections,[],0)