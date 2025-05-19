import os
import hashlib
from collections import defaultdict

def get_file_hash(filepath, block_size=65536):
    """Вычисляет хеш SHA-256 файла"""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(block_size)
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()
    except (IOError, PermissionError):
        return None

def find_duplicates(directory):
    """Находит дубликаты файлов в указанной директории"""
    files_by_size = defaultdict(list)
    files_by_hash = defaultdict(list)
    
    # группировка по размеру
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                file_size = os.path.getsize(filepath)
                files_by_size[file_size].append(filepath)
            except (OSError, PermissionError):
                continue
    
    # проверка хеша
    for file_size, files in files_by_size.items():
        if len(files) > 1:
            for filepath in files:
                file_hash = get_file_hash(filepath)
                if file_hash:
                    files_by_hash[(file_size, file_hash)].append(filepath)
    
    return [files for files in files_by_hash.values() if len(files) > 1]

def user_select_action(duplicates):
    """Интерфейс выбора действия для дубликатов"""
    print(f"\nНайдено {len(duplicates)} дубликатов:")
    for i, filepath in enumerate(duplicates, 1):
        print(f"{i}. {filepath}")
    
    print("\nВыберите действие:")
    print("1-9: Оставить файл с указанным номером, остальные удалить")
    print("a: Оставить все файлы (пропустить)")
    print("d: Удалить все дубликаты")
    print("q: Выйти")
    
    while True:
        choice = input("Ваш выбор: ").strip().lower()
        if choice == 'a':
            return None
        elif choice == 'd':
            return []
        elif choice == 'q':
            exit()
        elif choice.isdigit() and 1 <= int(choice) <= len(duplicates):
            return [duplicates[int(choice)-1]]
        else:
            print("Неверный ввод. Попробуйте снова.")

def main():
    print("=== Поиск дубликатов файлов ===")
    directory = input("Введите путь к директории для проверки: ").strip()
    
    if not os.path.isdir(directory):
        print(f"Ошибка: '{directory}' не является директорией")
        return
    
    print(f"\nСканирую {directory}...")
    duplicates = find_duplicates(directory)
    
    if not duplicates:
        print("\nДубликаты не найдены!")
        return
    
    print(f"\nНайдено {sum(len(group) for group in duplicates)} дубликатов в {len(duplicates)} группах")
    
    for group in duplicates:
        action = user_select_action(group)
        
        if action is None:  # Пропустить
            continue
        elif not action:    # Удалить все
            for filepath in group:
                try:
                    os.remove(filepath)
                    print(f"Удален: {filepath}")
                except Exception as e:
                    print(f"Ошибка при удалении {filepath}: {e}")
        else:               # Оставить выбранный
            for filepath in group:
                if filepath != action[0]:
                    try:
                        os.remove(filepath)
                        print(f"Удален: {filepath}")
                    except Exception as e:
                        print(f"Ошибка при удалении {filepath}: {e}")
    
    print("\nОперация завершена!")

if __name__ == "__main__":
    main()
    input("Нажмите Enter для выхода...")  # Чтобы окно не закрылось
