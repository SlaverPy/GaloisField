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


