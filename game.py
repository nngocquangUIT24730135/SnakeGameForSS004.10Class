import curses
import random
import time

WIDTH = 20
HEIGHT = 10

SNAKE_CHAR = 'O'
HEAD_CHAR = 'X'
FOOD_CHAR = '*'
WALL_CHAR = '#'

DIRECTIONS = {
    curses.KEY_UP: (0, -1),
    curses.KEY_DOWN: (0, 1),
    curses.KEY_LEFT: (-1, 0),
    curses.KEY_RIGHT: (1, 0),
}

class Snake:
    def __init__(self, body=[(5, 5)], direction=(1, 0)):
        self.body = body
        self.direction = direction

    def move(self, food_pos):
        dx, dy = self.direction
        head_x, head_y = self.body[0]
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)

        if new_head == food_pos:
            return True
        else:
            self.body.pop()
            return False

    def check_collision(self):
        head = self.body[0]
        return (head in self.body[1:] or
                head[0] < 0 or head[0] >= WIDTH or
                head[1] < 0 or head[1] >= HEIGHT)

class Food:
    def __init__(self):
        self.position = (10, 5)

    def spawn(self, snake_body):
        while True:
            pos = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            if pos not in snake_body:
                self.position = pos
                break

def draw_borders(stdscr, start_x, start_y):
    for y in range(HEIGHT + 2):
        for x in range(WIDTH + 2):
            if y == 0 or y == HEIGHT + 1 or x == 0 or x == WIDTH + 1:
                stdscr.addstr(start_y + y, start_x + x * 2, WALL_CHAR * 2)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    snake = Snake()
    food = Food()
    score = 0

    # Starting position for the board
    start_x = 2
    start_y = 1

    while True:
        key = stdscr.getch()
        if key in DIRECTIONS:
            new_dir = DIRECTIONS[key]
            if (new_dir[0] != -snake.direction[0] or new_dir[1] != -snake.direction[1]):
                snake.direction = new_dir
        elif key == ord('q'):
            break

        ate = snake.move(food.position)

        if snake.check_collision():
            break

        if ate:
            score += 1
            food.spawn(snake.body)

        stdscr.clear()
        draw_borders(stdscr, start_x, start_y)

        # Draw snake and food inside border
        for y in range(HEIGHT):
            for x in range(WIDTH):
                draw_x = start_x + (x + 1) * 2
                draw_y = start_y + (y + 1)
                if (x, y) == snake.body[0]:
                    stdscr.addstr(draw_y, draw_x, HEAD_CHAR)
                elif (x, y) in snake.body:
                    stdscr.addstr(draw_y, draw_x, SNAKE_CHAR)
                elif (x, y) == food.position:
                    stdscr.addstr(draw_y, draw_x, FOOD_CHAR)

        stdscr.addstr(start_y + HEIGHT + 3, start_x, f"Điểm: {score}  (Nhấn 'q' để thoát)")
        stdscr.refresh()

    stdscr.clear()
    stdscr.addstr(HEIGHT // 2, WIDTH, f"Trò chơi kết thúc! Điểm: {score}")
    stdscr.refresh()
    time.sleep(2)

if __name__ == "__main__":
    curses.wrapper(main)
