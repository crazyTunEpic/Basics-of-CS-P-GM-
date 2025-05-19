import pytest
import csv
import os
from datetime import datetime, timedelta
from main import read_data_from_file, calculate_statistics
from split_module import split_data
import statistics

# Тестовые данные
TEST_DATA = [
    (datetime(2023, 1, 1, 0, 0), 10.5),
    (datetime(2023, 1, 1, 0, 15), 15.2),
    (datetime(2023, 1, 1, 0, 30), 12.8),
    (datetime(2023, 1, 1, 0, 45), 10.5),
    (datetime(2023, 1, 1, 1, 0), 18.3),
    (datetime(2023, 1, 1, 1, 15), 15.2),
]

# Фикстуры для тестов
@pytest.fixture
def create_test_csv(tmp_path):
    def _create_test_csv(filename, data):
        file_path = tmp_path / filename
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)
        return file_path
    return _create_test_csv

@pytest.fixture
def create_invalid_csv(tmp_path):
    file_path = tmp_path / "invalid.csv"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("This is not a CSV file")
    return file_path

# Тесты
def test_read_nonexistent_file():
    """Тест на отсутствие файла"""
    with pytest.raises(FileNotFoundError):
        read_data_from_file("nonexistent_file.csv")

def test_read_file_without_permission(tmp_path):
    """Тест на файл без прав на чтение"""
    file_path = tmp_path / "no_permission.csv"
    file_path.touch(mode=0o000)  # Создаем файл без прав на чтение
    with pytest.raises(PermissionError):
        read_data_from_file(str(file_path))
    file_path.chmod(0o644)  # Восстанавливаем права для удаления файла

def test_read_invalid_csv(create_invalid_csv):
    """Тест на не-CSV файл"""
    with pytest.raises(csv.Error):
        read_data_from_file(str(create_invalid_csv))

def test_read_csv_with_missing_columns(create_test_csv):
    """Тест на строку с одной колонкой"""
    test_data = [
        ["2023-01-01 00:00:00", "10.5"],
        ["2023-01-01 00:15:00"],  # Пропущено значение
        ["2023-01-01 00:30:00", "12.8"],
    ]
    file_path = create_test_csv("missing_columns.csv", test_data)
    data = read_data_from_file(str(file_path))
    assert len(data) == 2  # Должны прочитаться только 2 корректные строки

def test_read_csv_with_invalid_data_types(create_test_csv):
    """Тест на неверные типы данных"""
    test_data = [
        ["2023-01-01 00:00:00", "10.5"],
        ["invalid_date", "15.2"],  # Неверный формат даты
        ["2023-01-01 00:30:00", "not_a_number"],  # Не число
    ]
    file_path = create_test_csv("invalid_types.csv", test_data)
    data = read_data_from_file(str(file_path))
    assert len(data) == 1  # Должна прочитаться только 1 корректная строка

def test_split_data_intervals():
    """Тест на правильность разбиения по интервалам"""
    interval = 30  # 30 минут
    segments = split_data(TEST_DATA, interval)
    
    # Должно получиться 3 интервала:
    # 0:00-0:30, 0:30-1:00, 1:00-1:30
    assert len(segments) == 3
    
    # Проверяем количество точек в каждом интервале
    assert len(segments[0]) == 2  # 0:00 и 0:15
    assert len(segments[1]) == 2  # 0:30 и 0:45
    assert len(segments[2]) == 2  # 1:00 и 1:15

def test_calculate_statistics():
    """Тест на правильность расчета статистик"""
    stats = calculate_statistics(TEST_DATA[:4])  # Первые 4 значения
    
    assert stats['count'] == 4
    assert stats['mean'] == pytest.approx((10.5 + 15.2 + 12.8 + 10.5) / 4)
    assert stats['mode'] == 10.5  # 10.5 встречается дважды
    assert stats['median'] == pytest.approx((10.5 + 12.8) / 2)

# Дополнительные тесты (3 штуки)
def test_empty_file(create_test_csv):
    """Тест на пустой файл"""
    file_path = create_test_csv("empty.csv", [])
    data = read_data_from_file(str(file_path))
    assert len(data) == 0

def test_split_empty_data():
    """Тест на разбиение пустых данных"""
    segments = split_data([], 30)
    assert len(segments) == 0

def test_statistics_with_single_value():
    """Тест статистик с одним значением"""
    single_data = [(datetime(2023, 1, 1, 0, 0), 10.5)]
    stats = calculate_statistics(single_data)
    
    assert stats['count'] == 1
    assert stats['mean'] == 10.5
    assert stats['mode'] is None  # Не может быть моды для одного значения
    assert stats['median'] == 10.5
