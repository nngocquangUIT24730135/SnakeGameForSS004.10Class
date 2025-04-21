import os
import time
import keyboard
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
    print(snake.body)
    print(snake.direction)

    # Kiểm tra thông tin về kiểu dữ liệu
    print(type(snake.body))  # <class 'list'
    print(type(snake.body[0])) # <class 'tuple'>
    print(type(snake.direction)) # <class 'tuple'>

    # Tạo con rắn thứ 2 có độ dài là 3 và hướng di chuyển sang trái
    snake2 = Snake([(5,5), (5,6), (5,7)], (-1, 0))
    print(snake2.body)
    print(snake2.direction)
    # lấy đầu con rắn
    print(snake2.body[0])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTrò chơi bị dừng.")