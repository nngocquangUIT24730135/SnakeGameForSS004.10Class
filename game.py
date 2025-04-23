import os
import random
import time
from pynput import keyboard
import platform

# Cài đặt trò chơi
SNAKE_CHAR = 'O'
HEAD_CHAR = '1'
FOOD_CHAR = '*'
WALL_CHAR = '#'
EMPTY_CHAR = ' '

WIDTH = 20
HEIGHT = 10

class Snake:
    def __init__(self, body=[(5, 5)], direction=(1, 0)):
        self.body = body           # Khởi tạo thân rắn với vị trí đầu tiên
        self.direction = direction       # Hướng di chuyển ban đầu

    def move(self, food_position):
        # Di chuyển rắn
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        
        # Kiểm tra ăn thức ăn
        if new_head == food_position:
            return True  # Rắn ăn thức ăn, không xóa đuôi
        else:
            self.body.pop()  # Xóa đuôi nếu không ăn
            return False

    def check_collision(self):
        # Kiểm tra va chạm với chính mình hoặc tường
        head = self.body[0]
        return (head in self.body[1:] or
                head[0] < 0 or head[0] >= WIDTH or
                head[1] < 0 or head[1] >= HEIGHT)

class Food:
    def __init__(self, initial_position=(10, 5)):
        self.position = initial_position  # Vị trí thức ăn ban đầu

    def spawn(self, snake_body):
        # Tạo vị trí mới cho thức ăn
        while True:
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
            if (x, y) not in snake_body:
                self.position = (x, y)
                break

class Game:
    def __init__(self):
        self.snake = Snake()  # Khởi tạo rắn
        self.food = Food()  # Khởi tạo thức ăn
        self.score = 0  # Điểm số ban đầu
        self.game_over = False  # Trạng thái kết thúc trò chơi
        self.current_keys = set()  # Lưu trữ trạng thái phím
        self.listener = None  # Listener cho pynput

    @staticmethod
    def clear_screen():
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    def draw_board(self):
        # Vẽ bảng trò chơi
        self.clear_screen()
        print(WALL_CHAR * (WIDTH + 2))  # In tường trên
        for y in range(HEIGHT):
            row = WALL_CHAR  # Bắt đầu hàng với tường
            for x in range(WIDTH):
                if (x, y) == self.snake.body[0]:
                    row += HEAD_CHAR  # Vẽ đầu rắn
                elif (x, y) in self.snake.body:
                    row += SNAKE_CHAR  # Vẽ thân rắn
                elif (x, y) == self.food.position:
                    row += FOOD_CHAR  # Vẽ thức ăn
                else:
                    row += EMPTY_CHAR  # Vẽ ô trống
            row += WALL_CHAR  # Kết thúc hàng với tường
            print(row)
        print(WALL_CHAR * (WIDTH + 2))  # In tường dưới
        print(f"Điểm: {self.score}")  # In điểm số

    def update_state(self):
        # Di chuyển rắn
        ate_food = self.snake.move(self.food.position)

        # Kiểm tra va chạm
        if self.snake.check_collision():
            self.draw_board()  # Hiển thị trạng thái cuối
            time.sleep(3)  # Tạm dừng 3 giây
            self.game_over = True
            return False  # Thoát vòng lặp chính

        # Cập nhật nếu ăn thức ăn
        if ate_food:
            self.score += 1  # Tăng điểm
            self.food.spawn(self.snake.body)  # Tạo thức ăn mới

        return True  # Tiếp tục vòng lặp chính

    def handle_input(self):
        current_dx, current_dy = self.snake.direction
        if 'q' in self.current_keys:
            return False  # Thoát trò chơi
        if 'up' in self.current_keys and current_dy != 1:  # Ngăn di chuyển ngược lại
            self.snake.direction = (0, -1)
        elif 'down' in self.current_keys and current_dy != -1:
            self.snake.direction = (0, 1)
        elif 'left' in self.current_keys and current_dx != 1:
            self.snake.direction = (-1, 0)
        elif 'right' in self.current_keys and current_dx != -1:
            self.snake.direction = (1, 0)
        return True  # Tiếp tục trò chơi

    def on_press(self, key):
        try:
            if key == keyboard.Key.up:
                self.current_keys.add('up')
            elif key == keyboard.Key.down:
                self.current_keys.add('down')
            elif key == keyboard.Key.left:
                self.current_keys.add('left')
            elif key == keyboard.Key.right:
                self.current_keys.add('right')
            elif key == keyboard.KeyCode.from_char('q'):
                self.current_keys.add('q')
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key == keyboard.Key.up:
                self.current_keys.discard('up')
            elif key == keyboard.Key.down:
                self.current_keys.discard('down')
            elif key == keyboard.Key.left:
                self.current_keys.discard('left')
            elif key == keyboard.Key.right:
                self.current_keys.discard('right')
            elif key == keyboard.KeyCode.from_char('q'):
                self.current_keys.discard('q')
        except AttributeError:
            pass

    def start_listener(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def stop_listener(self):
        if self.listener:
            self.listener.stop()

def main():
    game = Game()
    game.start_listener()

    FRAME_RATE = 60
    FRAME_TIME = 1.0 / FRAME_RATE
    last_time = time.perf_counter()

    try:
        while not game.game_over:
            game.draw_board()

            if not game.handle_input():
                break

            if not game.update_state():
                break

            # Delay để giữ FPS ổn định
            now = time.perf_counter()
            elapsed = now - last_time
            if elapsed < FRAME_TIME:
                time.sleep(FRAME_TIME - elapsed)
            last_time = now

    finally:
        game.stop_listener()

    game.clear_screen()
    print("--------------------------------")
    print(f"Trò chơi kết thúc! Điểm cuối: {game.score}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTrò chơi bị dừng.")