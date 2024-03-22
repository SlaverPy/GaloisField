import json
import yaml
from galois_field_old import GaloisField, Element


class FieldOperationProcessor:
    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '^': lambda x, y: x ** y.value,
    }

    def __init__(self, filename):
        self.filename = filename
        self.data = self.read_file()

    def read_file(self):
        """Читаем данные из JSON или YAML файла."""
        if self.filename.endswith('.json'):
            with open(self.filename, 'r') as f:
                return json.load(f)
        elif self.filename.endswith('.yaml') or self.filename.endswith('.yml'):
            with open(self.filename, 'r') as f:
                return yaml.safe_load(f)
        else:
            raise ValueError("Файл должен быть формата JSON или YAML")

    def perform_operation(self, field_data):
        elem1 = field_data.get("elem1")
        elem2 = field_data.get("elem2")
        operation = field_data.get("operation")
        if "p" in field_data:
            p = field_data.get("p")
            n = field_data.get("n")
            return self.operation_in_the_field(p, n, elem1, elem2, operation)

        elif "polynomial" in field_data:
            polynomial = field_data.get("polynomial")

        else:
            return "Отсутствуют параметры поля или полином"

    def operation_in_the_field(self, p, n, elem1, elem2, operation):
        gf = GaloisField(p, n)
        elem1 = gf(elem1)
        elem2 = gf(elem2)
        if operation in self.operations:
            try:
                result = self.operations[operation](elem1, elem2)
                return f"Результат: {result}"
            except Exception as e:
                return f"Ошибка при выполнении операции: {e}"
        else:
            print(operation)


    def process_data(self):
        """Обработка списка объектов."""
        results = []
        for obj in self.data:
            try:
                result = self.perform_operation(obj)
                results.append(result)
            except Exception as e:
                results.append(f"Ошибка: {e}")
        return results


if __name__ == "__main__":
    file_path = "example.json"
    processor = FieldOperationProcessor(file_path)
    results = processor.process_data()
    for result in results:
        print(result)
