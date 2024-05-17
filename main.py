from tkinter import *
import os

window = Tk()
window.geometry("600x400")
window.title("MS Paint")
window.configure(bg="#008080")
window.resizable(False, False)

grid_frame = Frame(window)
grid_frame.place(relx=0.6, rely=0.5, anchor=CENTER)

# colors
black = "#000000"
white = "#FFFFFF"
red = "#ff0000"
green = "#00ff00"
blue = "#0000ff"
pink = "#ff4df6"
orange = "#ff7700"
yellow = "#fffb17"
brown = "#57270b"
gray = "#757575"

SELECTED_COLOR = white

class ColorButton():
    def __init__(self, color, x, y):
        self.color = color

        def buttonClick(self):
            global SELECTED_COLOR
            SELECTED_COLOR = self.color

        color_button = Button(window, padx=18, pady=10, bg=self.color, command=lambda: buttonClick(self))
        color_button.place(x=x, y=y)


red_button = ColorButton(red, 50, 50)
green_button = ColorButton(green, 50, 100)
blue_button = ColorButton(blue, 50, 150)
white_button = ColorButton(white, 50, 200)
black_button = ColorButton(black, 50, 250)
pink_button = ColorButton(pink, 100, 50)
orange_button = ColorButton(orange, 100, 100)
yellow_button = ColorButton(yellow, 100, 150)
brown_button = ColorButton(brown, 100, 200)
gray_button = ColorButton(gray, 100, 250)


class Pixel():
    def __init__(self, state, row, column):
        self.x = row
        self.y = column
        self.state = state

        def pixelClick(self):
            global SELECTED_COLOR
            self.pixel_button['bg'] = SELECTED_COLOR

            if SELECTED_COLOR == white:
                self.state = 0

            elif SELECTED_COLOR == red:
                self.state = 1

            elif SELECTED_COLOR == orange:
                self.state = 2

            elif SELECTED_COLOR == yellow:
                self.state = 3

            elif SELECTED_COLOR == green:
                self.state = 4

            elif SELECTED_COLOR == blue:
                self.state = 5

            elif SELECTED_COLOR == pink:
                self.state = 6

            elif SELECTED_COLOR == brown:
                self.state = 7

            elif SELECTED_COLOR == gray:
                self.state = 8

            elif SELECTED_COLOR == black:
                self.state = 9

            grid.grid_matrix[self.x][self.y] = self.state


        self.pixel_button = Button(grid_frame, padx=8, bg=white, command=lambda: pixelClick(self))
        self.pixel_button.grid(row=row, column=column, sticky=N)


class Grid():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid_matrix = []

    def newGrid(self):
        for widget in grid_frame.winfo_children():
            widget.destroy()

        self.grid_matrix = []
        pixel_count = 0
        for y in range(self.y):
            row = []
            for x in range(self.x):
                pixel = Pixel(0, x, y)
                row.append(pixel.state)
            self.grid_matrix.append(row)

    def printGrid(self):
        for i in range(len(self.grid_matrix)-1):
            print(self.grid_matrix[i])

        print(" ")

grid = Grid(12, 12)
grid.newGrid()

clear_button = Button(window, text="Clear", font=("arial", 12), bg=white, fg=black, command=grid.newGrid)
clear_button.place(x=50, y=350)

print_grid_button = Button(window, text="Print", font=("arial", 12), bg=white, fg=black, command=grid.printGrid)
print_grid_button.place(x=120, y=350)


window.mainloop()