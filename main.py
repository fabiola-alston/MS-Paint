from tkinter import *
from PIL import Image, ImageTk
import time
import threading
import os
from tkinter import filedialog


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
# grid_frame.place(relx=0.648, rely=0.45, anchor=CENTER)
grid_frame.place(x=165, y=60)

CreatorName = "Username"

# colors (hex)

white_hex = "#FFFFFF"
red_hex = "#ff0000"
orange_hex = "#ff7700"
yellow_hex = "#fffb17"
green_hex = "#00ff00"
blue_hex = "#0000ff"
pink_hex = "#ff4df6"
brown_hex = "#57270b"
gray_hex = "#757575"
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

CirclePic = Image.open("Circle.webp")
CirclePic = CirclePic.resize((60,60), 3)
tk_CirclePic = ImageTk.PhotoImage(CirclePic)

SquarePic = Image.open("square.png")
SquarePic = SquarePic.resize((60,60), 3)
tk_SquarePic = ImageTk.PhotoImage(SquarePic)

VScroll = Image.open("VScrollBar.png")
VScroll = VScroll.resize((21, 375), 3)
tk_VScroll = ImageTk.PhotoImage(VScroll)

HScroll = Image.open("HScrollBar.png")
HScroll = HScroll.resize((396, 21), 3)
tk_HScroll = ImageTk.PhotoImage(HScroll)

no_img = Image.open("nosymbol.jpg")
no_img = no_img.resize((396, 21), 3)
no_tk = ImageTk.PhotoImage(no_img)

brush = Image.open("brush.jpg")
brush = brush.resize((396, 21), 3)
brush_tk = ImageTk.PhotoImage(brush)


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
brown_button = ColorButton(brown_hex, brown, brown_ascii,420, 475)
gray_button = ColorButton(gray_hex, gray, gray_ascii,380, 475)
black_button = ColorButton(black_hex, black, black_ascii,340, 475)

hover_x = 0
hover_y = 0
drawing = False
is_hovering = False

def left_click_start(event):
    global drawing, is_hovering

    if is_hovering:
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
            global hover_x, hover_y, drawing, is_hovering

            is_hovering = True
            hover_x = self.x
            hover_y = self.y

            if drawing:
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


class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid_matrix = []

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

    def Openfile(self):
        openFile = filedialog.askopenfilename(filetypes=[('textfile', '.txt')],
                                              defaultextension='.txt')
        file = open(openFile, 'r')
        self.updateGrid()
        print(file.read())
        file.close()

    def saveGrid(self):
        global CreatorName
        savefileW = Toplevel(window)
        savefileW.geometry('200x140')

        savefileL = Label(savefileW, text="Save file as...", font=("Cascadia Mono", 10))

        savefileL2 = Label(savefileW, text="Creator:", underline=True, font=("Cascadia Mono", 10))

        savefileE2 = Entry(savefileW, relief="sunken", width=15)

        CreatorName = savefileE2.get()

        savefileL.place(x=40, y=10)
        savefileL2.place(x=15, y=50)
        savefileE2.place(x=85, y=54)

        def saveFile():
            creator.config(text=f"by - {CreatorName}")
            save_file = filedialog.asksaveasfile(defaultextension='.txt',
                                                 filetypes=[("Text file", '.txt')])
            save_file_text = str(grid.grid_matrix)
            save_file.write(save_file_text)
            save_file.close()
            savefileW.destroy()
            print(save_file.read)

        savefileSB = Button(savefileW, text="Save", font=("Cascadia Mono", 10), command=saveFile)
        savefileCB = Button(savefileW, text="Cancel", font=("Cascadia Mono", 10), command=savefileW.destroy)
        savefileSB.place(x=35, y=95)
        savefileCB.place(x=105, y=95)

    def printGrid(self):
        global ShowMatrix

        #os.system("cls")

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

    def drawSquare(self):
        pass

    def drawCircle(self):
        pass

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


grid = Grid(18, 18)
grid.newGrid()



#Placing tools on window


