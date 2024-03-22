import unittest
from galois_field_old import GaloisField, Polynomial


class TestElementGF7(unittest.TestCase):
    def setUp(self):
        self.gf = GaloisField(7)
        self.elem1 = self.gf(3)
        self.elem2 = self.gf(5)

    def test_addition_GF_7(self):
        # Проверяем сложение элементов
        result = self.elem1 + self.elem2
        self.assertEqual(result.value, 1)

    def test_subtraction_GF_7(self):
        result = self.elem1 - self.elem2
        self.assertEqual(result.value, 5)

    def test_multiplication_GF_7(self):
        result = self.elem1 * self.elem2
        self.assertEqual(result.value, 1)

    def test_division_GF_7(self):
        result = self.elem1 / self.elem2
        self.assertEqual(result.value, 2)

    def test_power_GF_7(self):
        result = self.elem1 ** 2
        self.assertEqual(result.value, 2, "3^2 mod 7 should be 2")

        result = self.elem2 ** 3
        self.assertEqual(result.value, 6, "5^3 mod 7 should be 6")

        result = self.elem1 ** 0
        self.assertEqual(result.value, 1, "Any number to the power of 0 should be 1")

        result = self.elem2 ** -1
        self.assertEqual(result.value, 3, "The inverse of 5 mod 7 should be 3")

    def test_equality_GF_7(self):
        self.assertTrue(self.elem1 == self.gf(3))
        self.assertFalse(self.elem1 == self.elem2)

    def test_inverse_GF_7(self):
        inverse = self.elem2.inverse()
        self.assertEqual(inverse.value, 3)


class TestElementGF2(unittest.TestCase):
    def setUp(self):
        self.gf = GaloisField(2)
        self.elem1 = self.gf(3)
        self.elem2 = self.gf(4)

    def test_chek_value(self):
        self.assertEqual(self.elem1.value, 1)
        self.assertEqual(self.elem2.value, 0)

    def test_addition_GF_2(self):
        result = self.elem1 + self.elem2
        self.assertEqual(result.value, 1)

    def test_subtraction_GF_2(self):
        result = self.elem1 - self.elem2
        self.assertEqual(result.value, 1)

    def test_power_GF_2(self):
        result = self.elem1 ** 2
        self.assertEqual(result.value, 1, "1^2 mod 2 should be 1")

        result = self.elem2 ** 3
        self.assertEqual(result.value, 0, "0^3 mod 2 should be 0")

        result = self.elem1 ** 0
        self.assertEqual(result.value, 1, "Any number to the power of 0 should be 1")

    def test_multiplication_GF_2(self):
        result = self.elem1 * self.elem2
        self.assertEqual(result.value, 0)

    def test_division_GF_2(self):
        with self.assertRaises(ValueError):
            self.elem1 / self.elem2

    def test_equality_GF_2(self):
        self.assertTrue(self.elem1 == self.gf(3))
        self.assertFalse(self.elem1 == self.elem2)

    def test_inverse_GF_2(self):
        with self.assertRaises(ValueError):
            self.elem2.inverse()





if __name__ == '__main__':
    unittest.main()