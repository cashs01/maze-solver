from tkinter import Tk, BOTH, Canvas
import time


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
    def __init__(self, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = window

    def draw(self, x1, x2, y1, y2):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        if self.has_left_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "white")
        if self.has_right_wall:
            self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "white")
        if self.has_top_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "white")
        if self.has_bottom_wall:
            self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "white")

    def draw_move(self, to_cell, undo=False):
        if not undo:
            color = "red"
        else:
            color = "gray"
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
        win,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.__cells = []
        self.__create_cells()

    def __create_cells(self):
        for i in range(self.num_cols):
            col_cells = []
            for j in range(self.num_rows):
                cell = Cell(self.win)
                col_cells.append(cell)
            self.__cells.append(col_cells)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self.__cells[i][j].draw(x1, x2, y1, y2)
        self.__animate()

    def __animate(self):
        self.win.redraw()
        time.sleep(0.05)



def main():
    win = Window(800, 500)

    # Create a small test maze (5x5)
    maze = Maze(50, 50, 15, 20, 20, 20, win)

    win.wait_for_close()


main()

