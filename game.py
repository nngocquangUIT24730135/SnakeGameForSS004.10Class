import os
import random
import time
import keyboard

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

    @staticmethod
    def clear_screen():
        # Xóa màn hình console
        os.system('cls' if os.name == 'nt' else 'clear')

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
        if keyboard.is_pressed('q'):
            self.last_key = "q"
            return False  # Thoát trò chơi
        current_dx, current_dy = self.snake.direction
        if keyboard.is_pressed('up') and current_dy != 1:  # Ngăn di chuyển ngược lại
            self.snake.direction = (0, -1)
            self.last_key = "up"
        elif keyboard.is_pressed('down') and current_dy != -1:
            self.snake.direction = (0, 1)
            self.last_key = "down"
        elif keyboard.is_pressed('left') and current_dx != 1:
            self.snake.direction = (-1, 0)
            self.last_key = "left"
        elif keyboard.is_pressed('right') and current_dx != -1:
            self.snake.direction = (1, 0)
            self.last_key = "right"
        return True  # Tiếp tục trò chơi

def main():
    game = Game()  # Khởi tạo trạng thái trò chơi
    
    while not game.game_over:
        game.draw_board()  # Vẽ bảng trò chơi

        # Xử lý đầu vào
        if not game.handle_input():
            break

        # Cập nhật trạng thái trò chơi
        if not game.update_state():
            break

        time.sleep(0.2) # Tạm dừng 0.2 giây

    game.clear_screen()
    print("--------------------------------")
    print(f"Trò chơi kết thúc! Điểm cuối: {game.score}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTrò chơi bị dừng.")
