from tkinter import Button, Frame, Label, Tk
import random

# Define global variables
board_size = 3
buttons = [[' ' for _ in range(board_size)] for _ in range(board_size)]
board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
label = None
reset_button = None
main_menu_button = None
frame = None
current_player = None

def minimax(board, depth, is_maximizing, alpha, beta):
    if check_win('o'):  # Assuming 'o' is the AI
        return {'score': 1}
    elif check_win('x'):  # Assuming 'x' is the human player
        return {'score': -1}
    elif ' ' not in [cell for row in board for cell in row]:  # Draw condition
        return {'score': 0}

    if is_maximizing:
        best_score = {'score': -float('inf')}
        for row in range(board_size):
            for column in range(board_size):
                if board[row][column] == ' ':
                    board[row][column] = 'o'
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[row][column] = ' '
                    score['row'], score['column'] = row, column
                    best_score = max(best_score, score, key=lambda x:x['score'])
                    alpha = max(alpha, score['score'])
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = {'score': float('inf')}
        for row in range(board_size):
            for column in range(board_size):
                if board[row][column] == ' ':
                    board[row][column] = 'x'
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[row][column] = ' '
                    score['row'], score['column'] = row, column
                    best_score = min(best_score, score, key=lambda x:x['score'])
                    beta = min(beta, score['score'])
                    if beta <= alpha:
                        break
        return best_score

def start_single_player_game():
    global label, buttons, reset_button, main_menu_button, frame, board, current_player

    # Initialize game state
    board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
    current_player = 'x'

    if label and label.winfo_exists():
        label.pack_forget()
    if reset_button and reset_button.winfo_exists():
        reset_button.pack_forget()
    if main_menu_button and main_menu_button.winfo_exists():
        main_menu_button.pack_forget()
    if frame and frame.winfo_exists():
        frame.pack_forget()

    label = Label(text=current_player + ' turn', font=('consolas', 40))  # shows players turn
    label.pack(side='top')

    # reset game button
    reset_button = Button(text='restart', font=('consolas', 20), command=start_single_player_game)
    reset_button.pack(side='top')

    main_menu_button = Button(text='Main Menu', font=('consolas', 20), command=main_menu)
    main_menu_button.pack(side='top')

    frame = Frame(window)  # put all of them into a frame
    frame.pack()

    # create buttons for each rows and columns
    for row in range(board_size):
        for column in range(board_size):
            buttons[row][column] = Button(frame, text='', font=('consolas', 40), width=5, height=2,
                                          command=lambda row=row, column=column: next_turn(row, column))
            buttons[row][column].grid(row=row, column=column)

    if app.single_player_mode and app.user_choice == 'o':
        # Make the computer take the first turn as 'X'
        window.after(100, ai_move)

def start_multi_player_game():
    global label, buttons, reset_button, main_menu_button, frame, board, current_player

    # Initialize game state
    board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
    current_player = 'x'

    if label and label.winfo_exists():
        label.pack_forget()
    if reset_button and reset_button.winfo_exists():
        reset_button.pack_forget()
    if main_menu_button and main_menu_button.winfo_exists():
        main_menu_button.pack_forget()
    if frame and frame.winfo_exists():
        frame.pack_forget()

    label = Label(text=current_player + ' turn', font=('consolas', 40))  # shows players turn
    label.pack(side='top')

    # reset game button
    reset_button = Button(text='restart', font=('consolas', 20), command=start_multi_player_game)
    reset_button.pack(side='top')

    main_menu_button = Button(text='Main Menu', font=('consolas', 20), command=main_menu)
    main_menu_button.pack(side='top')

    frame = Frame(window)  # put all of them into a frame
    frame.pack()

    # create buttons for each rows and columns
    for row in range(board_size):
        for column in range(board_size):
            buttons[row][column] = Button(frame, text='', font=('consolas', 40), width=5, height=2,
                                          command=lambda row=row, column=column: next_turn(row, column))
            buttons[row][column].grid(row=row, column=column)

def ai_move():
    global current_player

    move = minimax(board, 0, True, -float('inf'), float('inf'))
    
    buttons[move['row']][move['column']]['text'] = current_player
    buttons[move['row']][move['column']]['state'] = 'disabled'
    board[move['row']][move['column']] = current_player

    if check_win(current_player):
        label['text'] = current_player + ' wins!'
        for row in buttons:
            for button in row:
                button['state'] = 'disabled'
    elif ' ' not in [cell for row in board for cell in row]:
        label['text'] = 'Draw!'
        for row in buttons:
            for button in row:
                button['state'] = 'disabled'
    else:
        label['text'] = current_player + ' turn'
        current_player = 'o' if current_player == 'x' else 'x'

def next_turn(row, column):
    global current_player

    # Mark the cell
    buttons[row][column]['text'] = current_player
    buttons[row][column]['state'] = 'disabled'
    board[row][column] = current_player

    # Check for win
    if check_win(current_player):
        label['text'] = current_player + ' wins!'
        for row in buttons:
            for button in row:
                button['state'] = 'disabled'
    elif ' ' not in [cell for row in board for cell in row]:
        label['text'] = 'Draw!'
        for row in buttons:
            for button in row:
                button['state'] = 'disabled'
    else:
        current_player = 'o' if current_player == 'x' else 'x'
        label['text'] = current_player + ' turn'

        if app.single_player_mode and current_player != app.user_choice:
            ai_move()

def check_win(player):
    # Check rows, columns and diagonals for win
    return any(all(cell == player for cell in row) for row in board) or \
           any(all(board[i][j] == player for i in range(board_size)) for j in range(board_size)) or \
           all(board[i][i] == player for i in range(board_size)) or \
           all(board[i][board_size - i - 1] == player for i in range(board_size))

class TicTacToeApp:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        self.single_player_mode = False

        self.single_player_button = Button(self.frame, text="Player vs Computer", font=('consolas', 20),
                                           command=self.single_player)
        self.single_player_button.pack()

        self.multiplayer_button = Button(self.frame, text="Player vs Player", font=('consolas', 20),
                                         command=self.multiplayer)
        self.multiplayer_button.pack()

    def single_player(self):
        self.frame.pack_forget()
        self.single_player_mode = True
        self.ask_user_choice()

    def multiplayer(self):
        self.frame.pack_forget()
        self.single_player_mode = False
        start_multi_player_game()

    def ask_user_choice(self):
        self.choice_frame = Frame(self.master)
        self.choice_frame.pack()

        self.x_button = Button(self.choice_frame, text="X", font=('consolas', 20),
                               command=lambda: self.set_user_choice('x'))
        self.x_button.pack(side='left')

        self.o_button = Button(self.choice_frame, text="O", font=('consolas', 20),
                               command=lambda: self.set_user_choice('o'))
        self.o_button.pack(side='right')

    def set_user_choice(self, choice):
        self.user_choice = choice
        self.choice_frame.pack_forget()
        start_single_player_game()

def main_menu():
    global label, reset_button, main_menu_button, frame

    # Hide the current game elements
    if label:
        label.pack_forget()
    if reset_button:
        reset_button.pack_forget()
    if main_menu_button:
        main_menu_button.pack_forget()
    if frame:
        frame.pack_forget()

    # Show the initial menu frame
    app.frame.pack()

window = Tk()
window.title("Tic Tac Toe")
window.geometry("500x500")

app = TicTacToeApp(window)

main_menu()  # Call main_menu() here

window.mainloop()  # Then start the mainloop
