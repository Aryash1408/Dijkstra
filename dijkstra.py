from tkinter import *
import pygame
import math
from queue import PriorityQueue
import random

WIDTH = 800
Height = 800

def get():
    root1.destroy()

root1 = Tk()
root1.geometry("1000x700")
root1.title('Guide')

label_0 = Label(root1, text="Path Finder ", width=20, font=("bold", 40))
label_0.place(x=200, y=40)

label_5 = Label(root1, text="Quick Guide", width=20, font=(20))
label_5.place(x=380, y=110)

label_1 = Label(root1, text="Controls", width=20, font=(20))
label_1.place(x=380, y=150)

label_3 = Label(root1, text="1. After Reaching the board, Select Starting and Ending Node by Left Click of the Mouse.\n", font=(10))
label_3.place(x=50, y=220)

label_4 = Label(root1, text="2. Once selecting those 2 points, one can select any Node as an obstacle apart from Start and End Node.\n", font=(10))
label_4.place(x=50, y=300)

label_5 = Label(root1, text="3. To Start The Algorithm, Press Space Bar!!!!.\n", font=(10))
label_5.place(x=50, y=340)

label_6 = Label(root1, text="4. One Can Rerun the same Algorithm using the same Space Bar (Only after execution of the Algorithm).\n", font=(10))
label_6.place(x=50, y=380)

Button(root1, text='Skip Guide...', font=(20), width=20, bg="black", fg='white', command=get).place(x=380, y=580)

root1.mainloop()

root = Tk()
root.geometry("500x500")
root.title('Path Finder')


yel = (242, 227, 7)
bl = (112, 205, 226)
blu = (0, 172, 205)
RED = (190, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (181, 181, 22)
WHITE = (255, 255, 255)
BLACK = (60, 60, 60)
PURPLE = (128, 0, 128)
ORANGE = (201, 103, 170)
GREY = (128, 128, 128)
TURQUOISE = (15, 135, 0)

class Spot:
    def __init__(self, row, col, gap, gap1, width, height, total_rows, total_cols, diag):
        self.row = row
        self.col = col
        self.x = row * gap
        self.y = col * gap1
        self.color = WHITE
        self.neighbors = []
        self.diag = diag
        self.height = height
        self.width = width
        self.total_rows = total_rows
        self.total_cols = total_cols

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == RED

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = RED

    def make_closed(self):
        self.color = blu

    def make_open(self):
        self.color = bl

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = yel

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.y, self.x, self.width, self.height))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def reconstruct_path(came_from, current, draw, temp):
    count = 0
    t1 = current
    while current in came_from:
        count += 1
        current = came_from[current]
        if current != temp:
            current.make_path()
            draw()
    print("Shortest Path Found Is of Distance", count)


def algorithm(Algorithm, draw, grid, start, end, diag):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    current = 0
    temp = start
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]

        if current == end:
            print("Total Nodes Explored by The Algorithm  = ", len(came_from))
            reconstruct_path(came_from, end, draw, temp)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set.queue:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    print("Algorithm Failed!!")
    return False


def make_grid(cols, rows, width, height, diag):
    grid = []
    gap = height // rows
    col = width // cols

    for i in range(rows):
        grid.append([])
        for j in range(cols):
            spot = Spot(i, j, gap, col, width, height, rows, cols, diag)
            grid[i].append(spot)

    return grid


def draw_grid(win, cols, rows, width, height):
    col = width // cols
    gap = height // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(cols):
            pygame.draw.line(win, GREY, (j * col, 0), (j * col, height))


def draw(win, cols, grid, rows, width, height):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, cols, rows, width, height)
    pygame.display.update()


def get_clicked_pos(pos, rows, cols, width, height):
    gap = height // rows
    col1 = width // cols
    y, x = pos

    col = y // gap
    row = x // col1

    return row, col


def main(Algorithm):
    WIN = pygame.display.set_mode((WIDTH, Height))
    pygame.display.set_caption(f"{Algorithm} - Pathfinding Algorithm")
    win = WIN
    width = WIDTH
    height = Height
    ROWS = 25
    cols = 25
    grid = make_grid(cols, ROWS, width, height, "no")
    start = None
    end = None
    run = True

    while run:
        draw(win, cols, grid, ROWS, width, height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: 
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, cols, width, height)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, cols, width, height)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(Algorithm, lambda: draw(win, cols, grid, ROWS, width, height), grid, start, end, "no")

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(cols, ROWS, width, height, "no")

    pygame.quit()


if __name__ == "__main__":
    main("Dijikstra's")
