import os
import random

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

    #TODO Hiện thực hoá hàm vẽ khung trò chơi dưới đây
    def draw_board(self):
        # Vẽ bảng trò chơi
        self.clear_screen()
        print("ĐÂY LÀ MÀN HÌNH TRÒ CHƠI")

    #TODO Hiện thực hoá update trạng thái trò chơi sau khi di chuyển con rắn dưới dây
    def update_state(self):
        # Cập nhật trạng thái trò chơi
        return True  # Tiếp tục vòng lặp chính

    #TODO Hiện thực hoá hàm xử lý khi người chơi ấn các phím
    def handle_input(self):
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


    game.clear_screen()
    print("--------------------------------")
    print(f"Trò chơi kết thúc! Điểm cuối: {state.score}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTrò chơi bị dừng.")