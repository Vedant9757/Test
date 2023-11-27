import tkinter as tk
from tkinter import messagebox
import random

def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

def solve_sudoku(board):
    find = find_empty_location(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False

def is_valid(board, num, position):
    for i in range(len(board[0])):
        if board[position[0]][i] == num and position[1] != i:
            return False

    for i in range(len(board)):
        if board[i][position[1]] == num and position[0] != i:
            return False

    box_x = position[1] // 3
    box_y = position[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != position:
                return False

    return True

def find_empty_location(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    return None

def solve():
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            value = entry_list[i][j].get()
            if value == "":
                row.append(0)
            else:
                row.append(int(value))
        board.append(row)

    if solve_sudoku(board):
        for i in range(9):
            for j in range(9):
                entry_list[i][j].insert(0, str(board[i][j]))
                entry_list[i][j].config(state="readonly")
        messagebox.showinfo("Sudoku Solver", "Sudoku Solved!")
    else:
        messagebox.showerror("Sudoku Solver", "No solution exists.")

def clear_board():
    for i in range(9):
        for j in range(9):
            entry_list[i][j].delete(0, tk.END)
            entry_list[i][j].config(state="normal")

def create_board(difficulty_level):
    board = [[0 for _ in range(9)] for _ in range(9)]
    if difficulty_level == 'Easy':
        filled_cells = 25
    elif difficulty_level == 'Medium':
        filled_cells = 40
    else:
        filled_cells = 55

    while filled_cells > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] == 0:
            num = random.randint(1, 9)
            if is_valid(board, num, (row, col)):
                board[row][col] = num
                filled_cells -= 1

    return board

root = tk.Tk()
root.title("Sudoku Solver")

entry_list = []

for i in range(9):
    row = []
    for j in range(9):
        entry = tk.Entry(root, width=2, font=('Arial', 14))
        entry.grid(row=i, column=j)
        row.append(entry)
    entry_list.append(row)

difficulty_label = tk.Label(root, text="Select Difficulty:")
difficulty_label.grid(row=9, column=0, columnspan=3)

difficulty_var = tk.StringVar()
difficulty_var.set('Easy')
difficulty_option = tk.OptionMenu(root, difficulty_var, 'Easy', 'Medium', 'Hard','Master')
difficulty_option.grid(row=9, column=3, columnspan=3)

solve_button = tk.Button(root, text="Solve Sudoku", command=solve)
solve_button.grid(row=10, columnspan=9)

clear_button = tk.Button(root, text="Clear Board", command=clear_board)
clear_button.grid(row=11, columnspan=9)

def create_new_board(difficulty):
    clear_board()
    board = create_board(difficulty)
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                entry_list[i][j].insert(0, str(board[i][j]))
                entry_list[i][j].config(state="readonly")

create_new_board(difficulty_var.get())

root.mainloop()
