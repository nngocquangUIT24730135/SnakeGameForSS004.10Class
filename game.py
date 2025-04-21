import os
import time
import msvcrt
import sys

# Hàm di chuyển con trỏ console (thay thế gotoxy)
def gotoxy(x, y):
    print(f"\033[{y};{x}H", end='')

# Lớp Point để lưu tọa độ
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Lớp CONRAN
class CONRAN:
    def __init__(self):
        self.DoDai = 3
        self.A = [Point(10, 10), Point(11, 10), Point(12, 10)]  # Khởi tạo rắn với 3 điểm

    def Ve(self):
        # Xóa màn hình
        os.system('cls' if os.name == 'nt' else 'clear')
        # Vẽ rắn
        for i in range(self.DoDai):
            gotoxy(self.A[i].x, self.A[i].y)
            print('X', end='')
        sys.stdout.flush()

    def DiChuyen(self, Huong):
        # Di chuyển các điểm của rắn
        for i in range(self.DoDai - 1, 0, -1):
            self.A[i].x = self.A[i - 1].x
            self.A[i].y = self.A[i - 1].y
        # Cập nhật đầu rắn theo hướng
        if Huong == 0:  # Phải
            self.A[0].x += 1
        elif Huong == 1:  # Xuống
            self.A[0].y += 1
        elif Huong == 2:  # Trái
            self.A[0].x -= 1
        elif Huong == 3:  # Lên
            self.A[0].y -= 1

def main():
    r = CONRAN()
    Huong = 0  # Hướng ban đầu: 0 (phải), 1 (xuống), 2 (trái), 3 (lên)

    while True:
        # Kiểm tra đầu vào từ bàn phím
        if msvcrt.kbhit():
            t = msvcrt.getch().decode('utf-8').lower()
            if t == 'a':
                Huong = 2
            elif t == 'w':
                Huong = 3
            elif t == 'd':
                Huong = 0
            elif t == 's':
                Huong = 1

        r.Ve()
        r.DiChuyen(Huong)
        time.sleep(0.3)  # Tạm dừng 300ms

if __name__ == "__main__":
    main()