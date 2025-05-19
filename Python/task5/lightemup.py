import random
import time
from tkinter import *
from tkinter import messagebox

class Block:
    """Класс, представляющий блок на игровом поле"""
    def __init__(self, x, y, block_type):
        self.x = x
        self.y = y
        self.type = block_type  # 0 - вертикальный, 1 - горизонтальный, 2 - угловой
        self.rotation = 0  # 0, 1, 2, 3 - количество поворотов на 90 градусов
        
    def rotate(self):
        """Поворот блока на 90 градусов"""
        self.rotation = (self.rotation + 1) % 4
        
    def get_connections(self):
        """Возвращает направления, в которых есть соединения"""
        if self.type == 0:  # вертикальный
            if self.rotation % 2 == 0:
                return ['up', 'down']
            else:
                return ['left', 'right']
        elif self.type == 1:  # горизонтальный
            if self.rotation % 2 == 0:
                return ['left', 'right']
            else:
                return ['up', 'down']
        else:  # Угловой
            if self.rotation == 0:
                return ['up', 'right']
            elif self.rotation == 1:
                return ['right', 'down']
            elif self.rotation == 2:
                return ['down', 'left']
            else:
                return ['left', 'up']

class LightEmUpGame:
    def __init__(self, root, size=5):
        self.root = root
        self.size = size
        self.board = [[Block(x, y, random.randint(0, 2)) for x in range(size)] for y in range(size)]
        self.lit_cells = set()
        self.time_left = 120  # 2 минуты в секундах
        self.game_over = False
        self.win = False
        self.start_time = time.time()
        
        # создание интерфейса
        self.setup_ui()
        
        # запуск таймера
        self.update_timer()
        
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        self.root.title("Light'em up!")
        
        # фрейм для игрового поля
        self.game_frame = Frame(self.root)
        self.game_frame.pack(pady=10)
        
        # создание кнопок-блоков
        self.buttons = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                btn = Button(self.game_frame, text='', width=4, height=2,
                            command=lambda x=x, y=y: self.handle_click(x, y))
                btn.grid(row=y, column=x, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)
        
        # таймер
        self.timer_label = Label(self.root, text="Time: 02:00", font=('Arial', 14))
        self.timer_label.pack(pady=5)
        
        # кнопка настроек
        Button(self.root, text="Settings", command=self.show_settings).pack(pady=5)
        
        # обновление отображения
        self.update_board()
    
    def show_settings(self):
        """Показать окно настроек"""
        if self.game_over:
            return
            
        settings = Toplevel(self.root)
        settings.title("Settings")
        
        Label(settings, text="Field Size:").grid(row=0, column=0, padx=5, pady=5)
        
        self.size_var = IntVar(value=self.size)
        Spinbox(settings, from_=5, to=10, textvariable=self.size_var, width=5).grid(row=0, column=1, padx=5, pady=5)
        
        def apply_settings():
            new_size = self.size_var.get()
            if new_size != self.size:
                self.size = new_size
                self.reset_game()
                settings.destroy()
        
        Button(settings, text="Apply", command=apply_settings).grid(row=1, column=0, columnspan=2, pady=5)
    
    def reset_game(self):
        """Сбросить игру с новыми настройками"""
        self.board = [[Block(x, y, random.randint(0, 2)) for x in range(self.size)] for y in range(self.size)]
        self.lit_cells = set()
        self.time_left = 120
        self.game_over = False
        self.win = False
        self.start_time = time.time()
        
        # обновить интерфейс
        self.game_frame.destroy()
        self.setup_ui()
    
    def update_timer(self):
        """Обновление таймера"""
        if self.game_over:
            return
            
        elapsed = time.time() - self.start_time
        self.time_left = max(0, 120 - elapsed)
        
        minutes = int(self.time_left // 60)
        seconds = int(self.time_left % 60)
        self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        
        if self.time_left <= 0:
            self.game_over = True
            self.win = False
            messagebox.showinfo("Game Over", "Time's up! You lose!")
            self.show_solution()
        else:
            self.root.after(1000, self.update_timer)
    
    def handle_click(self, x, y):
        """Обработка клика по блоку"""
        if self.game_over:
            return
            
        self.board[y][x].rotate()
        self.update_game_state()
    
    def update_game_state(self):
        """Обновление состояния игры"""
        self.lit_cells = set()
        queue = [(0, 0)]
        
        while queue:
            x, y = queue.pop()
            if (x, y) in self.lit_cells:
                continue
                
            self.lit_cells.add((x, y))
            block = self.board[y][x]
            connections = block.get_connections()
            
            if 'up' in connections and y > 0:
                neighbor = self.board[y-1][x]
                if 'down' in neighbor.get_connections():
                    queue.append((x, y-1))
            if 'down' in connections and y < self.size - 1:
                neighbor = self.board[y+1][x]
                if 'up' in neighbor.get_connections():
                    queue.append((x, y+1))
            if 'left' in connections and x > 0:
                neighbor = self.board[y][x-1]
                if 'right' in neighbor.get_connections():
                    queue.append((x-1, y))
            if 'right' in connections and x < self.size - 1:
                neighbor = self.board[y][x+1]
                if 'left' in neighbor.get_connections():
                    queue.append((x+1, y))
        
        # проверка победы
        if len(self.lit_cells) == self.size * self.size:
            self.game_over = True
            self.win = True
            messagebox.showinfo("Congratulations!", "You win! All cells are lit!")
        
        self.update_board()
    
    def update_board(self):
        """Обновление отображения игрового поля"""
        for y in range(self.size):
            for x in range(self.size):
                block = self.board[y][x]
                is_lit = (x, y) in self.lit_cells
                
                # определяем символ для отображения в зависимости от типа и поворота блока
                if block.type == 0:  # вертикальный
                    if block.rotation % 2 == 0:
                        text = "║"
                    else:
                        text = "═"
                elif block.type == 1:  # горизонтальный
                    if block.rotation % 2 == 0:
                        text = "═"
                    else:
                        text = "║"
                else:  # угловой
                    if block.rotation == 0:
                        text = "╚"
                    elif block.rotation == 1:
                        text = "╔"
                    elif block.rotation == 2:
                        text = "╗"
                    else:
                        text = "╝"
                
                # устанавливаем текст и цвет кнопки
                self.buttons[y][x].config(text=text)
                if is_lit:
                    self.buttons[y][x].config(bg="yellow")
                else:
                    self.buttons[y][x].config(bg="SystemButtonFace")
    
    def show_solution(self):
        """Показать решение после проигрыша"""
        # временно сохраняем текущее состояние
        temp_board = [[(block.type, block.rotation) for block in row] for row in self.board]
        
        # сбрасываем повороты
        for row in self.board:
            for block in row:
                block.rotation = 0
        
        # ищем правильную комбинацию (упрощенный вариант)
        
        for row in self.board:
            for block in row:
                for _ in range(4):
                    self.update_game_state()
                    if len(self.lit_cells) == self.size * self.size:
                        return
                    block.rotate()
        
        # если решение не найдено, восстанавливаем исходное состояние
        for y in range(self.size):
            for x in range(self.size):
                self.board[y][x].type, self.board[y][x].rotation = temp_board[y][x]
        self.update_game_state()

def main():
    root = Tk()
    game = LightEmUpGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
