import calculator.calc_functions as calc_functions
import unittest

class Calctests(unittest.TestCase):

    def test_add(self):
        self.assertEqual(calc_functions.add(2, 4), 6)

    def test_subtract(self):
        self.assertEqual(calc_functions.subtract(2, 4), -2)

    def test_multiply(self):
        self.assertEqual(calc_functions.multiply(2, 4), 8)

    def test_divide(self):
        self.assertEqual(calc_functions.divide(2, 4), 0.5)
