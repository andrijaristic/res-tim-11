from database_crud.database_management import TerminalOperations
import unittest
from unittest import mock
from unittest.mock import patch

class TestTerminalOperations(unittest.TestCase):

    @patch('builtins.print')
    def test_meni(self, mock_print):
        terminal_operations = TerminalOperations()
        terminal_operations.meni()
        mock_print.side_effect = ["\n=======================", "1. Create row", "2. Delete row", "3. Update row", "X. Exit", "======================="]

    @patch('builtins.input')
    def test_input_params(self, mock_input):
        terminal_operations = TerminalOperations()
        mock_input.side_effect = ['A', 'A', 'AA', '10', '100', 'AAA']
        self.assertAlmostEqual(terminal_operations.input_params(), ('A', 'A', 'AA', '10', '100', 'AAA'))

    @patch('builtins.input')
    def test_input_option(self, mock_input):
        terminal_operations = TerminalOperations()
        mock_input.side_effect = '1'
        self.assertAlmostEqual(terminal_operations.input_option(), '1')

    @patch('builtins.input')
    def test_input_id(self, mock_input):
        terminal_operations = TerminalOperations()
        mock_input.side_effect = '1'
        self.assertAlmostEqual(terminal_operations.input_id(), '1')
