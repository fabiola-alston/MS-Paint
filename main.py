from tkinter import *
# import os

# window creation
window = Tk()
window.geometry("600x400")
window.title("MS Paint")
window.configure(bg="#A9A9A9")
window.resizable(False, False)

# frame for pixel grid
grid_frame = Frame(window)
grid_frame.place(relx=0.6, rely=0.5, anchor=CENTER)

# colors (hex)
black_hex = "#000000"
white_hex = "#FFFFFF"
red_hex = "#ff0000"
green_hex = "#00ff00"
blue_hex = "#0000ff"
pink_hex = "#ff4df6"
orange_hex = "#ff7700"
yellow_hex = "#fffb17"
brown_hex = "#57270b"
gray_hex = "#757575"

# colors (num)
black = 9
white = 0
red = 1
orange = 2
yellow = 3
green = 4
blue = 5
pink = 6
brown = 7
gray = 8

# global variable for changing the current selected color
SELECTED_COLOR = white_hex
SELECTED_NUMBER = white

ShowMatrix = False

# class for buttons that change color
class ColorButton:
    def __init__(self, color, number, x, y):
        self.color = color
        self.number = number

        def colorClick(self):
            global SELECTED_COLOR, SELECTED_NUMBER
            SELECTED_COLOR = self.color
            SELECTED_NUMBER = self.number

        color_button = Button(window, padx=18, pady=10, bg=self.color, command=lambda: colorClick(self))
        color_button.place(x=x, y=y)



red_button = ColorButton(red_hex, red, 50, 50)
green_button = ColorButton(green_hex, green, 50, 100)
blue_button = ColorButton(blue_hex, blue, 50, 150)
white_button = ColorButton(white_hex, white, 50, 200)
black_button = ColorButton(black_hex, black, 50, 250)
pink_button = ColorButton(pink_hex, pink, 100, 50)
orange_button = ColorButton(orange_hex, orange, 100, 100)
yellow_button = ColorButton(yellow_hex, yellow, 100, 150)
brown_button = ColorButton(brown_hex, brown, 100, 200)
gray_button = ColorButton(gray_hex, gray, 100, 250)


class Pixel:
    global SELECTED_COLOR, SELECTED_NUMBER
    def __init__(self, state, row, column):
        self.x = row
        self.y = column
        self.state = state

        def pixelClick(self):
            global ShowMatrix
            self.pixel_button['bg'] = SELECTED_COLOR
            if ShowMatrix == True:
                self.pixel_button['text'] = SELECTED_NUMBER

            if SELECTED_COLOR == white_hex:
                self.state = white

            elif SELECTED_COLOR == red_hex:
                self.state = red

            elif SELECTED_COLOR == orange_hex:
                self.state = orange

            elif SELECTED_COLOR == yellow_hex:
                self.state = yellow

            elif SELECTED_COLOR == green_hex:
                self.state = green

            elif SELECTED_COLOR == blue_hex:
                self.state = blue

            elif SELECTED_COLOR == pink_hex:
                self.state = pink

            elif SELECTED_COLOR == brown_hex:
                self.state = brown

            elif SELECTED_COLOR == gray_hex:
                self.state = gray

            elif SELECTED_COLOR == black_hex:
                self.state = black

            grid.grid_matrix[self.x][self.y] = self.state

        self.pixel_button = Button(grid_frame, text="  ",  padx=8, pady=3, bg=white_hex, command=lambda: pixelClick(self))
        self.pixel_button.grid(row=row, column=column, sticky=N)


class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid_matrix = []

    def newGrid(self):
        for widget in grid_frame.winfo_children():
            widget.destroy()
        self.grid_matrix = []
        self.grid_class_matrix = []

        for y in range(self.y):
            row = []
            for x in range(self.x):
                pixel = Pixel(0, x, y)
                row.append(pixel.state)
                self.grid_class_matrix.append(pixel)
                print(self.grid_class_matrix)
            self.grid_matrix.append(row)

    #def getGrid(self):
        #for y in range(self.y):


    def printGrid(self):
        global ShowMatrix
        for i in range(len(self.grid_matrix)):
            print(self.grid_matrix[i])
        print(" ")

    def showMatrix(self):
        global ShowMatrix
        # for pixel in grid_frame.winfo_children():
        #     pixel['text'] = pixel.state

        for i in range(len(self.grid_class_matrix)):
            self.grid_class_matrix[i].pixel_button['text'] = self.grid_class_matrix[i].state

        ShowMatrix = True


    def hideMatrix(self):
        global ShowMatrix
        for i in range(len(self.grid_class_matrix)):
            self.grid_class_matrix[i].pixel_button['text'] = "  "

        ShowMatrix = False


grid = Grid(12, 12)
grid.newGrid()

sm_button = Button(window, text='show', command=lambda: grid.showMatrix())
sm_button.pack()

hm_button = Button(window, text='hide', command=lambda: grid.hideMatrix())
hm_button.pack()

clear_button = Button(window, text="Clear", font=("arial", 12), bg=white_hex, fg=black_hex, command=grid.newGrid)
clear_button.place(x=50, y=350)

print_grid_button = Button(window, text="Print", font=("arial", 12), bg=white_hex, fg=black_hex, command=grid.printGrid)
print_grid_button.place(x=120, y=350)


window.mainloop()