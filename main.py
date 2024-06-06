from tkinter import *
from PIL import Image, ImageTk
import time
import threading
import os
from tkinter import filedialog
import math

CreatorName = "Username"

# window creation
window = Tk()
window.geometry("550x550")
window.title("MS Paint")
window.configure(bg="light grey")
window.resizable(False, False)

window.iconbitmap("PaletteIcon.ico")

# header

header = Frame(window, width=600, height=40, bg="snow3")
header.propagate(False)
header.pack()

# frame for pixel grid
grid_frame = Frame(window)
grid_frame.place(x=165, y=60)

# colors (hex)
white_hex = "#FFFFFF"
red_hex = "#ff1f1f"
orange_hex = "#ffa02b"
yellow_hex = "#fff94a"
green_hex = "#9eff42"
blue_hex = "#3e1cff"
pink_hex = "#ff66db"
brown_hex = "#693c2f"
gray_hex = "#ce1cff"
black_hex = "#000000"


# colors (num)
white = 0
red = 1
orange = 2
yellow = 3
green = 4
blue = 5
pink = 6
brown = 7
gray = 8
black = 9

# colors (ascii)
white_ascii = " "
red_ascii = "."
orange_ascii = ":"
yellow_ascii = "-"
green_ascii = "="
blue_ascii = "!"
pink_ascii = "&"
brown_ascii = "$"
gray_ascii = "%"
black_ascii = "@"


# load button images

MatrixPic = Image.open("matrizfoto.png")
MatrixPic = MatrixPic.resize((60,60), 3)
tk_MatrixPic = ImageTk.PhotoImage(MatrixPic)

MatrixNumPic = Image.open("matriznumfoto.png")
MatrixNumPic = MatrixNumPic.resize((60,60), 3)
tk_MatrixNumPic = ImageTk.PhotoImage(MatrixNumPic)

MatrixClearPic = Image.open("matrizclearfoto.png")
MatrixClearPic = MatrixClearPic.resize((60,60), 3)
tk_MatrixClearPic = ImageTk.PhotoImage(MatrixClearPic)

MatrixACIIPic = Image.open("matrizACIIfoto.png")
MatrixACIIPic = MatrixACIIPic.resize((60,60), 3)
tk_MatrixACIIPic = ImageTk.PhotoImage(MatrixACIIPic)

MatrixNegativePic = Image.open("matrizNegativefoto.png")
MatrixNegativePic = MatrixNegativePic.resize((60,60), 3)
tk_MatrixNegativePic = ImageTk.PhotoImage(MatrixNegativePic)

MatrixInvertedPic = Image.open("matrizInvertedfoto.png")
MatrixInvertedPic = MatrixInvertedPic.resize((60,60), 3)
tk_MatrixInvertedPic = ImageTk.PhotoImage(MatrixInvertedPic)

ZoominPic= Image.open("zoomin.png")
tk_ZoominPic = ImageTk.PhotoImage(ZoominPic)

ZoomoutPic= Image.open("zoomout.png")
tk_ZoomoutPic = ImageTk.PhotoImage(ZoomoutPic)

RotateLPic= Image.open("rotateleft.png")
tk_RotateLPic = ImageTk.PhotoImage(RotateLPic)

RotateRPic= Image.open("rotateright.png")
tk_RotateRPic = ImageTk.PhotoImage(RotateRPic)

InvertHPic= Image.open("invertH.png")
tk_InvertHPic = ImageTk.PhotoImage(InvertHPic)

InvertVPic= Image.open("invertV.png")
tk_InvertVPic = ImageTk.PhotoImage(InvertVPic)

RhomboidPic = Image.open("rhomboid.png")
RhomboidPic = RhomboidPic.resize((60, 60), 3)
tk_RhomboidPic = ImageTk.PhotoImage(RhomboidPic)

SquarePic = Image.open("square.png")
SquarePic = SquarePic.resize((60,60), 3)
tk_SquarePic = ImageTk.PhotoImage(SquarePic)


# global variable for changing the current selected color
SELECTED_COLOR = white_hex
SELECTED_NUMBER = white
SELECTED_ASCII = white_ascii

ShowMatrix = False
ShowAsciiMatrix = False

