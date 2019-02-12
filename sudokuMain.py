from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import random

savePath = []
entries = []
rBoard = []
hintList = [0]
hintMax = [7]
timeMax = [0]
global timeLimitLabel

'''
BUGS
1. doesnt have to be the right stringBoard to display congrats                      FIXED

2. Make default size bigger and change placement of buttons and lines
'''


def initialize(top, arr):
    E = entries[0]
    m = 1
    for i in range(9):
        for j in range(9):
            if (not E.get()):
                arr[i][j] = 0
            else:
                arr[i][j] = int(E.get())
            if (m <= 80):
                E = entries[m]
                m += 1


def print_maze(arr):
    E = entries[0]
    m = 1
    completedString = ""
    for i in range(9):
        for j in range(9):

            completedString += str(arr[i][j])
            if (m <= 80):
                E = entries[m]
                m += 1

    return completedString


def find_empty_location(arr, l):
    for row in range(9):
        for col in range(9):
            if (arr[row][col] == 0):
                l[0] = row
                l[1] = col
                return True
    return False


def used_in_row(arr, row, num):
    for i in range(9):
        if (arr[row][i] == num):
            return True
    return False


def used_in_col(arr, col, num):
    for i in range(9):
        if (arr[i][col] == num):
            return True
    return False


def used_in_box(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if (arr[i + row][j + col] == num):
                return True
    return False


def check_location_is_safe(arr, row, col, num):
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row - row % 3,
                                                                                                 col - col % 3, num)


def solve_sudoku(arr):
    l = [0, 0]
    if (not find_empty_location(arr, l)):
        return True
    row = l[0]
    col = l[1]
    for num in range(1, 10):
        if (check_location_is_safe(arr, row, col, num)):
            arr[row][col] = num
            if (solve_sudoku(arr)):
                return True
            arr[row][col] = 0
    return False


def convertEntriesToString():
    savedFormattedString = ""
    for count, elem in enumerate(entries):
        if elem.get() == "" or elem.get() == " ":
            savedFormattedString += "0"
        else:
            savedFormattedString += elem.get()
    return savedFormattedString


def putStringToBoard(arr):
    for count, elem in enumerate(entries):

        valueToPass = arr[count]
        if valueToPass == "0":
            elem.delete(0, END)
            continue
        else:
            elem.delete(0, END)
            elem.insert(0, valueToPass)
        realBoardString = print_maze(maze)
        rBoard.append(realBoardString)


def createGUI(maze):
    top = Tk()
    top.resizable(False, False)
    top.title("Sudoku: By, Josh Gimenes")
    canvas = Canvas(top, height=320, width=350)
    canvas.configure(background='#ed0b0b')
    createRow(canvas)
    createCol(canvas)
    createEntry(top)
    hintsRemaining, maxTime = createLabels(top)

    createButtons(top, hintsRemaining)
    createMenuBar(top, hintsRemaining)
    canvas.pack(side='top')

    top.mainloop()




def createLabels(top):
    global timeLimitLabel
    hintsRemaining = Label(top, text=("Hints Remaining: " + str(hintMax[0] - hintList[0])), background='#ed0b0b',font="Helvetica 11 bold")
    timeLimitLabel = Label(top, text=("Time Left: " + str(timeMax[0])), background='#ed0b0b',font="Helvetica 11 bold")
    hintsRemaining.place(x=35, y=5)
    timeLimitLabel.place(x=225, y=5)
    return hintsRemaining, timeLimitLabel


def createButtons(top, hintsRemaining):
    button_new = Button(top, text="Submit", justify='right',background='#2a70e0', command=lambda: checkForCompletion(top, maze))
    button_hint = Button(top, text="Hint", justify='left',background='#2a70e0', command=lambda: give_hint(top, hintsRemaining))

    button_hint.place(x=70, y=275, height=30, width=60)
    button_new.place(x=230, y=275, height=30, width=60)


def clean_Mess():
    for e in entries:
        e.delete(0, END)


def createMenuBar(top, hintsRemaining):
    menubar = Menu(top)
    newGameMenu = Menu(top, tearoff=0)
    filemenu = Menu(top, tearoff=0)
    filemenu.add_command(label="Save", command=lambda: save_game(top))
    filemenu.add_separator()
    filemenu.add_command(label="Save As", command=lambda: save_as(top))
    filemenu.add_separator()
    filemenu.add_command(label="Load", command=lambda: load_file(top))
    filemenu.add_separator()
    filemenu.add_cascade(label="New", menu=newGameMenu)
    menubar.add_cascade(label="File", menu=filemenu)

    newGameMenu.add_command(label="Easy", command=lambda: arrangeEasy(top, hintsRemaining))
    newGameMenu.add_command(label="Intermediate", command=lambda: arrangeIntermediate(top, hintsRemaining))
    newGameMenu.add_command(label="Hard", command=lambda: arrangeHard(top, hintsRemaining))
    newGameMenu.add_command(label="Custom", command=lambda: arrangeCustom(top, hintsRemaining))

    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_separator()
    top.config(menu=menubar)


