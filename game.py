import os
import time
import random

# Cài đặt trò chơi
SNAKE_CHAR = 'O'
HEAD_CHAR = '1'
EMPTY_CHAR = ' '

class Snake:
    def __init__(self, body=[(5, 5)], direction=(1, 0)):
        self.body = body           # Khởi tạo thân rắn với vị trí đầu tiên
        self.direction = direction       # Hướng di chuyển ban đầu

    #TODO: Hiện thực hoá hàm di chuyển con rắn
    def move(self, food_position):
        # Di chuyển rắn
        
        # Kiểm tra ăn thức ăn
        return True

    #TODO: Hiện thực hoá hàm kiểm tra va chạm
    def check_collision(self):
        # Kiểm tra va chạm với chính mình hoặc tường
        return True
    
def main():
    # Tạo một con rắn với đối số mặc định
    snake = Snake()
    print("Rắn 1 - Vị trí khởi tạo:", snake.body)
    print("Rắn 1 - Hướng di chuyển:", snake.direction)

    # Kiểm tra thông tin về kiểu dữ liệu
    print("\n[Kiểu dữ liệu]")
    print("Kiểu snake.body:", type(snake.body))           # <class 'list'>
    print("Kiểu phần tử đầu trong body:", type(snake.body[0]))  # <class 'tuple'>
    print("Kiểu direction:", type(snake.direction))       # <class 'tuple'>

    # Tạo con rắn thứ 2 có độ dài là 3 và hướng di chuyển sang trái
    snake2 = Snake([(5,5), (5,6), (5,7)], (-1, 0))
    print("\nRắn 2 - Vị trí khởi tạo:", snake2.body)
    print("Rắn 2 - Hướng di chuyển:", snake2.direction)

    # Lấy đầu con rắn
    print("Rắn 2 - Vị trí đầu rắn:", snake2.body[0])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTrò chơi bị dừng.")