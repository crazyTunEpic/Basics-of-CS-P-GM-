import sys
import csv
import statistics
from datetime import datetime, timedelta
from split_module import split_data  # импорт

def read_data_from_file(filename):
    """Чтение данных из CSV-файла"""
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:  # проверяем, что в строке есть хотя бы 2 столбца
                try:
                    timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                    value = float(row[1])
                    data.append((timestamp, value))
                except (ValueError, IndexError):
                    continue  # пропускаем некорректные строки
    return data

def calculate_statistics(data_segment):
    """Вычисление статистик для сегмента данных"""
    if not data_segment:
        return None
    
    timestamps = [item[0] for item in data_segment]
    values = [item[1] for item in data_segment]
    
    stats = {
        'start': min(timestamps),
        'end': max(timestamps),
        'count': len(values),
        'mean': statistics.mean(values),
    }
    
    try:
        stats['mode'] = statistics.mode(values)
    except statistics.StatisticsError:
        stats['mode'] = None
    
    try:
        stats['median'] = statistics.median(values)
    except statistics.StatisticsError:
        stats['median'] = None
    
    return stats

def print_statistics(statistics_list):
    """Вывод статистик на экран"""
    for stats in statistics_list:
        if stats is None:
            continue
        
        print(f"\nОтрезок с {stats['start']} по {stats['end']}:")
        print(f"  Количество значений: {stats['count']}")
        print(f"  Среднее значение: {stats['mean']:.2f}")
        if stats['mode'] is not None:
            print(f"  Мода: {stats['mode']:.2f}")
        else:
            print("  Мода: не определена (все значения уникальны)")
        if stats['median'] is not None:
            print(f"  Медиана: {stats['median']:.2f}")

def main():
    if len(sys.argv) < 3:
        print("Использование: python main.py <файл.csv> <интервал_в_минутах>")
        sys.exit(1)
    
    filename = sys.argv[1]
    try:
        interval = int(sys.argv[2])
    except ValueError:
        print("Ошибка: интервал должен быть целым числом (минуты)")
        sys.exit(1)
    
    try:
        # чтение данных из файла
        data = read_data_from_file(filename)
        if not data:
            print("Файл не содержит данных или имеет неправильный формат")
            return
        
        # разбиение данных на отрезки
        segments = split_data(data, interval)
        
        # расчет статистик для каждого отрезка
        statistics_list = []
        for segment in segments:
            stats = calculate_statistics(segment)
            statistics_list.append(stats)
        
        # вывод результатов
        print_statistics(statistics_list)
        
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main()
