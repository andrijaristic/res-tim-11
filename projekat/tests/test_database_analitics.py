import filecmp
import os
from unittest import mock
from unittest.mock import Mock
import unittest
from database_analitics.classes import DatabaseAnalytics
class TestDatabasaAnalitics(unittest.TestCase):
    def test_kreirajnazivfajlagrad(self):
        analitics = DatabaseAnalytics()
        nazivfajla = analitics.kreirajnazivfajlagrad('Novi Sad')
        self.assertEqual(nazivfajla,'NoviSadizvestaj.txt')
        nazivfajla = analitics.kreirajnazivfajlagrad('beograd')
        self.assertEqual(nazivfajla,'beogradizvestaj.txt')
    def test_upisiufajlgrad(self):
        analitics = DatabaseAnalytics()
        f = analitics.upisiufajlgrad('fajl.txt','grad','1-1;2-2;3-3'.encode())
        self.assertTrue(filecmp.cmp('fajl.txt','tests/testgrad.txt',shallow=False))
        os.remove('fajl.txt')
    def test_upisiufajlbrojilo(self):
        analitics = DatabaseAnalytics()
        f = analitics.upisiufajlbrojilo('fajl2.txt','1','1-1;2-2;3-3'.encode())
        self.assertTrue(filecmp.cmp('fajl2.txt','tests/testbrojilo.txt',shallow=False))
        os.remove('fajl2.txt') 

