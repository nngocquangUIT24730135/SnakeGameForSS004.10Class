
import random
import pygame
import sys 

# Khởi tạo pygame
pygame.init()

TITLE_FONT = pygame.font.Font(None, 40)
SCORE_FONT = pygame.font.Font(None, 40)
POPUP_FONT = pygame.font.Font(None, 40)

GREEN = (80, 200, 120)
DARK_GREEN = (6, 64, 43)
HEAD_COLOR = (45, 104, 196)

CELL_SIZE = 30
NUMBER_OF_CELLS = 15
WIDTH = NUMBER_OF_CELLS
HEIGHT = NUMBER_OF_CELLS

OFFSET = 75
EAT_SOUND = pygame.mixer.Sound("Sounds/eat.mp3")
WALL_HIT_SOUND = pygame.mixer.Sound("Sounds/wall.mp3")
FOOD_SURFACE = pygame.image.load("Graphics/food.png")
SNAKE_UPDATE = pygame.USEREVENT

pygame.time.set_timer(SNAKE_UPDATE, 200)
screen = pygame.display.set_mode((2*OFFSET + CELL_SIZE*NUMBER_OF_CELLS, 2*OFFSET + CELL_SIZE*NUMBER_OF_CELLS))
pygame.display.set_caption("Snake loves money")
clock = pygame.time.Clock() 

class Snake:
    def __init__(self, body=[(6, 9), (5, 9), (4, 9)], direction=(1, 0)):
        self.body = body           # Khởi tạo thân rắn với vị trí đầu tiên
        self.direction = direction # Hướng di chuyển ban đầu

    def reset(self):
        self.body = [(6, 9), (5, 9), (4, 9)]
        self.direction = (1, 0)

    def draw(self):
        for index, segment in enumerate(self.body):
            x, y = segment
            segment_rect = (OFFSET + x * CELL_SIZE, OFFSET+ y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = HEAD_COLOR if index == 0 else DARK_GREEN
            pygame.draw.rect(screen, color, segment_rect, 0, 7)

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
        x, y = self.position
        food_rect = pygame.Rect(OFFSET + x * CELL_SIZE, OFFSET + y * CELL_SIZE, 
            CELL_SIZE, CELL_SIZE)
        screen.blit(FOOD_SURFACE, food_rect)

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
        self.state = "STOPPED"  # Trạng thái trò chơi 
        self.game_started = False                    

    def game_over(self):
        self.snake.reset()
        self.food.spawn(self.snake.body)
        self.state = "STOPPED"
        WALL_HIT_SOUND.play()
        
    def draw_popup(self):
        # Tính toán kích thước cửa sổ bật lên
        window_size = 2 * OFFSET + CELL_SIZE * NUMBER_OF_CELLS
        popup_width = int(window_size * 2 / 3)  # ~600 pixels
        popup_height = int(window_size * 0.35)  # ~315 pixels

        # Lớp phủ bán trong suốt
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        # Nền cửa sổ bật lên
        popup_rect = pygame.Rect(
            (window_size - popup_width) // 2,
            (window_size - popup_height) // 2,
            popup_width,
            popup_height
        )
        pygame.draw.rect(screen, GREEN, popup_rect, 0, 10)
        pygame.draw.rect(screen, DARK_GREEN, popup_rect, 5, 10)

        # Văn bản dựa trên trạng thái trò chơi
        if not self.game_started:
            # Màn hình bắt đầu ban đầu
            start_text = POPUP_FONT.render("Press SPACE to Start", True, DARK_GREEN)
            start_rect = start_text.get_rect(center=(window_size // 2, window_size // 2))
            screen.blit(start_text, start_rect)
        else:
            # Màn hình Kết thúc trò chơi
            game_over_text = POPUP_FONT.render("Game Over", True, DARK_GREEN)
            score_text = POPUP_FONT.render(f"Score: {self.score}", True, DARK_GREEN)
            play_again_text = POPUP_FONT.render("Press SPACE to Play Again", True, DARK_GREEN)

            game_over_rect = game_over_text.get_rect(center=(window_size // 2, window_size // 2 - 2 * CELL_SIZE))
            score_rect = score_text.get_rect(center=(window_size // 2, window_size // 2))
            play_again_rect = play_again_text.get_rect(center=(window_size // 2, window_size // 2 + 2 * CELL_SIZE))

            screen.blit(game_over_text, game_over_rect)
            screen.blit(score_text, score_rect)
            screen.blit(play_again_text, play_again_rect)

    def draw_board(self):
        screen.fill(GREEN)
        pygame.draw.rect(screen, DARK_GREEN, 
            (OFFSET-5, OFFSET-5, CELL_SIZE*NUMBER_OF_CELLS + 10, CELL_SIZE*NUMBER_OF_CELLS + 10), 5)
        self.snake.draw()
        self.food.draw()
        title_surface = TITLE_FONT.render("Snake loves money", True, DARK_GREEN)
        score_surface = SCORE_FONT.render(str(self.score), True, DARK_GREEN)
        screen.blit(title_surface, (OFFSET-5, 20))
        screen.blit(score_surface, (OFFSET-5, OFFSET + CELL_SIZE*NUMBER_OF_CELLS + 10))
        
        if self.state == "STOPPED":
            self.draw_popup()
        
        pygame.display.update()
        clock.tick(60)
    
    def update_state(self):
        if self.state == "STOPPED":
            return None
        
        # Di chuyển rắn
        ate_food = self.snake.move(self.food.position)

        # Kiểm tra va chạm
        if self.snake.check_collision():
            self.draw_board()  
            self.game_over()

        # Cập nhật nếu ăn thức ăn
        if ate_food:
            EAT_SOUND.play() # âm thanh
            self.score += 1  # Tăng điểm
            self.food.spawn(self.snake.body)  # Tạo thức ăn mới

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "STOPPED" and event.key == pygame.K_SPACE:
                self.state = "RUNNING"
                self.game_started = True  # Đánh dấu trò chơi đã bắt đầu
                self.score = 0  # Đặt lại điểm số khi bắt đầu trò chơi mới
            if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                self.snake.direction = (0, -1)
            if event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                self.snake.direction = (0, 1)
            if event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                self.snake.direction = (-1, 0)
            if event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                self.snake.direction = (1, 0)

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