# class for buttons that change color
class ColorButton:
    def __init__(self, color, number, ascii, x, y):
        self.color = color
        self.number = number
        self.ascii = ascii

        def colorClick(self):
            global SELECTED_COLOR, SELECTED_NUMBER, SELECTED_ASCII
            SELECTED_COLOR = self.color
            SELECTED_NUMBER = self.number
            SELECTED_ASCII = self.ascii

        color_button = Button(window, padx=11, pady=4, bg=self.color, command=lambda: colorClick(self))
        color_button.place(x=x, y=y)


white_button = ColorButton(white_hex, white, white_ascii, 340, 430)
red_button = ColorButton(red_hex, red, red_ascii, 380, 430)
orange_button = ColorButton(orange_hex, orange, orange_ascii, 420, 430)
yellow_button = ColorButton(yellow_hex, yellow, yellow_ascii, 460, 430)
green_button = ColorButton(green_hex, green, green_ascii, 500, 430)
blue_button = ColorButton(blue_hex, blue, blue_ascii, 500, 475)
pink_button = ColorButton(pink_hex, pink, pink_ascii, 460, 475)
brown_button = ColorButton(brown_hex, brown, brown_ascii,380, 475)
gray_button = ColorButton(gray_hex, gray, gray_ascii,420, 475)
black_button = ColorButton(black_hex, black, black_ascii,340, 475)

hover_x = 0
hover_y = 0
drawing = False
is_hovering = False
draw_enabled = True
square_posx1 = 0
square_posy1 = 0
square_posx2 = 0
square_posy2 = 0
square_pos1_set = False
done_drawing_square = True
rhomboid_mode = False
zoom_in_mode = False

def left_click_start(event):
    global drawing, is_hovering, draw_enabled

    if is_hovering and draw_enabled:
        drawing = not drawing

window.bind("<Button-1>", left_click_start)


class Pixel:
    global SELECTED_COLOR, SELECTED_NUMBER, SELECTED_ASCII

    def __init__(self, state, row, column):
        self.x = row
        self.y = column
        self.state = state
        self.color = SELECTED_COLOR
        self.state_ascii = white_ascii

        self.pixel_button = Label(grid_frame, text=" ", bg=SELECTED_COLOR, fg="black", padx=5, pady=1, font=("courier new", 8))
        self.pixel_button.grid(row=row, column=column, sticky=N)

        def hoverMouse(e):
            global hover_x, hover_y, drawing, is_hovering, draw_enabled

            is_hovering = True
            hover_x = self.x
            hover_y = self.y
            if drawing and draw_enabled:
                paintPixel()

        def notHovering(e):
            global is_hovering

            is_hovering = False

        def paintPixel():
            global ShowMatrix, ShowAsciiMatrix
            for pixel in grid.grid_class_matrix:
                if (hover_x == pixel.x and hover_y == pixel.y):
                    pixel.pixel_button['bg'] = SELECTED_COLOR
                    pixel.color = SELECTED_COLOR
                    pixel.state = SELECTED_NUMBER
                    pixel.state_ascii = SELECTED_ASCII
                    grid.grid_matrix[pixel.x][pixel.y] = SELECTED_NUMBER

                    if pixel.state == black:
                        pixel.pixel_button['fg'] = white_hex
                    elif pixel.state != black:
                        pixel.pixel_button['fg'] = black_hex

                    if ShowMatrix == True:
                        pixel.pixel_button['text'] = pixel.state
                        pixel.pixel_button['padx'] = 5

                    if ShowAsciiMatrix == True:
                        pixel.pixel_button['text'] = pixel.state_ascii
                        pixel.pixel_button['padx'] = 5

        self.pixel_button.bind("<Enter>", hoverMouse)
        self.pixel_button.bind("<Leave>", notHovering)

    def updateColor(self):
        global ShowMatrix, ShowAsciiMatrix

        if self.state == 0:
            self.pixel_button['bg'] = white_hex
        elif self.state == 1:
            self.pixel_button['bg'] = red_hex
        elif self.state == 2:
            self.pixel_button['bg'] = orange_hex
        elif self.state == 3:
            self.pixel_button['bg'] = yellow_hex
        elif self.state == 4:
            self.pixel_button['bg'] = green_hex
        elif self.state == 5:
            self.pixel_button['bg'] = blue_hex
        elif self.state == 6:
            self.pixel_button['bg'] = pink_hex
        elif self.state == 7:
            self.pixel_button['bg'] = brown_hex
        elif self.state == 8:
            self.pixel_button['bg'] = gray_hex
        elif self.state == 9:
            self.pixel_button['bg'] = black_hex

        if self.state == black:
            self.pixel_button['fg'] = white_hex
        elif self.state != black:
            self.pixel_button['fg'] = black_hex

        if ShowMatrix == True:
            self.pixel_button['text'] = self.state

        if ShowAsciiMatrix == True:
            self.pixel_button['text'] = self.state_ascii

    def __str__(self):
        return f"Row: {self.x} Column: {self.y}".format(self=self)

    def squareListen1(self):
        global square_posx1, square_posy1, done_drawing_square
        print("Se llamo")
        square_posx1 = self.x
        square_posy1 = self.y
        if not done_drawing_square:
            grid.selectArea2()


    def squareListen2(self):
        global square_posx2, square_posy2, done_drawing_square, rhomboid_mode, zoom_in_mode
        square_posx2 = self.x
        square_posy2 = self.y
        if not done_drawing_square and not rhomboid_mode and not zoom_in_mode:
            grid.drawSquare()
        elif not done_drawing_square and rhomboid_mode and not zoom_in_mode:
            grid.drawRhomboid()
        elif not done_drawing_square and not rhomboid_mode and zoom_in_mode:
            grid.zoomIn()