def save_game(top):
    if len(savePath) == 0:
        save_as(top)
    else:
        pathToSave = savePath[len(savePath) - 1]
        file = open(top.filename + ".sku", "w")

        file.write(convertEntriesToString())


def give_hint(top, label_hint):
    listOfZeroIndexes = []
    initialize(top, maze)
    if (hintList[0] == (hintMax[0])):
        pass
    else:
        if (solve_sudoku(maze)):
            realBoardString = print_maze(maze)
            currentBoardString = convertEntriesToString()
            if currentBoardString != realBoardString:
                for count, elem in enumerate(currentBoardString):
                    if elem == "0":
                        listOfZeroIndexes.append(count)
                randomIndex = random.choice(listOfZeroIndexes)
                hintValue = realBoardString[randomIndex]

                entries[randomIndex].insert(0, hintValue)
                if (solve_sudoku(maze)):
                    realBoardString = print_maze(maze)
                    rBoard.append(realBoardString)
                    hintList[0] += 1
                    label_hint.configure(text=("Hints Remaining: " + str(hintMax[0] - hintList[0])))


def checkForCompletion(top, maze):
    initialize(top, maze)
    if (solve_sudoku(maze)):
        if (rBoard[len(rBoard) - 1] == convertEntriesToString()):
            messagebox.showinfo("Sudoku", "Nice job! The puzzle took " + str(hintList[0]) + " hints!")
        else:
            messagebox.showwarning("Sudoku", "Thats the best you can do? Try again!.")
    else:
        print("No solution found!")


def save_as(top):
    top.filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                filetypes=(("sku file", "*.txt"), ("all files", "*.*")))
    file = open(top.filename + ".sku", "w+")

    file.write(convertEntriesToString())
    if (top.filename != ""):
        savePath.append(top.filename)


def arrangeEasy(top, hintsRemaining):
    for count, elem in enumerate(entries):
        elem.delete(0, END)
    difficulty = 15
    hintList[0] = 0
    hintMax[0] = 7
    start_new_game(top, difficulty, hintsRemaining)

def arrangeIntermediate(top, hintsRemaining):
    for count, elem in enumerate(entries):
        elem.delete(0, END)
    difficulty = 25
    hintList[0] = 0
    hintMax[0] = 5
    start_new_game(top, difficulty, hintsRemaining)

def arrangeHard(top, hintsRemaining):
    for count, elem in enumerate(entries):
        elem.delete(0, END)
    difficulty = 35
    hintList[0] = 0
    hintMax[0] = 3
    start_new_game(top, difficulty, hintsRemaining)

def arrangeCustom(top, hintsRemaining):
    top2 = Tk()
    top2.resizable(False, False)
    top2.title("Create Custom Game")
    e2State = [1]
    e3State = [1]

    def checkCheckButton1():
        if (e2State[0] == 0):
            tempVar = 'disabled'
            e2State[0] = 1
        else:
            tempVar = 'normal'
            e2State[0] = 0
        e2.configure(state=tempVar)

    def checkCheckButton2():
        if (e3State[0] == 0):
            tempVar = 'disabled'
            e3State[0] = 1
        else:
            tempVar = 'normal'
            e3State[0] = 0
        e3.configure(state=tempVar)

    chVarDis1 = IntVar()
    chVarDis2 = IntVar()
    check1 = Checkbutton(top2, text="Hint Limit", variable=chVarDis1, state='active',
                         command=lambda: checkCheckButton1())
    check2 = Checkbutton(top2, text="Time Limit", variable=chVarDis2, state='active',
                         command=lambda: checkCheckButton2())

    Label(top2, text="Empty Spaces (rounds evenly)").grid(row=0, column=0, padx=10, pady=5)
    Label(top2, text="Maximum Hints").grid(row=0, column=1, padx=10, pady=5)
    Label(top2, text="Time Limit (seconds)").grid(row=3, column=0, padx=10, pady=5)

    check1.grid(row=2, column=1, padx=5, )
    check2.grid(row=5, column=0, padx=5, )
    e1 = Entry(top2)
    e2 = Entry(top2, state='disabled')
    e3 = Entry(top2, state='disabled')
    b1 = Button(top2, text="Generate", justify='right',
                command=lambda: startCustomGame(top,top2, hintsRemaining, e1.get(), e2.get(), e3.get()))

    e1.grid(row=1, column=0, pady=5, padx=15)
    e2.grid(row=1, column=1, pady=5, padx=15)
    e3.grid(row=4, column=0, pady=5, padx=15)
    b1.grid(row=4, column=1, padx=5, pady=5)

    top2.mainloop()


