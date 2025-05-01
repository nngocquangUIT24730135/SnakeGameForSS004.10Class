import os
import random
import time
import platform
from pynput import keyboard
import pygame
import sys 

# Khởi tạo pygame
pygame.init()

title_font = pygame.font.Font(None, 40)
score_font = pygame.font.Font(None, 40)
popup_font = pygame.font.Font(None, 40)

GREEN = (80, 200, 120)
DARK_GREEN = (6, 64, 43)
HEAD_COLOR = (45, 104, 196)

cell_size = 30
number_of_cells = 15
WIDTH = number_of_cells
HEIGHT = number_of_cells

OFFSET = 75
eat_sound = pygame.mixer.Sound("Sounds/eat.mp3")
wall_hit_sound = pygame.mixer.Sound("Sounds/wall.mp3")
food_surface = pygame.image.load("Graphics/food.png")
SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)
screen = pygame.display.set_mode((2*OFFSET + cell_size*number_of_cells, 2*OFFSET + cell_size*number_of_cells))
pygame.display.set_caption("Snake loves money")
clock = pygame.time.Clock() 

# Thông số tốc độ
FRAME_RATE = 30
FRAME_TIME = 1.0 / FRAME_RATE
MOVES_PER_SECOND = 5
FRAMES_PER_MOVE = FRAME_RATE // MOVES_PER_SECOND  # Số khung hình giữa các lần di chuyển của rắn

class Snake:
    def __init__(self, body=[(5, 5)], direction=(1, 0)):
        self.body = body           # Khởi tạo thân rắn với vị trí đầu tiên
        self.direction = direction       # Hướng di chuyển ban đầu

    def draw(self):
        #TODO: viết hàm vẽ con rắn trên canvas
        return None;

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

    def draw(self):
        #TODO: viết hàm vẽ đồ ăn trên canvas
        return None

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
        self.frame_count = 0  # Đếm số khung hình để kiểm soát di chuyển

    @staticmethod
    def clear_screen():
        # Xóa màn hình console
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    def draw_board(self):
        screen.fill(GREEN)
        pygame.draw.rect(screen, DARK_GREEN, 
            (OFFSET-5, OFFSET-5, cell_size*number_of_cells + 10, cell_size*number_of_cells + 10), 5)
        self.snake.draw()
        self.food.draw()
        title_surface = title_font.render("Snake loves money", True, DARK_GREEN)
        score_surface = score_font.render(str(self.score), True, DARK_GREEN)
        screen.blit(title_surface, (OFFSET-5, 20))
        screen.blit(score_surface, (OFFSET-5, OFFSET + cell_size*number_of_cells + 10))
        
        if self.state == "STOPPED":
            self.draw_popup()
        
        pygame.display.update()
        clock.tick(60)
    
    def update_state(self):
        # Cập nhật trạng thái trò chơi
        self.frame_count += 1
        if self.frame_count >= FRAMES_PER_MOVE:
            self.frame_count = 0  # Reset bộ đếm
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

    def handle_input(self, event):
        #TODO: cần được implement lại
        return None

    def on_press(self, key):
        # Xử lý sự kiện nhấn phím
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
        # Xử lý sự kiện thả phím
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
        # Bắt đầu lắng nghe sự kiện phím
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def stop_listener(self):
        # Dừng lắng nghe sự kiện phím
        if self.listener:
            self.listener.stop()

def main():
    game = Game()  # Khởi tạo trạng thái trò chơi
    
    while True:
        game.draw_board()  # Vẽ bảng trò chơi
        for event in pygame.event.get():
            if event.type == SNAKE_UPDATE:
                game.update_state()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Xử lý đầu vào
            game.handle_input(event)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTrò chơi bị dừng.")