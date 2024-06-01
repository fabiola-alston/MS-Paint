from tkinter import *
from PIL import Image, ImageTk
import time
import threading


# window creation
window = Tk()
window.geometry("550x525")
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
grid_frame.place(relx=0.648, rely=0.45, anchor=CENTER)

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

        color_button = Button(window, padx=11, pady=4, bg=self.color, command=lambda: colorClick(self))
        color_button.place(x=x, y=y)


white_button = ColorButton(white_hex, white, 340, 430)
red_button = ColorButton(red_hex, red, 380, 430)
orange_button = ColorButton(orange_hex, orange, 420, 430)
yellow_button = ColorButton(yellow_hex, yellow, 460, 430)
green_button = ColorButton(green_hex, green, 500, 430)
blue_button = ColorButton(blue_hex, blue, 500, 475)
pink_button = ColorButton(pink_hex, pink, 460, 475)
brown_button = ColorButton(brown_hex, brown, 420, 475)
gray_button = ColorButton(gray_hex, gray, 380, 475)
black_button = ColorButton(black_hex, black, 340, 475)

hover_x = 0
hover_y = 0
hold_down = True

# def holdDown(e):
#     global hold_down
#     hold_down = True
#
# def letGo(e):
#     global hold_down
#     hold_down = False
#
# def clickBind():
#     window.bind("<ButtonPress-1>", holdDown)
#     window.bind("<ButtonRelease-1>", letGo)
#
# click_thread = threading.Thread(target=clickBind)
# click_thread.start()

class Pixel:
    global SELECTED_COLOR, SELECTED_NUMBER

    def __init__(self, state, row, column):
        self.x = row
        self.y = column
        self.state = state

        self.pixel_button = Label(grid_frame, bg=SELECTED_COLOR, fg="black", padx=8, pady=1)
        self.pixel_button.grid(row=row, column=column, sticky=N)

        def hoverMouse(e):
            global hover_x, hover_y
            hover_x = self.x
            hover_y = self.y
            paintPixel()
            print(hover_x, hover_y)

        def paintPixel():
            global hold_down
            print("painting !")
            for pixel in grid.grid_class_matrix:
                if (hover_x == pixel.x and hover_y == pixel.y) and hold_down == True:
                    pixel.pixel_button['bg'] = SELECTED_COLOR
                    pixel.state = SELECTED_NUMBER
                    if ShowMatrix == True:
                        pixel.pixel_button['text'] = pixel.state
                        pixel.pixel_button['padx'] = 5

        self.pixel_button.bind("<Enter>", hoverMouse)

    def __str__(self):
        return f"Row: {self.x} Column: {self.y}".format(self=self)


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
            self.grid_matrix.append(row)


    def printGrid(self):
        global ShowMatrix
        for i in range(len(self.grid_matrix)):
            print(self.grid_matrix[i])
        print(" ")

    def showMatrix(self):
        global ShowMatrix

        for i in range(len(self.grid_class_matrix)):
            self.grid_class_matrix[i].pixel_button['text'] = self.grid_class_matrix[i].state
            self.grid_class_matrix[i].pixel_button['padx'] = 5

        ShowMatrix = True

    def hideMatrix(self):
        global ShowMatrix
        for i in range(len(self.grid_class_matrix)):
            self.grid_class_matrix[i].pixel_button['text'] = "  "

        ShowMatrix = False

grid = Grid(18, 18)
grid.newGrid()

VscrollL = Label(window, image=tk_VScroll)
#VscrollL.place(x=520, y=60)

HscrollL = Label(window, image=tk_HScroll)
#HscrollL.place(x=173, y=420)

showMatrix_button = Button(window, image=tk_MatrixPic, command=lambda: grid.hideMatrix())
shownumbers_button = Button(window, image=tk_MatrixNumPic, command=lambda: grid.showMatrix())
clear_button = Button(window, image=tk_MatrixClearPic, font=("arial", 12), bg=white_hex, fg=black_hex, command=grid.newGrid)
showACII_button = Button(window, image=tk_MatrixACIIPic)
NegativeMatrix_button = Button(window, image=tk_MatrixNegativePic)
InvertedMatrix_button = Button(window, image=tk_MatrixInvertedPic)
Zoomin_button = Button(window, image=tk_ZoominPic)
Zoomout_button = Button(window, image=tk_ZoomoutPic)
RotateR_button = Button(window, image=tk_RotateRPic)
RotateL_button = Button(window, image=tk_RotateLPic)
InvertH_button = Button(window, image=tk_InvertHPic)
InvertV_button = Button(window, image=tk_InvertVPic)
Circle_button = Button(window, image=tk_CirclePic)
Square_button = Button(window, image=tk_SquarePic)


showMatrix_button.place(x=10, y=60)
shownumbers_button.place(x=90, y=60)
NegativeMatrix_button.place(x=10, y=135)
InvertedMatrix_button.place(x=90, y=135)
clear_button.place(x=10,y=210)
showACII_button.place(x=90, y=210)
Zoomin_button.place(x=10,y=285)
Zoomout_button.place(x=90,y=285)
RotateL_button.place(x=10,y=360)
RotateR_button.place(x=90,y=360)
InvertH_button.place(x=10, y=435)
InvertV_button.place(x=90, y=435)
Circle_button.place(x=170, y=435)
Square_button.place(x=250, y=435)


newfile_button = Button(header, text="New", underline=True,  font=("Cascadia Mono", 10), bg= "snow3", relief=FLAT)
newfile_button.place(x=10, y=5)

openfile_button = Button(header, text="Open", underline=True, font=("Cascadia Mono", 10), bg= "snow3", relief=FLAT)
openfile_button.place(x=50, y=5)

savefile_button = Button(header, text="Save", underline=True, font=("Cascadia Mono", 10), bg= "snow3", relief=FLAT)
savefile_button.place(x=98, y=5)

print_grid_button = Button(header, text="Print", underline=True, font=("Cascadia Mono", 10), bg= "snow3", relief=FLAT, command=grid.printGrid)
print_grid_button.place(x=140, y=5)

creator_name = "creator name"

creator = Label(header, text=f"by - {creator_name}", font=("Cascadia Mono", 10), bg= "snow3")
creator.place(x=210, y=8)

window.mainloop()