class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid_matrix = []
        self.saved_grid_matrix = []
        self.saved_grid_class_matrix = []
        self.zoomed_grid = None

    def deleteGrid(self):
        for widget in grid_frame.winfo_children():
            widget.destroy()
        self.grid_matrix = []
        self.grid_class_matrix = []

    def newGrid(self):
        global SELECTED_COLOR, SELECTED_NUMBER, ShowMatrix, ShowAsciiMatrix

        ShowMatrix = False
        ShowAsciiMatrix = False

        for widget in grid_frame.winfo_children():
            widget.destroy()
        self.grid_matrix = []
        self.grid_class_matrix = []

        for y in range(self.y):
            row = []
            for x in range(self.x):
                SELECTED_COLOR = white_hex
                SELECTED_NUMBER = white

                pixel = Pixel(0, x, y)
                row.append(pixel.state)

                self.grid_class_matrix.append(pixel)
            self.grid_matrix.append(row)

    def printGrid(self):
        global ShowMatrix

        os.system("cls")

        for i in range(len(self.grid_matrix)):
            print(self.grid_matrix[i])
        print(" ")


    def updateGrid(self):
        i = 0
        for y in range(len(self.grid_matrix)):
            for x in range(len(self.grid_matrix[y])):

                self.grid_class_matrix[i].state = self.grid_matrix[x][y]
                self.grid_class_matrix[i].updateColor()
                i+=1

    def updateGridClassMatrix(self):
        i = 0
        print(len(self.grid_class_matrix))
        for y in range(len(self.grid_matrix)):
            for x in range(len(self.grid_matrix[y])):
                #self.grid_class_matrix.append(self.grid_matrix[y][x])
                self.grid_class_matrix[i].state = self.grid_matrix[y][x]
                self.grid_class_matrix[i].updateColor()
                i += 1

        # for i in range(len(self.grid_class_matrix)):
        #     self.grid_class_matrix[i].updateColor()

    def showMatrix(self):
        global ShowMatrix

        for i in range(len(self.grid_class_matrix)):
            self.grid_class_matrix[i].pixel_button['text'] = self.grid_class_matrix[i].state
            self.grid_class_matrix[i].pixel_button['padx'] = 5

        ShowMatrix = True

    def showAsciiMatrix(self):
        global ShowAsciiMatrix

        for i in range(len(self.grid_class_matrix)):
            self.grid_class_matrix[i].pixel_button['text'] = self.grid_class_matrix[i].state_ascii
            self.grid_class_matrix[i].pixel_button['padx'] = 5

        ShowAsciiMatrix = True

    def resetUpdateGrid(self):
        for pixel in self.grid_class_matrix:
            pixel.pixel_button['bg'] = white_hex
            pixel.pixel_button['text'] = " "

    def rotateRight(self):
        self.resetUpdateGrid()

        rotated_matrix = []
        for x in range(len(self.grid_matrix)):
            y = len(self.grid_matrix)-1
            rotated_row = []
            for i in range(len(self.grid_matrix[x])):
                rotated_row.append(self.grid_matrix[y][x])
                y-=1
            rotated_matrix.append(rotated_row)

        self.grid_matrix = rotated_matrix

        self.printGrid()
        self.updateGrid()


    def rotateLeft(self):
        self.resetUpdateGrid()

        rotated_matrix = []

        x = len(self.grid_matrix[0])-1
        for i in range(len(self.grid_matrix[0])):
            rotated_row = []
            for y in range(len(self.grid_matrix[0])):
                rotated_row.append(self.grid_matrix[y][x])

            rotated_matrix.append(rotated_row)
            x-=1

        self.grid_matrix = rotated_matrix

        self.printGrid()
        self.updateGrid()

    def invertVertical(self):
        self.resetUpdateGrid()

        inverted_matrix = []

        y = len(grid.grid_matrix)-1
        for i in range(len(grid.grid_matrix)):
            inverted_matrix.append(grid.grid_matrix[y])
            y-=1

        self.grid_matrix = inverted_matrix

        self.printGrid()
        self.updateGrid()


    def invertHorizontal(self):
        self.resetUpdateGrid()

        inverted_matrix = []

        for y in range(len(grid.grid_matrix)):
            x = len(grid.grid_matrix)-1
            inverted_row = []
            for i in range(len(grid.grid_matrix[y])):
                inverted_row.append(grid.grid_matrix[y][x])
                x-=1
            inverted_matrix.append(inverted_row)

        self.grid_matrix = inverted_matrix

        self.printGrid()
        self.updateGrid()

    def selectArea1(self, mode):
        global drawing, draw_enabled, hover_x, hover_y, done_drawing_square, is_hovering, rhomboid_mode, zoom_in_mode
        print("SET SQUARE")
        done_drawing_square = False
        drawing = False
        draw_enabled = False
        was_clicked = False
        print("click on square pos 1! ")

        if mode == 0:
            rhomboid_mode = False
            zoom_in_mode = False
        elif mode == 1:
            rhomboid_mode = True
            zoom_in_mode = False
        elif mode == 2:
            rhomboid_mode = False
            zoom_in_mode = True


        def clickPaint(e):
            was_clicked = True
            window.bind("<B1-ButtonRelease>", clickRelease)

        def clickRelease(e):
            for pixel in grid.grid_class_matrix:
                if (hover_x == pixel.x and hover_y == pixel.y) and not done_drawing_square and is_hovering:
                    pixel.squareListen1()
        if not was_clicked and not done_drawing_square:
            window.bind("<Button-1>", clickPaint)

    def selectArea2(self):
        global done_drawing_square, is_hovering
        was_clicked = False

        print("click on square pos 2!")

        def clickPaint(e):
            was_clicked = True
            window.bind("<B1-ButtonRelease>", clickRelease)

        def clickRelease(e):
            for pixel in grid.grid_class_matrix:
                if hover_x == pixel.x and hover_y == pixel.y and not done_drawing_square and is_hovering:
                    pixel.squareListen2()
                    break

        if was_clicked == False and not done_drawing_square:
            window.bind("<Button-1>", clickPaint)


    def drawSquare(self):
        global square_posx1, square_posy1, square_posx2, square_posy2, draw_enabled, SELECTED_COLOR, done_drawing_square
        print("draw square !!")
        for pixel in grid.grid_class_matrix:
            if pixel.x == square_posx1 and pixel.y == square_posy1:
                print("first pixel")
                pixel.pixel_button['bg'] = SELECTED_COLOR
                grid.grid_matrix[pixel.x][pixel.y] = SELECTED_NUMBER

        print("Left line")
        for i in range(abs(square_posx2-square_posx1)):
            for pixel in grid.grid_class_matrix:
                if pixel.x == square_posx1 + i and pixel.y == square_posy1:
                    pixel.pixel_button['bg'] = SELECTED_COLOR
                    grid.grid_matrix[pixel.x][pixel.y] = SELECTED_NUMBER

        print("Right line")
        for i in range(abs(square_posx2 - square_posx1)):
            for pixel in grid.grid_class_matrix:
                if pixel.x == square_posx1 + i and pixel.y == square_posy2:
                    pixel.pixel_button['bg'] = SELECTED_COLOR
                    grid.grid_matrix[pixel.x][pixel.y] = SELECTED_NUMBER

        print("Top line")
        for i in range(abs(square_posy2 - square_posy1)):
            for pixel in grid.grid_class_matrix:
                if pixel.x == square_posx1  and pixel.y == square_posy1 + i:
                    pixel.pixel_button['bg'] = SELECTED_COLOR
                    grid.grid_matrix[pixel.x][pixel.y] = SELECTED_NUMBER

        print("Bottom line")
        for i in range(abs(square_posy2 - square_posy1)):
            for pixel in grid.grid_class_matrix:
                if pixel.x == square_posx2 and pixel.y == square_posy1 + i:
                    pixel.pixel_button['bg'] = SELECTED_COLOR
                    grid.grid_matrix[pixel.x][pixel.y] = SELECTED_NUMBER

        for pixel in grid.grid_class_matrix:
            if pixel.x == square_posx2 and pixel.y == square_posy2:
                print("last pixel")
                pixel.pixel_button['bg'] = SELECTED_COLOR
                grid.grid_matrix[pixel.x][pixel.y] = SELECTED_NUMBER

        grid.updateGrid()

        draw_enabled = True
        done_drawing_square = True
        square_posx1 = 0
        square_posy1 = 0
        square_posx2 = 0
        square_posy2 = 0

        window.bind("<Button-1>", left_click_start)

        print(done_drawing_square, draw_enabled)

    def drawRhomboid(self):
        global square_posx1, square_posy1, square_posx2, square_posy2, draw_enabled, SELECTED_COLOR, done_drawing_square
        print("draw square !!")
        for pixel in grid.grid_class_matrix:
            if pixel.x == square_posx1 and pixel.y == square_posy1 + 3:
                print("first pixel")
                pixel.pixel_button['bg'] = SELECTED_COLOR
                grid.grid_matrix[pixel.x][pixel.y] = SELECTED_NUMBER


        print("Top line")
        for i in range(abs(square_posy2 - square_posy1 + 1)):
            if i > 3:
                for pixel in grid.grid_class_matrix:
                    if pixel.x == square_posx1 and pixel.y == square_posy1 + i:
                        pixel.pixel_button['bg'] = SELECTED_COLOR
                        grid.grid_matrix[pixel.x][pixel.y] = SELECTED_NUMBER

        print("Bottom line")
        for i in range(abs(square_posy2 - square_posy1)):
            if i < (square_posy2 - square_posy1 - 3):
                for pixel in grid.grid_class_matrix:
                    if pixel.x == square_posx2 and pixel.y == square_posy1 + i:
                        pixel.pixel_button['bg'] = SELECTED_COLOR
                        grid.grid_matrix[pixel.x][pixel.y] = SELECTED_NUMBER

        for pixel in grid.grid_class_matrix:
            if pixel.x == square_posx2 and pixel.y == square_posy2 - 3:
                print("last pixel")
                pixel.pixel_button['bg'] = SELECTED_COLOR
                grid.grid_matrix[pixel.x][pixel.y] = SELECTED_NUMBER

        diag_size = square_posx2 - square_posx1 - 1
        diag_column_size = diag_size // 3
        diag_extra_column_size = diag_size % 3

        x = 1
        # right diagonal
        for i in range(3):
            for j in range(diag_column_size):
                for pixel in grid.grid_class_matrix:
                    if pixel.y == square_posx2 - x and pixel.x == (square_posy2 - 3) + i:
                        pixel.pixel_button['bg'] = SELECTED_COLOR
                        grid.grid_matrix[pixel.y][pixel.x] = SELECTED_NUMBER
                        x+=1
                        last_pixelx_right = (square_posy2 - 3) + i
                        last_pixely_right = square_posx2 - x


        for i in range(diag_extra_column_size):
            for pixel in grid.grid_class_matrix:
                if pixel.y == square_posx1 + 1 + i and pixel.x == square_posy2:
                    pixel.pixel_button['bg'] = SELECTED_COLOR
                    grid.grid_matrix[pixel.y][pixel.x] = SELECTED_NUMBER
                    x+=1

        # left diagonal
        x = 1
        for i in range(3):
            for j in range(diag_column_size):
                for pixel in grid.grid_class_matrix:
                    if pixel.y == square_posx2 - x and pixel.x == square_posy1 + i:
                        pixel.pixel_button['bg'] = SELECTED_COLOR
                        grid.grid_matrix[pixel.y][pixel.x] = SELECTED_NUMBER
                        x+=1

        for i in range(diag_extra_column_size):
            for pixel in grid.grid_class_matrix:
                if pixel.y == square_posx1 + 1 + i and pixel.x == square_posy1 + 3:
                    pixel.pixel_button['bg'] = SELECTED_COLOR
                    grid.grid_matrix[pixel.y][pixel.x] = SELECTED_NUMBER
                    x+=1



        grid.updateGrid()

        draw_enabled = True
        done_drawing_square = True
        square_posx1 = 0
        square_posy1 = 0
        square_posx2 = 0
        square_posy2 = 0

        window.bind("<Button-1>", left_click_start)

    def negativeColors(self):
        white_invert_list = [0, 1, 2, 3, 4]
        black_invert_list = [5, 6, 7, 8, 9]

        for pixel in grid.grid_class_matrix:
            if pixel.state in white_invert_list:
                pixel.pixel_button['bg'] = white_hex

                if ShowMatrix == True:
                    pixel.pixel_button['text'] = white

                if ShowAsciiMatrix == True:
                    pixel.pixel_button['text'] = white_ascii

            elif pixel.state in black_invert_list:
                pixel.pixel_button['bg'] = black_hex
                if ShowMatrix == True:
                    pixel.pixel_button['text'] = black

                if ShowAsciiMatrix == True:
                    pixel.pixel_button['text'] = black_ascii

    def invertColors(self):
        color_code = {white:black_hex,
                      red:gray_hex,
                      orange:brown_hex,
                      yellow:pink_hex,
                      green:blue_hex,
                      blue:green_hex,
                      pink:yellow_hex,
                      brown:orange_hex,
                      gray:red_hex,
                      black:white_hex}

        for pixel in grid.grid_class_matrix:
            for state in color_code:
                if pixel.state == state:
                    pixel.pixel_button['bg'] = color_code[state]


    def hideMatrix(self):
        global ShowMatrix, ShowAsciiMatrix
        for i in range(len(self.grid_class_matrix)):
            self.grid_class_matrix[i].pixel_button['text'] = " "

        self.updateGrid()

        ShowMatrix = False
        ShowAsciiMatrix = False

    def Openfile(self):
        openFile = filedialog.askopenfilename(filetypes=[('textfile', '.txt')],
                                              defaultextension='.txt')
        grid.grid_matrix = []
        CreatorName = None
        if openFile:
            with open(openFile, 'r') as file:
                CreatorName = str(file.readline().strip())
                creator.configure(text=f"by - {CreatorName}")
                for linea in file:
                    fila = list(map(int, linea.split()))
                    grid.grid_matrix.append(fila)
            print(grid.grid_matrix)
            print(CreatorName)
            grid.updateGrid()


    def saveGrid(self):
        global CreatorName
        savefileW = Toplevel(window)
        savefileW.geometry('200x140')

        savefileL = Label(savefileW, text="Save file as...", font=("Cascadia Mono", 10))

        savefileL2 = Label(savefileW, text="Creator:", underline=True, font=("Cascadia Mono", 10))

        savefileE2 = Entry(savefileW, relief="sunken", width=15)

        savefileL.place(x=40, y=10)
        savefileL2.place(x=15, y=50)
        savefileE2.place(x=85, y=54)

        def saveFile():
            global CreatorName
            CreatorName = savefileE2.get()
            creator.configure(text=f"by - {savefileE2.get()}")
            save_file = filedialog.asksaveasfilename(defaultextension='.txt',
                                                 filetypes=[("Text file", '.txt')])
            if save_file:
                with open(save_file, 'w') as file:
                    file.write(str(CreatorName) + '\n')
                    for i in grid.grid_matrix:
                        file.write(' '.join(map(str, i)) + '\n')
                print(f'Matriz guardada en {save_file}')
            print(savefileE2.get())
            savefileW.destroy()

        savefileSB = Button(savefileW, text="Save", font=("Cascadia Mono", 10), command=saveFile)
        savefileCB = Button(savefileW, text="Cancel", font=("Cascadia Mono", 10), command=savefileW.destroy)
        savefileSB.place(x=35, y=95)
        savefileCB.place(x=105, y=95)

    def zoomIn(self):
        global square_posx1, square_posy1, square_posx2, square_posy2
        print("zoom in")

        x1 = square_posy1
        y1 = square_posx1
        x2 = square_posy2
        y2 = square_posx2

        zoomed_matrix = []
        for i in range(y2 - y1):
            zoomed_row = []
            for j in range(x2 - x1):
                x = self.grid_matrix[y1 + i][x1 + j]
                zoomed_row.append(x)
            zoomed_matrix.append(zoomed_row)

        for row in zoomed_matrix:
            print(row)

        self.saved_grid_matrix = self.grid_matrix
        self.saved_grid_class_matrix = self.grid_class_matrix

        self.deleteGrid()

        grid2 = Grid(len(zoomed_matrix), len(zoomed_matrix[0]))
        grid2.newGrid()
        grid2.grid_matrix = zoomed_matrix

        self.zoomed_grid = grid2

        grid2.updateGridClassMatrix()

        square_posx1 = 0
        square_posy1 = 0
        square_posx2 = 0
        square_posy2 = 0

        # grid.updateGrid()

    def zoomOut(self):
        global draw_enabled, SELECTED_COLOR, done_drawing_square
        draw_enabled = True
        done_drawing_square = True
        SELECTED_COLOR = white_hex
        SELECTED_NUMBER = white
        SELECTED_ASCII = white_ascii

        self.zoomed_grid.deleteGrid()

        self.newGrid()
        self.grid_matrix = self.saved_grid_matrix
        self.updateGrid()

        window.bind("<Button-1>", left_click_start)


