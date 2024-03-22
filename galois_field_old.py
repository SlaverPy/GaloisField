from itertools import zip_longest


class GaloisField:
    """
    Класс для представления поля Галуа GF(p^n).

    :ivar _p: Характеристика поля.
    :ivar _n: Степень расширения поля.
    :ivar _order: Порядок поля, равный p^n.
    """

    def __init__(self, p: int, n: int = 1):
        """
        Инициализирует новый экземпляр класса поля Галуа.

        :param p: Простое число, характеристика поля.
        :param n: Степень расширения поля. По умолчанию равно 1.
        :raises ValueError: Если p не является простым числом.
        :raises ValueError: Если n не является положительным целым числом.
        """
        if not self.is_prime(p):
            raise ValueError("p должно быть простым числом")
        if n <= 0:
            raise ValueError("n должно быть положительным целым числом")
        self._p = p
        self._n = n
        self._order = p ** n

    def __call__(self, value):
        """Создание нового объекта, представляющего элемент поля Галуа."""
        return Element(value, self)

    def __str__(self) -> str:
        """
        Строковое представление поля Галуа.

        :return: Значение Поля.
        """
        return f"GF({self.p}^{self.n})"

    def is_prime(self, num: int) -> bool:
        """
        Проверяет, является ли заданное число простым.

        :param num: Число для проверки на простоту.
        :return: True, если число простое, иначе False.
        """
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True



    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, value):
        self._p = value

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        self._n = value

    @property
    def order(self):
        return self._order


