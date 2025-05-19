import os
import re

class CommandEditor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = self.load_file()
        self.history = []  # история изменений
        self.copied_text = ""  # для хранения скопированного текста
        self.unsaved_changes = False  # флаг наличия несохраненных изменений

    def load_file(self):
        """Загружает содержимое файла, если он существует, иначе создает пустой файл."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return file.readlines()
        else:
            # если файл не существует, создаем пустой файл.
            with open(self.file_path, 'w') as file:
                pass
            return []

    def save(self):
        """Сохраняет изменения в файл и добавляет текущее состояние в историю."""
        self.history.append(self.lines[:])  # сохраняем текущее состояние
        with open(self.file_path, 'w') as file:
            file.writelines(self.lines)
        self.unsaved_changes = False  # изменения сохранены
        print(f"Файл '{self.file_path}' сохранен.")

    def insert(self, text, num_row=None, num_col=None):
        """Вставляет текст в файл в указанное место."""
        self.history.append(self.lines[:])  # сохраняем текущее состояние перед изменением
        self.unsaved_changes = True  # изменения не сохранены

        if num_row is None:
            num_row = len(self.lines) + 1  # вставляем в новую строку в конец файла

        if num_col is None:
            num_col = 0

        # если номер строки больше, чем количество строк в файле, добавляем пустые строки
        while len(self.lines) < num_row:
            self.lines.append("\n")

        line = self.lines[num_row - 1]
        self.lines[num_row - 1] = line[:num_col] + text + line[num_col:]
        print(f"Текст '{text}' вставлен в строку {num_row}, позиция {num_col}.")

    def delete_all(self):
        """Удаляет все содержимое файла."""
        self.history.append(self.lines[:])  # сохраняем текущее состояние
        self.unsaved_changes = True  # изменения не сохранены
        self.lines = []  # очистка всех строк
        print(f"Все содержимое файла '{self.file_path}' удалено.")

    def delete_row(self, num_row):
        """Удаляет указанную строку из файла."""
        if num_row is None or num_row <= 0 or num_row > len(self.lines):
            print("Ошибка: Неверный номер строки для удаления.")
        else:
            self.history.append(self.lines[:])  # сохраняем текущее состояние
            self.unsaved_changes = True  # изменения не сохранены
            self.lines.pop(num_row - 1)  # удаляем строку по номеру
            print(f"Строка {num_row} удалена.")

    def delete_column(self, num_col):
        """Удаляет указанный столбец из всех строк."""
        if num_col is None or num_col <= 0:
            print("Ошибка: Неверный номер столбца для удаления.")
            return
        
        self.history.append(self.lines[:])  # сохраняем текущее состояние
        self.unsaved_changes = True  # изменения не сохранены

        # удаление столбца из каждой строки
        for i in range(len(self.lines)):
            if num_col - 1 < len(self.lines[i]):
                self.lines[i] = self.lines[i][:num_col - 1] + self.lines[i][num_col:]
        
        print(f"Столбец {num_col} удален из всех строк.")

    def swap_lines(self, num_row_1, num_row_2):
        """Меняет местами две строки в файле."""
        if num_row_1 is None or num_row_2 is None:
            print("Ошибка: Номера строк не указаны для обмена.")
            return

        if num_row_1 <= 0 or num_row_1 > len(self.lines) or num_row_2 <= 0 or num_row_2 > len(self.lines):
            print("Ошибка: Неверные номера строк для обмена.")
            return

        self.history.append(self.lines[:])  # сохраняем текущее состояние
        self.unsaved_changes = True  # изменения не сохранены

        # меняем местами строки
        self.lines[num_row_1 - 1], self.lines[num_row_2 - 1] = self.lines[num_row_2 - 1], self.lines[num_row_1 - 1]
        print(f"Строки {num_row_1} и {num_row_2} были обменяны местами.")

    def undo(self, num_operations=1):
        """Отменяет последние изменения в файле."""
        if num_operations <= 0:
            print("Ошибка: Количество операций должно быть положительным числом.")
            return

        # откатываем изменения
        for _ in range(num_operations):
            if self.history:
                self.lines = self.history.pop()
                self.unsaved_changes = True  # изменения не сохранены после отмены
                print(f"Отменено {num_operations} изменений.")
            else:
                print("Ошибка: Нет доступных изменений для отмены.")
                break

    def copy(self, num_row, start=None, end=None):
        """Копирует текст из строки num_row начиная с позиции start до end."""
        if num_row is None or num_row <= 0 or num_row > len(self.lines):
            print("Ошибка: Неверный номер строки для копирования.")
            return

        line = self.lines[num_row - 1]

        if start is None:
            start = 0
        if end is None or end > len(line):
            end = len(line)

        if start < 0 or end > len(line) or start > end:
            print("Ошибка: Неверные значения для start и end.")
            return

        self.copied_text = line[start:end]
        print(f"Копирован текст: '{self.copied_text}' из строки {num_row}, позиция {start}-{end}.")

    def paste(self, num_row):
        """Вставляет скопированный текст в указанную строку."""
        if not self.copied_text:
            print("Ошибка: Нет скопированного текста для вставки.")
            return
        
        if num_row is None or num_row <= 0 or num_row > len(self.lines):
            print("Ошибка: Неверный номер строки для вставки.")
            return
        
        self.history.append(self.lines[:])  # сохраняем текущее состояние
        self.unsaved_changes = True  # изменения не сохранены

        # вставляем скопированный текст в начало указанной строки
        self.lines[num_row - 1] = self.copied_text + self.lines[num_row - 1]
        print(f"Скопированный текст вставлен в строку {num_row}.")

    def show(self):
        """Показывает текущее состояние файла."""
        print("\nТекущее состояние файла:")
        for line in self.lines:
            print(line, end="")
        print("\n")

    def run(self):
        """Основной цикл обработки команд."""
        while True:
            command = input("Введите команду (insert/save/del/delrow/delcol/swap/undo/copy/paste/show/exit): ").strip()
            if command == "exit":
                if self.unsaved_changes:
                    save_prompt = input("У вас есть несохраненные изменения. Хотите сохранить файл? (y/n): ").strip().lower()
                    if save_prompt == "y":
                        self.save()
                break
            elif command.startswith("insert"):
                match = re.match(r'insert\s+"(.*?)"\s*(\d*)\s*(\d*)', command)
                if match:
                    text = match.group(1)
                    num_row = int(match.group(2)) if match.group(2) else None
                    num_col = int(match.group(3)) if match.group(3) else None
                    self.insert(text, num_row, num_col)
                else:
                    print("Ошибка: Неверный формат команды insert.")
            elif command == "save":
                self.save()
            elif command == "show":
                self.show()
            elif command == "del":
                self.delete_all()
            elif command.startswith("delrow"):
                match = re.match(r'delrow\s*(\d+)', command)
                if match:
                    num_row = int(match.group(1))
                    self.delete_row(num_row)
                else:
                    print("Ошибка: Неверный формат команды delrow.")
            elif command.startswith("delcol"):
                match = re.match(r'delcol\s*(\d+)', command)
                if match:
                    num_col = int(match.group(1))
                    self.delete_column(num_col)
                else:
                    print("Ошибка: Неверный формат команды delcol.")
            elif command.startswith("swap"):
                match = re.match(r'swap\s*(\d+)\s*(\d+)', command)
                if match:
                    num_row_1 = int(match.group(1))
                    num_row_2 = int(match.group(2))
                    self.swap_lines(num_row_1, num_row_2)
                else:
                    print("Ошибка: Неверный формат команды swap.")
            elif command.startswith("undo"):
                match = re.match(r'undo\s*(\d*)', command)
                if match:
                    num_operations = int(match.group(1)) if match.group(1) else 1
                    self.undo(num_operations)
                else:
                    print("Ошибка: Неверный формат команды undo.")
            elif command.startswith("copy"):
                match = re.match(r'copy\s*(\d+)\s*(\d*)\s*(\d*)', command)
                if match:
                    num_row = int(match.group(1))
                    start = int(match.group(2)) if match.group(2) else None
                    end = int(match.group(3)) if match.group(3) else None
                    self.copy(num_row, start, end)
                else:
                    print("Ошибка: Неверный формат команды copy.")
            elif command.startswith("paste"):
                match = re.match(r'paste\s*(\d+)', command)
                if match:
                    num_row = int(match.group(1))
                    self.paste(num_row)
                else:
                    print("Ошибка: Неверный формат команды paste.")
            else:
                print("Неизвестная команда.")

if __name__ == "__main__":
    file_path = input("Введите путь к файлу: ").strip()
    editor = CommandEditor(file_path)
    editor.run()
