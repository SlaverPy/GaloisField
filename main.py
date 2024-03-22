class GaloisField:
    def __init__(self, p, n):
        if not self.is_prime(p):
            raise ValueError("p должно быть простым числом")
        if n == 1 or not isinstance(n, int) or n <= 0:
            raise ValueError("n должно быть положительным целым числом больше 0")
        self._p = p
        self._n = n

    @staticmethod
    def is_prime(number):
        """Проверка числа на простоту."""
        if number <= 1:
            return False
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                return False
        return True

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, value):
        if not self.is_prime(value):
            raise ValueError("p должно быть простым числом.")
        self._p = value

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("n должно быть положительным целым числом")
        self._n = value

    def __str__(self):
        return f"Поле: GF({self.p}^{self.n})"


class GaloisFieldElement:
    def __init__(self, value, field):
        if not isinstance(value, int) or value < 0 or value >= field.p ** field.n:
            raise ValueError("Значение должно быть неотрицательным целым числом, меньшим, чем p^n")
        self.value = value
        self.field = field

    def __add__(self, other):
        if self.field != other.field:
            raise ValueError("Нельзя складывать элементы из разных полей")
        return GaloisFieldElement((self.value + other.value) % self.field.p, self.field)

    def __sub__(self, other):
        if self.field != other.field:
            raise ValueError("Нельзя вычитать элементы из разных полей")
        return GaloisFieldElement((self.value - other.value) % self.field.p, self.field)

    def __mul__(self, other):
        if self.field != other.field:
            raise ValueError("Нельзя умножать элементы из разных полей")
        return GaloisFieldElement((self.value * other.value) % self.field.p, self.field)

    def __truediv__(self, other):
        # Использование расширенного алгоритма Евклида для нахождения обратного элемента
        inv = self._inv(other.value, self.field.p)
        return GaloisFieldElement((self.value * inv) % self.field.p, self.field)

    def __eq__(self, other):
        return self.field == other.field and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"{self.value} в GF({self.field.p}^{self.field.n})"

    def __pow__(self, exponent):
        # Возведение в степень по модулю p
        return GaloisFieldElement(pow(self.value, exponent, self.field.p), self.field)

    @staticmethod
    def _inv(a, m):
        # Расширенный алгоритм Евклида
        g, x, _ = GaloisFieldElement._extended_gcd(a, m)
        if g != 1:
            raise Exception('Обратный элемент не существует')
        else:
            return x % m

    @staticmethod
    def _extended_gcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = GaloisFieldElement._extended_gcd(b % a, a)
            return (g, x - (b // a) * y, y)


class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = coefficients

    def __add__(self, other):
        # Сложение полиномов с учетом коэффициентов по модулю 2 (для GF(2^n))
        result = {}
        for power in set(self.coefficients) | set(other.coefficients):
            coef1 = self.coefficients.get(power, 0)
            coef2 = other.coefficients.get(power, 0)
            result[power] = (coef1 + coef2) % 2  # Сложение по модулю 2
        return Polynomial(result)

    def __str__(self):
        if not self.coefficients:
            return '0'
        terms = []
        for power, coef in sorted(self.coefficients.items(), reverse=True):
            if coef:
                if power == 0:
                    terms.append('1')
                elif power == 1:
                    terms.append('x')
                else:
                    terms.append(f'x^{power}')
        return ' + '.join(terms) or '0'


# Пример использования

# Создание поля GF(7)
# gf7 = GaloisField(7, 1)
#
# # Создание элементов поля
# a = GaloisFieldElement(3, gf7)
# b = GaloisFieldElement(5, gf7)
#
# print(f"a = {a}")
# print(f"b = {b}")
#
def poly_divmod_gf2(num, den):
    # Преобразуем полиномы в двоичный формат для удобства работы
    num_poly = num[:]
    den_poly = den[:]
    quotient = [0] * (len(num) - len(den) + 1)

    # Главный цикл деления
    while len(num_poly) >= len(den_poly):
        # Определяем степень текущего делимого и делителя
        diff = len(num_poly) - len(den_poly)

        # Вычисляем частное для текущего шага деления
        quotient[diff] = 1
        # Вычитание (в GF(2) это эквивалентно сложению) делителя, умноженного на x^diff, из делимого
        den_temp = [0] * diff + den_poly
        num_poly = [(n + d) % 2 for n, d in zip(num_poly + [0] * (len(den_temp) - len(num_poly)), den_temp)]

        # Удаляем ведущие нули в текущем делимом
        while num_poly and num_poly[0] == 0:
            num_poly.pop(0)

    remainder = num_poly
    return quotient, remainder


# Пример использования
num = [1, 0, 1, 1]  # x^3 + x + 1
den = [1, 1, 0, 1]  # x^3 + x^2 + 1

quotient, remainder = poly_divmod_gf2(num, den)

# Преобразуем результат в удобочитаемый формат
quotient_str = " + ".join([f"x^{i}" if i != 0 else "1" for i, bit in enumerate(reversed(quotient)) if bit]) or "0"
remainder_str = " + ".join([f"x^{i}" if i != 0 else "1" for i, bit in enumerate(reversed(remainder)) if bit]) or "0"

print(f"Частное от деления: {quotient_str}")
print(f"Остаток от деления: {remainder_str}")


