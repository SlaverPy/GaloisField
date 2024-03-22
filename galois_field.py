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
    def p(self) -> int:
        """
        Возвращает характеристику поля Галуа (простое число p).

        :return: Характеристика поля Галуа.
        """
        return self._p

    @p.setter
    def p(self, value: int):
        """
        Устанавливает характеристику поля Галуа (простое число p).

        :param value: Новая характеристика поля Галуа.
        """
        self._p = value

    @property
    def n(self) -> int:
        """
        Возвращает степень расширения поля Галуа.

        :return: Степень расширения поля Галуа.
        """
        return self._n

    @n.setter
    def n(self, value: int):
        """
        Устанавливает степень расширения поля Галуа.

        :param value: Новая степень расширения поля Галуа.
        """
        self._n = value

    @property
    def order(self) -> int:
        """
        Возвращает порядок поля Галуа, который равен p^n.

        :return: Порядок поля Галуа.
        """
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
