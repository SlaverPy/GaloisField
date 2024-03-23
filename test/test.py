import unittest
from galois_field_old import GaloisField


class TestElementGF7(unittest.TestCase):
    """Тестирование операций в поле Галуа GF(7)."""
    def setUp(self):
        """Инициализация тестового окружения."""
        self.gf = GaloisField(7)
        self.elem1 = self.gf(3)
        self.elem2 = self.gf(5)

    def test_addition_GF_7(self):
        """Тестирование сложения элементов в GF(7)."""
        result = self.elem1 + self.elem2
        self.assertEqual(result.value, 1)

    def test_subtraction_GF_7(self):
        """Тестирование вычитания элементов в GF(7)."""
        result = self.elem1 - self.elem2
        self.assertEqual(result.value, 5)

    def test_multiplication_GF_7(self):
        """Тестирование перемножения элементов в GF(7)."""
        result = self.elem1 * self.elem2
        self.assertEqual(result.value, 1)

    def test_division_GF_7(self):
        """Тестирование деления элементов в GF(7)."""
        result = self.elem1 / self.elem2
        self.assertEqual(result.value, 2)

    def test_power_GF_7(self):
        """Тестирование возведение в степень элементов в GF(7)."""
        result = self.elem1 ** 2
        self.assertEqual(result.value, 2, "3^2 mod 7 should be 2")

        result = self.elem2 ** 3
        self.assertEqual(result.value, 6, "5^3 mod 7 should be 6")

        result = self.elem1 ** 0
        self.assertEqual(result.value, 1, "Any number to the power of 0 should be 1")

        result = self.elem2 ** -1
        self.assertEqual(result.value, 3, "The inverse of 5 mod 7 should be 3")

    def test_equality_GF_7(self):
        """Тестирование сравнения равенства и неравенства элементов в GF(7)."""
        self.assertTrue(self.elem1 == self.gf(3))
        self.assertFalse(self.elem1 == self.elem2)

    def test_inverse_GF_7(self):
        """
        Тестирование нахождения обратного элемента в поле Галуа GF(7).

        Проверяет, что обратный элемент для `elem2` (значение 5 в GF(7))
        равен ожидаемому значению (3), так как 5 * 3 mod 7 = 1.
        """
        inverse = self.elem2.inverse()
        self.assertEqual(inverse.value, 3)


class TestElementGF2(unittest.TestCase):
    """Тестирование операций в поле Галуа GF(2)."""
    def setUp(self):
        """Инициализация тестового окружения."""
        self.gf = GaloisField(2)
        self.elem1 = self.gf(3)
        self.elem2 = self.gf(4)

    def test_chek_value(self):
        """
        Проверка значений элементов в поле Галуа GF(2).

        Этот тест убеждается, что значения элементов корректно
        отражают ожидаемые значения в контексте поля GF(2),
        где возможные значения элементов ограничены 0 и 1.
        Тест проверяет, что после инициализации элементов поля
        их значения соответствуют ожидаемым (1 и 0 соответственно),
        что важно для поддержания инвариантов поля Галуа.
        """
        self.assertEqual(self.elem1.value, 1)
        self.assertEqual(self.elem2.value, 0)

    def test_addition_GF_2(self):
        """Тестирование сложения элементов в GF(2)."""
        result = self.elem1 + self.elem2
        self.assertEqual(result.value, 1)

    def test_subtraction_GF_2(self):
        """Тестирование вычитания элементов в GF(2)."""
        result = self.elem1 - self.elem2
        self.assertEqual(result.value, 1)

    def test_multiplication_GF_2(self):
        """Тестирование перемножения элементов в GF(2)."""
        result = self.elem1 * self.elem2
        self.assertEqual(result.value, 0)

    def test_division_GF_2(self):
        """Тестирование деления элементов в GF(2)."""
        result = self.elem2 / self.elem1
        self.assertEqual(result.value, 0)
        with self.assertRaises(ValueError):
            self.elem1 / self.elem2

    def test_power_GF_2(self):
        """Тестирование возведение в степень элементов в GF(2)."""
        result = self.elem1 ** 2
        self.assertEqual(result.value, 1, "1^2 mod 2 should be 1")

        result = self.elem2 ** 3
        self.assertEqual(result.value, 0, "0^3 mod 2 should be 0")

        result = self.elem1 ** 0
        self.assertEqual(result.value, 1, "Any number to the power of 0 should be 1")

    def test_equality_GF_2(self):
        """Тестирование сравнения равенства и неравенства элементов в GF(2)."""
        self.assertTrue(self.elem1 == self.gf(3))
        self.assertFalse(self.elem1 == self.elem2)

    def test_inverse_GF_2(self):
        """
        Тестирование попытки нахождения обратного элемента в GF(2),
        для случая, когда обратный элемент не существует.

        Ожидается возникновение исключения ValueError для элемента,
        для которого обратный элемент не может быть найден.
        В контексте поля GF(2), это тест может проверять,
        что обратного элемента не существует для нулевого элемента.
        """
        with self.assertRaises(ValueError):
            self.elem2.inverse()


if __name__ == '__main__':
    unittest.main()
