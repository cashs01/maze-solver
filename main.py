from tkinter import Tk, BOTH, Canvas
import time
import random


class Window():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Maze Solver")
        self.canvas = Canvas(self.root, width=width, height=height, bg="black")
        self.canvas.pack()
        self.running = False

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line, color):
        line.draw(self.canvas, color)


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, color):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=color, width=2)


class Cell():
    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = window
        self.visited = False

    def draw(self, x1, x2, y1, y2):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        if self.__win is None:
            return
        if self.has_left_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "white")
        else:
            self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "black")
        if self.has_right_wall:
            self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "white")
        else:
            self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "black")
        if self.has_top_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "white")
        else:
            self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "black")
        if self.has_bottom_wall:
            self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "white")
        else:
            self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "black")

    def draw_move(self, to_cell, undo=False):
        if not undo:
            color = "red"
        else:
            color = "gray"
        if self.__win is None:
            return
        self.__win.draw_line(Line(Point((self.__x1 + self.__x2) // 2,
                                    (self.__y1 + self.__y2) // 2),
                                    Point((to_cell.__x1 + to_cell.__x2) // 2,
                                    (to_cell.__y1 + to_cell.__y2) // 2)),
                                    color)


class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        if seed is not None:
            random.seed(seed)
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)

    def __create_cells(self):
        for i in range(self.__num_cols):
            col_cells = []
            for j in range(self.__num_rows):
                cell = Cell(self.__win)
                col_cells.append(cell)
            self.__cells.append(col_cells)

        if self.__win is not None:
            for i in range(self.__num_cols):
                for j in range(self.__num_rows):
                    self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        if self.__win is None:
            return
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        self.__cells[i][j].draw(x1, x2, y1, y2)
        self.__animate()

    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.02)

    def __break_entrance_and_exit(self):
        top_left_cell = self.__cells[0][0]
        bottom_right_cell = self.__cells[self.__num_cols - 1][self.__num_rows - 1]
        top_left_cell.has_top_wall = False
        self.__draw_cell(0, 0)
        bottom_right_cell.has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            possible_directions = []
            # Up
            if j > 0:
                if not self.__cells[i][j - 1].visited:
                    possible_directions.append((i, j - 1))
            # Down
            if j < self.__num_rows - 1:
                if not self.__cells[i][j + 1].visited:
                    possible_directions.append((i, j + 1))
            # Left
            if i > 0:
                if not self.__cells[i - 1][j].visited:
                    possible_directions.append((i - 1, j))
            # Right
            if i < self.__num_cols - 1:
                if not self.__cells[i + 1][j].visited:
                    possible_directions.append((i + 1, j))

            if len(possible_directions) == 0:
                return

            direction = random.choice(possible_directions)

            # Remove wall between cells
            if direction[0] == i and direction[1] == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__draw_cell(i, j)
                self.__cells[direction[0]][direction[1]].has_bottom_wall = False
                self.__draw_cell(direction[0], direction[1])
            elif direction[0] == i and direction[1] == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__draw_cell(i, j)
                self.__cells[direction[0]][direction[1]].has_top_wall = False
                self.__draw_cell(direction[0], direction[1])
            elif direction[0] == i - 1 and direction[1] == j:
                self.__cells[i][j].has_left_wall = False
                self.__draw_cell(i, j)
                self.__cells[direction[0]][direction[1]].has_right_wall = False
                self.__draw_cell(direction[0], direction[1])
            elif direction[0] == i + 1 and direction[1] == j:
                self.__cells[i][j].has_right_wall = False
                self.__draw_cell(i, j)
                self.__cells[direction[0]][direction[1]].has_left_wall = False
                self.__draw_cell(direction[0], direction[1])

            self.__break_walls_r(direction[0], direction[1])


def main():
    win = Window(800, 500)

    # Create a test maze
    maze = Maze(50, 50, 15, 25, 20, 20, win)

    win.wait_for_close()


if __name__ == "__main__":
    main()

