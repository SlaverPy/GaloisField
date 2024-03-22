class GaloisField:
    def __init__(self, p, n=1):
        if not self.is_prime(p):
            raise ValueError(f"{p} не является простым числом.")
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n должно быть положительным целым числом")
        self._p = p
        self._n = n

    @staticmethod
    def is_prime(number):
        if number < 2:
            return False
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                return False
        return True

    def __str__(self):
        return f"GF({self.p}^{self.n})"

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


class GaloisFieldElement:
    def __init__(self, value, field):
        self.field = field
        if isinstance(value, int):
            # Преобразование целого числа в список коэффициентов полинома над GF(2)
            self.coefficients = [int(bit) for bit in bin(value)[2:]]
        elif isinstance(value, list):
            # Если value уже список, используем его как коэффициенты напрямую
            self.coefficients = value
        else:
            raise TypeError("value должно быть целым числом или списком")
        # Дополнение списка коэффициентов нулями слева, если это необходимо
        while len(self.coefficients) < field.n:
            self.coefficients.insert(0, 0)

    def __add__(self, other):
        self._check_field(other)
        max_len = max(len(self.coefficients), len(other.coefficients))
        # Дополнение короткого списка нулями справа для выравнивания длины
        a = self.coefficients + [0] * (max_len - len(self.coefficients))
        b = other.coefficients + [0] * (max_len - len(other.coefficients))
        # Сложение полиномов путём побитового XOR коэффициентов
        result = [(a[i] + b[i]) % 2 for i in range(max_len)]
        # Преобразование списка коэффициентов обратно в целое число
        result_value = int("".join(map(str, result)), 2)
        return GaloisFieldElement(result_value, self.field)

    def __sub__(self, other):
        self._check_field(other)
        max_len = max(len(self.coefficients), len(other.coefficients))
        result = [(self.coefficients[i] if i < len(self.coefficients) else 0) -
                  (other.coefficients[i] if i < len(other.coefficients) else 0)
                  for i in range(max_len)]
        return GaloisFieldElement(result, self.field).normalize()

    def __mul__(self, other):
        self._check_field(other)
        result = [0] * (len(self.coefficients) + len(other.coefficients) - 1)
        for i, coef1 in enumerate(self.coefficients):
            for j, coef2 in enumerate(other.coefficients):
                result[i + j] += coef1 * coef2
        return GaloisFieldElement(result, self.field).normalize()

    def __truediv__(self, other):
        self._check_field(other)
        quotient, remainder = self.poly_divmod_gf2(self.coefficients, other.coefficients)
        return GaloisFieldElement(quotient), GaloisFieldElement(remainder)

    @staticmethod
    def poly_divmod_gf2(num, den):
        num = num[:]
        den = den[:]
        output = [0] * (len(num) - len(den) + 1)
        den_shift = len(num) - len(den)
        den = [0] * den_shift + den

        for i in range(len(output)):
            if num[0] == 1:
                coeff = 1
                output[i] = coeff
                den_temp = [0] * i + den
                num = [(n + d) % 2 for n, d in zip(num, den_temp + [0] * (len(num) - len(den_temp)))]
                while num and num[0] == 0:
                    num.pop(0)
        remainder = num
        return output, remainder

    def __eq__(self, other):
        self._check_field(other)
        return self.normalize().coefficients == other.normalize().coefficients

    def __ne__(self, other):
        return not self.__eq__(other)

    def __pow__(self, power):
        pass

    def normalize(self):
        i = len(self.coefficients) - 1
        while i > 0 and self.coefficients[i] == 0:
            i -= 1
        self.coefficients = self.coefficients[:i+1]
        return self

    def __str__(self):
        terms = []
        for i, coef in enumerate(self.coefficients):
            if i > 0:
                if coef == 1:
                    coef = ''
                if coef != 0:
                    if i == 1:
                        terms.append(f"{coef}x")
                    else:
                        terms.append(f"{coef}x^{i}")
            else:
                if coef != 0:
                    terms.append(str(coef))

        return " + ".join(terms) or "0"

    def _check_field(self, other):
        if self.field.p != other.field.p or self.field.n != other.field.n:
            raise ValueError("Элементы должны принадлежать одному и тому же полю.")

    def extended_gcd(self, a, b):
        """
        Возвращает кортеж (gcd, x, y), где gcd - НОД(a, b), и ax + by = gcd.
        """
        if a == 0:
            return (b, 0, 1)
        else:
            gcd, x1, y1 = self.extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return (gcd, x, y)

    def mod_inverse(self, a, m):
        """
        Возвращает мультипликативный обратный к a по модулю m.
        """
        gcd, x, _ = self.extended_gcd(a, m)
        if gcd != 1:
            raise Exception('Обратный элемент не существует')
        else:
            # x может быть отрицательным, поэтому приводим его к положительному эквиваленту в модуле m
            return x % m


GF = GaloisField(2, 3)
poly = GaloisFieldElement(3, field=GF)
other_poly = GaloisFieldElement(5, field=GF)

# Сложение полиномов
sum_poly = poly + other_poly

# Вывод результатов
print("Полином 1:", poly)  # Должно вывести представление полинома 3 в GF(2^3)
print("Полином 2:", other_poly)  # Должно вывести представление полинома 5 в GF(2^3)
print("Сложение полиномов:", sum_poly)  # Должно вывести результат сложения, эк

# print("Вычитание полиномов:", sub_poly) # x + x^2
# mul_poly = poly * other_poly
# # Умножение полиномов
# # mul_poly = poly * other_poly
# print("Умножение полиномов:", mul_poly) # 1 + x + x^2 + x^3 + x^4 + x^5 + x^6
#
# Деление полиномов
# print("Деление полиномов",poly / other_poly )

# # Возведение полинома в степень
# squared_poly = poly ** 2
# print("Квадрат полинома:", squared_poly)