def startCustomGame(top,top2, hintsRemaining, emptySpaces, hintLimit, timeLimit):
    top2.destroy()
    if (hintLimit != ""):
        hintMax[0] = int(hintLimit)
    for count, elem in enumerate(entries):
        elem.delete(0, END)
    if (int(emptySpaces) < 0 or int(emptySpaces) > 75  or int(hintLimit) < 0 or int(timeLimit) < 1):
        wrong = messagebox.showinfo("Error", "Invalid Entry.")
    else:
        start_new_game(top, (int(emptySpaces) / 2), hintsRemaining, timeLimit)


def start_new_game(top, difficulty, hint_label, timeLimit = 0):
    import sudokuGenerateVB
    hintList[0] = 0
    hint_label.configure(text=("Hints Remaining: " + str(hintMax[0] - hintList[0])))
    for count, elem in enumerate(entries):
        elem.config(state='normal')
    for count, elem in enumerate(entries):
        elem.delete(0, END)
    sudokuString = sudokuGenerateVB.start()
    import sudokuRemoveSpaces
    newBoardString = sudokuRemoveSpaces.main(sudokuString, difficulty)
    for count, elem in enumerate(entries):

        valueToPass = newBoardString[count]
        if valueToPass == "0":
            continue
        else:
            elem.delete(0, END)
            elem.insert(0, valueToPass)
    initialize(top, maze)
    global i
    if (timeLimit != 0 and timeLimit != ""):
        i = int(timeLimit)

        def printOneLess():
            global timeLimitLabel
            global i
            if(int(i) >= 0):
                timeLimitLabel.configure(text="Time Left: %d" % int(i))
                i -=1
                top.after(1000, printOneLess)
            else:
                timeUp = messagebox.showinfo("Timer", "Your time is up! Sorry!")
                if(str(timeUp == "ok")):
                    for count, elem in enumerate(entries):
                        elem.config(state='disabled')
                        hintMax[0] = 7

                        #elem.delete(0, END)



    if (solve_sudoku(maze)):
        realBoardString = print_maze(maze)
        rBoard.append(realBoardString)
        hintList[0] = 0
        hint_label.configure(text=("Hints Remaining: " + str(hintMax[0] - hintList[0])))
        if (timeLimit != "" and timeLimit != 0):
            timeMax[0] = int(timeLimit)


            printOneLess()



def load_file(top):
    top.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("sku files", "*.sku"), ("all files", "*.*")))
    try:
        file = open(top.filename, "r")
        sudokuString = file.read()

        if (len(sudokuString) == 81 and sudokuString.isdigit() == True):
            putStringToBoard(sudokuString)
            savePath.append(top.filename)
            if (solve_sudoku(maze)):
                realBoardString = print_maze(maze)
                rBoard.append(realBoardString)
                hintList[0] = 0

        else:
            messagebox.showerror("Error", "Cannot Load File. File is not correctly formatted.")

    except FileNotFoundError:
        pass


def createEntry(top):
    p, q = 41.4, 41.4
    for i in range(9):
        for j in range(9):
            E = Entry(top, width=3, font='BOLD')
            E.grid(row=i, column=j)
            E.place(x=p, y=q, height=20, width=25)
            entries.append(E)
            p += 30.0
        q += 24.5
        p = 41.2


def createRow(canvas):
    i, j = 40, 40
    p = 40
    q = 260
    for m in range(10):
        if (m % 3 == 0):
            canvas.create_line(i, j, p, q, width=6)
        else:
            pass
        i += 30
        p += 30


def createCol(canvas):
    t = 1.5
    i, j = 40, 40
    p, q = 310, 40
    for m in range(10):
        if m == 3 or m == 6 or m == 0 or m == 9:
            t = 6
            canvas.create_line(i, j, p, q, width=t)
        else:
            pass
        j += 24.5
        q += 24.5


if __name__ == "__main__":
    maze = [[0 for x in range(9)] for y in range(9)]
    createGUI(maze)
