import filecmp
import os
from unittest import mock
from unittest.mock import Mock
import unittest
from database_analitics.database_analitics import DatabaseAnalytics
class TestDatabasaAnalitics(unittest.TestCase):
    def test_kreiraj_naziv_fajla_grad(self):
        analitics = DatabaseAnalytics()
        nazivfajla = analitics.kreiraj_naziv_fajla_grad('Novi Sad')
        self.assertEqual(nazivfajla,'NoviSadizvestaj.txt')
        nazivfajla = analitics.kreiraj_naziv_fajla_grad('beograd')
        self.assertEqual(nazivfajla,'beogradizvestaj.txt')
    def test_upisi_u_fajlgrad(self):
        analitics = DatabaseAnalytics()
        f = analitics.upisi_u_fajl_grad('fajl.txt','grad','1-1;2-2;3-3'.encode())
        self.assertTrue(filecmp.cmp('fajl.txt','tests/testgrad.txt',shallow=False))
        os.remove('fajl.txt')
    def test_upisi_u_fajl_brojilo(self):
        analitics = DatabaseAnalytics()
        f = analitics.upisi_u_fajl_brojilo('fajl2.txt','1','1-1;2-2;3-3'.encode())
        self.assertTrue(filecmp.cmp('fajl2.txt','tests/testbrojilo.txt',shallow=False))
        os.remove('fajl2.txt') 

