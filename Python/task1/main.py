class Robot:
    def __init__(self):
        self.position = [1, 1]  # начальная позиция
        self.history = []  # история перемещений

    def move(self, direction: str, steps: int) -> None:
        if steps < 0:
            raise ValueError("Количество шагов не может быть отрицательным.")
        
        # сохранение позиции перед началом движения
        self.history.append(tuple(self.position))
        
        # перемещение
        if direction == 'R':  
            self.position[0] += steps
        elif direction == 'L':  
            self.position[0] -= steps
        elif direction == 'U':  
            self.position[1] -= steps
        elif direction == 'D':  
            self.position[1] += steps
        else:
            raise ValueError("Недопустимое направление.")
        
        # проверка выхода за границы поля
        if not (1 <= self.position[0] <= 100 and 1 <= self.position[1] <= 100):
            raise ValueError("Выход за границы поля.")

    def back(self, steps_back: int) -> None:
        if steps_back > len(self.history):
            raise ValueError("Количество шагов назад превышает количество шагов из истории.")
        
        self.position = list(self.history[-steps_back]) #  переход на предыдущую позицию
        self.history = self.history[:-steps_back]  # обновление истории перемещений

    def get_position(self) -> tuple[int, int]:
        return tuple(self.position)  # возврат текущей позиции

def main() -> None:
    robot = Robot()
    while True:
        command = input("Введите команду (Например, R,1) или exit для завершения: ").strip()
        
        if command.lower() == 'exit':
            break

        try:
            direction_steps = command.split(',')
            if len(direction_steps) != 2:
                raise ValueError("Команда должна содержать направление и количество шагов, разделенное запятой.")

            direction, steps = direction_steps
            steps = int(steps)

            if direction == 'B':
                robot.back(steps)
            else:
                robot.move(direction, steps)  

            print(f"Текущая позиция робота: {robot.get_position()}")  

        except Exception as e:
            print(f"Ошибка: {e}")  

if __name__ == "__main__":
    main()  # запуск функции main