hideMatrix_button = Button(window, image=tk_MatrixPic, command=lambda: grid.hideMatrix())
shownumbers_button = Button(window, image=tk_MatrixNumPic, command=lambda: grid.showMatrix())
clear_button = Button(window, image=tk_MatrixClearPic, font=("arial", 12), bg=white_hex, fg=black_hex, command=grid.newGrid)
showASCII_button = Button(window, image=tk_MatrixACIIPic, command=grid.showAsciiMatrix)
showASCII_button.place(x=90, y=210)

NegativeMatrix_button = Button(window, image=tk_MatrixNegativePic, command=grid.negativeColors)
NegativeMatrix_button.place(x=10, y=135)

InvertedMatrix_button = Button(window, image=tk_MatrixInvertedPic, command=grid.invertColors)
InvertedMatrix_button.place(x=90, y=135)

InvertedMatrix_button = Button(window, image=tk_MatrixInvertedPic)
NegativeMatrix_button = Button(window, image=tk_MatrixNegativePic)
Zoomin_button = Button(window, image=tk_ZoominPic)
Zoomout_button = Button(window, image=tk_ZoomoutPic)
RotateR_button = Button(window, image=tk_RotateRPic, command=grid.rotateRight)
RotateL_button = Button(window, image=tk_RotateLPic, command=grid.rotateLeft)
RotateL_button.place(x=10,y=360)

InvertH_button = Button(window, image=tk_InvertHPic, command=grid.invertHorizontal)
InvertH_button.place(x=10, y=435)

InvertV_button = Button(window, image=tk_InvertVPic, command=grid.invertVertical)
InvertV_button.place(x=90, y=435)

InvertV_button = Button(window, image=tk_InvertVPic)
InvertH_button = Button(window, image=tk_InvertHPic)
Circle_button = Button(window, image=tk_CirclePic)
Square_button = Button(window, image=tk_SquarePic)



openfile_button = Button(header, text="Open", underline=True, font=("Cascadia Mono", 10), bg= "snow3", relief=FLAT,
                         command=grid.Openfile)
savefile_button = Button(header, text="Save", underline=True, font=("Cascadia Mono", 10), bg= "snow3", relief=FLAT,
                         command=grid.saveGrid)
print_grid_button = Button(header, text="Print", underline=True, font=("Cascadia Mono", 10), bg= "snow3", relief=FLAT, command=grid.printGrid)
creator = Label(header, text=f"by - {CreatorName}", font=("Cascadia Mono", 10), bg= "snow3")



hideMatrix_button.place(x=10, y=60)
shownumbers_button.place(x=90, y=60)
clear_button.place(x=10,y=210)
showASCII_button.place(x=90, y=210)
InvertedMatrix_button.place(x=10, y=135)
NegativeMatrix_button.place(x=90, y=135)
Zoomin_button.place(x=10,y=285)
Zoomout_button.place(x=90,y=285)
RotateR_button.place(x=90,y=360)
RotateL_button.place(x=10,y=360)
InvertV_button.place(x=10, y=435)
InvertH_button.place(x=90, y=435)
Circle_button.place(x=170, y=435)
Square_button.place(x=250, y=435)

def paintOrNoPaint(value):
    global drawing
    if value == 0:
        drawing = True
    else:
        drawing = False

no_button = Button(window, text='PAINT', font=("Cascadia Mono", 10), command= lambda: paintOrNoPaint(0))
no_button.place(x=20, y=510)

brush_button = Button(window, text='STOP PAINTING', font=("Cascadia Mono", 10), command=lambda: paintOrNoPaint(1))
brush_button.place(x=100, y=510)

newfile_button = Button(header, text="New", underline=True,  font=("Cascadia Mono", 10), bg= "snow3", relief=FLAT)
newfile_button.place(x=10, y=5)
openfile_button.place(x=10, y=5)
savefile_button.place(x=58, y=5)
print_grid_button.place(x=110, y=5)
creator.place(x=170, y=8)



window.mainloop()