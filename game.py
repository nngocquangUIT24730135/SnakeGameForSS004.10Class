import random

WIDTH = 20
HEIGHT = 10
FOOD_CHAR = '*'

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

def main():
    food = Food()
    print(food.position)

    body = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9)]
    food.spawn(body)
    print(food.position)
    for i in range(1, 10001):
        food.spawn(body)
        if (food.position in body):
            # dòng dưới đây không bao giờ được in ra màn hình
            print("Thức ăn không thể xuất hiện trong thân con rắn")
            break;
    print(food.position)

if __name__ == "__main__":
    main()