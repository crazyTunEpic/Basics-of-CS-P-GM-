from datetime import datetime, timedelta

def split_data(data, interval_minutes):
    """Разбивает данные на временные отрезки заданной длины"""
    if not data:
        return []
    
    # сортируем данные по времени (на всякий случай)
    data.sort(key=lambda x: x[0])
    
    segments = []
    current_segment = []
    start_time = data[0][0]
    interval = timedelta(minutes=interval_minutes)
    
    for timestamp, value in data:
        # если время выходит за текущий интервал, создаем новый сегмент
        if timestamp >= start_time + interval:
            if current_segment:
                segments.append(current_segment)
                current_segment = []
            start_time = timestamp - timedelta(
                minutes=(timestamp - start_time).total_seconds() // 60 % interval_minutes
            )
        
        current_segment.append((timestamp, value))
    
    # добавляем последний сегмент
    if current_segment:
        segments.append(current_segment)
    
    return segments