class Element:
    """
    Класс для представления элемента поля Галуа.

    :ivar field: Поле Галуа, к которому принадлежит элемент.
    :ivar value: Значение элемента в поле.
    """

    def __init__(self, value: int, field: GaloisField):
        """
        Инициализирует новый экземпляр элемента поля Галуа.

        :param value: Значение элемента в поле.
        :param field: Экземпляр класса поля Галуа, к которому принадлежит элемент.
        """
        self.field = field
        self.value = value % field.order

    def __add__(self, other: 'Element') -> 'Element':
        """
        Сложение двух элементов поля Галуа.

        :param other: Второй элемент для сложения.
        :return: Новый элемент поля Галуа, результат сложения.
        """
        return Element((self.value + other.value) % self.field.order, self.field)

    def __sub__(self, other: 'Element') -> 'Element':
        """
        Вычитание элементов поля Галуа.

        :param other: Второй элемент для вычитания.
        :return: Новый элемент поля Галуа, результат вычитания.
        """
        return Element((self.value - other.value) % self.field.order, self.field)

    def __mul__(self, other: 'Element') -> 'Element':
        """
        Умножение элементов поля Галуа.

        :param other: Второй элемент для умножения.
        :return: Новый элемент поля Галуа, результат умножения.
        """
        return Element((self.value * other.value) % self.field.order, self.field)

    def __truediv__(self, other: 'Element') -> 'Element':
        """
        Деление элементов поля Галуа.

        :param other: Второй элемент для деления.
        :return: Новый элемент поля Галуа, результат деления.
        """
        return Element((self.value * other.inverse().value) % self.field.order, self.field)



    def __pow__(self, exponent):
        if exponent < 0:
            result = self.inverse()
            return result
        else:
            result = Element(1, self.field)
        base = self
        while exponent > 0:
            if exponent % 2 == 1:
                result = result * base
            base = base * base
            exponent = exponent // 2
        return result

    def __eq__(self, other: 'Element') -> bool:
        """
        Проверяет равенство двух элементов поля Галуа.

        :param other: Элемент поля Галуа, с которым сравнивается текущий элемент.
        :return: True, если значения элементов равны, иначе False.
        """
        return self.value == other.value

    def __ne__(self, other: 'Element') -> bool:
        """
        Проверяет неравенство двух элементов поля Галуа.

        :param other: Элемент поля Галуа, с которым сравнивается текущий элемент.
        :return: True, если значения элементов различаются, иначе False.
        """
        return not self.__eq__(other)

    def __str__(self) -> str:
        """
        Строковое представление значения элемента поля Галуа.

        :return: Значение элемента.
        """
        return f"{self.value}"

    def inverse(self) -> 'Element':
        """
        Нахождение обратного элемента по расширенному алгоритму Евклида

        :return: Обратный элемент поля Галуа.
        :raises ValueError: Если обратный элемент не существует.
        """
        g, x, _ = self.extended_gcd(self.value, self.field.order)
        if g != 1:
            raise ValueError("Обратный элемент не существует")
        return Element(x % self.field.order, self.field)

    def extended_gcd(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, x, y = self.extended_gcd(b % a, a)
            return g, y - (b // a) * x, x


# class Polynomial:
#     def __init__(self, input_data, field):
#         self.field = field
#         if isinstance(input_data, str):
#             coefficients = self._parse_polynomial_string(input_data)
#         else:
#             coefficients = input_data
#         self.coefficients = [self.field(x).value for x in coefficients]
#         while len(self.coefficients) > 1 and self.coefficients[-1] == 0:
#             self.coefficients.pop()
#
#     def _parse_polynomial_string(self, polynomial_str):
#         # Анализ строкового представления полинома для получения списка коэффициентов
#         coefficients = []
#         for term in polynomial_str.split('+'):
#             term = term.strip()
#             if 'x^' in term:
#                 coeff, _, power = term.partition('x^')
#                 power = int(power)
#             elif 'x' in term:
#                 coeff, _ = term.split('x')
#                 power = 1
#             else:
#                 coeff = term
#                 power = 0
#             coeff = int(coeff) if coeff else 1
#             # Расширяем список коэффициентов при необходимости
#             while len(coefficients) <= power:
#                 coefficients.append(0)
#             coefficients[power] = coeff
#         # Инвертируем список для совместимости с порядком, используемым в других методах
#         return list(reversed(coefficients))
#
#     def __add__(self, other):
#         result_coefficients = []
#         for coef1, coef2 in zip_longest(self.coefficients, other.coefficients, fillvalue=self.field(0)):
#             if isinstance(coef2, Element):
#                 coef2 = coef2.value
#             result_coefficients.append(coef1 + coef2)
#         return Polynomial(result_coefficients, self.field)
#
#     def __sub__(self, other):
#         result_coefficients = []
#         for coef1, coef2 in zip_longest(self.coefficients, other.coefficients, fillvalue=self.field(0)):
#             if isinstance(coef2, Element):
#                 coef2 = coef2.value
#             result_coefficients.append(coef1 - coef2)
#         return Polynomial(result_coefficients, self.field)
#
#     def __mul__(self, other):
#         result_deg = len(self.coefficients) + len(other.coefficients) - 2
#         result_coefficients = [self.field(0)] * (result_deg + 1)
#         for i, coef1 in enumerate(self.coefficients):
#             for j, coef2 in enumerate(other.coefficients):
#                 result_coefficients[i + j] += coef1 * coef2
#         return Polynomial(result_coefficients, self.field)
#
#     def __str__(self):
#         terms = []
#         for i, coeff in enumerate(reversed(self.coefficients)):  # Обращаем внимание на порядок следования коэффициентов
#             if coeff != 0:
#                 term = str(coeff)
#                 if i > 0:
#                     term += f"x^{i}"
#                 terms.append(term)
#         return " + ".join(terms) or "0"
class Polynomial(GaloisField):
    def __init__(self, coefficients, field):
        self.coefficients = [field(coef) for coef in coefficients]  # Коэффициенты полинома как элементы поля
        self.field = field
        self.normalize()

    def normalize(self):
        """Удаление ведущих нулей."""
        while self.coefficients and self.coefficients[-1].value == 0:
            self.coefficients.pop()

    def __str__(self):
        terms = []
        for i, coef in enumerate(reversed(self.coefficients)):
            if coef.value != 0:
                term = f"{coef}"
                if i > 0:
                    term += f"x^{i}"
                terms.append(term)
        return " + ".join(terms) or "0"