grid = Grid(18, 18)
grid.newGrid()

hideMatrix_button = Button(window, image=tk_MatrixPic, command=lambda: grid.hideMatrix())
hideMatrix_button.place(x=10, y=60)

shownumbers_button = Button(window, image=tk_MatrixNumPic, command=lambda: grid.showMatrix())
shownumbers_button.place(x=90, y=60)

clear_button = Button(window, image=tk_MatrixClearPic, font=("arial", 12), bg=white_hex, fg=black_hex, command=grid.newGrid)
clear_button.place(x=10,y=210)

showASCII_button = Button(window, image=tk_MatrixACIIPic, command=grid.showAsciiMatrix)
showASCII_button.place(x=90, y=210)

NegativeMatrix_button = Button(window, image=tk_MatrixNegativePic, command=grid.negativeColors)
NegativeMatrix_button.place(x=10, y=135)

InvertedMatrix_button = Button(window, image=tk_MatrixInvertedPic, command=grid.invertColors)
InvertedMatrix_button.place(x=90, y=135)

Zoomin_button = Button(window, image=tk_ZoominPic, command=lambda: grid.selectArea1(2))
Zoomin_button.place(x=10,y=285)

Zoomout_button = Button(window, image=tk_ZoomoutPic, command=grid.zoomOut)
Zoomout_button.place(x=90,y=285)

