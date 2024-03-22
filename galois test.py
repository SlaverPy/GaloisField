import galois

# Создание полинома над GF(2)
GF = galois.GF(2)
poly = galois.Poly([1, 0, 1, 1], field=GF)  # Создаем полином x^3 + x + 1 над GF(2)

# Печатаем полином
print("Полином:", poly)

# Создаем другой полином и выполняем операцию сложения
other_poly = galois.Poly([1, 1, 0, 1], field=GF)  # x^3 + x^2 + 1
sum_poly = poly + other_poly

# Печатаем результат сложения
print("Сложение полиномов:", sum_poly)
print("Вычитание", poly - other_poly)

# Умножение полиномов
mul_poly = poly * other_poly
print("Умножение полиномов:", mul_poly)

# Деление полиномов
quotient, remainder = divmod(poly, other_poly)
print("Частное от деления:", quotient)
print("Остаток от деления:", remainder)

# Возведение полинома в степень
squared_poly = poly ** 2
print("Квадрат полинома:", squared_poly)