RotateR_button = Button(window, image=tk_RotateRPic, command=grid.rotateRight)
RotateR_button.place(x=90,y=360)

RotateL_button = Button(window, image=tk_RotateLPic, command=grid.rotateLeft)
RotateL_button.place(x=10,y=360)

InvertH_button = Button(window, image=tk_InvertHPic, command=grid.invertHorizontal)
InvertH_button.place(x=10, y=435)

InvertV_button = Button(window, image=tk_InvertVPic, command=grid.invertVertical)
InvertV_button.place(x=90, y=435)

Rhomboid_button = Button(window, image=tk_RhomboidPic, command=lambda: grid.selectArea1(1))
Rhomboid_button.place(x=170, y=435)

Square_button = Button(window, image=tk_SquarePic, command=lambda: grid.selectArea1(0))
Square_button.place(x=250, y=435)

def paintOrNoPaint(value):
    global draw_enabled
    if value == 0:
        draw_enabled = True
    else:
        draw_enabled = False

no_button = Button(window, text='PAINT', font=("Cascadia Mono", 10), command= lambda: paintOrNoPaint(0))
no_button.place(x=20, y=510)

brush_button = Button(window, text='STOP PAINTING', font=("Cascadia Mono", 10), command=lambda: paintOrNoPaint(1))
brush_button.place(x=100, y=510)

openfile_button = Button(header, text="Open", underline=True, font=("Cascadia Mono", 10), bg= "snow3", relief=FLAT, command=grid.Openfile)
openfile_button.place(x=50, y=5)

savefile_button = Button(header, text="Save", underline=True, font=("Cascadia Mono", 10), bg= "snow3", relief=FLAT, command=grid.saveGrid)
savefile_button.place(x=98, y=5)

print_grid_button = Button(header, text="Print", underline=True, font=("Cascadia Mono", 10), bg= "snow3", relief=FLAT, command=grid.printGrid)
print_grid_button.place(x=140, y=5)


creator = Label(header, text=f"by - {CreatorName}", font=("Cascadia Mono", 10), bg= "snow3")
creator.place(x=210, y=8)

window.mainloop()