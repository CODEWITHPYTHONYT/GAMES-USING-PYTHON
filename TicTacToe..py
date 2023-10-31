import tkinter as tk
from tkinter import messagebox
from time import time
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")

        self.current_player = 'X'
        self.board = [None] * 9
        self.timer_running = True
        self.timer_duration = 10
        self.start_time = time()
        self.opponent_bot = False  # Initially, no bot
        self.bot_difficulty = 'Normal'  # Default bot difficulty

        self.opponent_selection_frame = tk.Frame(root)
        self.opponent_selection_frame.pack(pady=20)
        tk.Button(self.opponent_selection_frame, text="Play with Bot", command=self.play_with_bot).pack(side=tk.LEFT, padx=10)
        tk.Button(self.opponent_selection_frame, text="Play with Player", command=self.play_with_player).pack(side=tk.LEFT, padx=10)

        self.difficulty_selection_frame = tk.Frame(root)
        self.difficulty_selection_frame.pack(pady=10)
        difficulties = ['Easy', 'Normal', 'Hard', 'Extreme']
        self.difficulty_var = tk.StringVar(value='Normal')
        for difficulty in difficulties:
            tk.Radiobutton(self.difficulty_selection_frame, text=difficulty, variable=self.difficulty_var, value=difficulty, command=self.set_bot_difficulty).pack(side=tk.LEFT)

        self.timer_label = tk.Label(root, text="Time Left: 10", font=("Arial", 12))
        self.timer_label.pack(pady=10)
        
        self.timer_options = tk.Frame(root)
        self.timer_options.pack(pady=10)
        
        tk.Label(self.timer_options, text="Timer Duration (seconds):").grid(row=0, column=0)
        self.timer_entry = tk.Entry(self.timer_options)
        self.timer_entry.grid(row=0, column=1)
        self.timer_entry.insert(0, "10")
        
        self.set_timer_button = tk.Button(self.timer_options, text="Set Timer", command=self.set_timer)
        self.set_timer_button.grid(row=0, column=2)
        
        self.stop_timer_button = tk.Button(self.timer_options, text="Stop Timer", command=self.stop_timer)
        self.stop_timer_button.grid(row=0, column=3)
        
        self.no_timer_button = tk.Button(self.timer_options, text="No Timer", command=self.no_timer)
        self.no_timer_button.grid(row=0, column=4)

        grid_frame = tk.Frame(root)
        grid_frame.pack()
        for i in range(9):
            row = i // 3
            col = i % 3
            button = tk.Button(grid_frame, text='', width=10, height=3, command=lambda i=i: self.make_move(i))
            button.grid(row=row, column=col)
            self.board[i] = button

        self.update_timer()

    def play_with_bot(self):
        self.opponent_bot = True
        self.opponent_selection_frame.pack_forget()
        self.difficulty_selection_frame.pack()
        self.reset_board()

    def play_with_player(self):
        self.opponent_bot = False
        self.opponent_selection_frame.pack_forget()
        self.difficulty_selection_frame.pack_forget()
        self.reset_board()

    def set_bot_difficulty(self):
        self.bot_difficulty = self.difficulty_var.get()

    def make_move(self, index):
        if not self.board[index]["text"]:
            self.board[index]["text"] = self.current_player
            self.board[index]["state"] = 'disabled'
            if self.check_winner(index):
                self.animate_winning_line(index, self.current_player)
                if self.opponent_bot:
                    if self.current_player == 'X':
                        messagebox.showinfo("Game Over", "You win!")
                    else:
                        messagebox.showinfo("Game Over", "Bot wins!")
                else:
                    messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_board()
            elif not any(not cell["text"] for cell in self.board):
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.start_time = time()
                self.update_timer()
                if self.opponent_bot and self.current_player == 'O':
                    self.bot_move()

    def bot_move(self):
        if self.bot_difficulty == 'Easy':
            self.bot_move_easy()
        elif self.bot_difficulty == 'Normal':
            self.bot_move_normal()
        elif self.bot_difficulty == 'Hard':
            self.bot_move_hard()
        elif self.bot_difficulty == 'Extreme':
            self.bot_move_extreme()

    def bot_move_easy(self):
        available_cells = [i for i, cell in enumerate(self.board) if not cell["text"]]
        if available_cells:
            random_index = random.choice(available_cells)
            self.make_move(random_index)

    def bot_move_normal(self):
        player = 'X' if self.current_player == 'O' else 'O'

        for i in range(9):
            if not self.board[i]["text"]:
                self.board[i]["text"] = player
                if self.check_winner(i):
                    self.animate_winning_line(i, player)
                    return

                self.board[i]["text"] = ''

        self.bot_move_easy()

    def bot_move_hard(self):
        player = 'X' if self.current_player == 'O' else 'O'

        for i in range(9):
            if not self.board[i]["text"]:
                self.board[i]["text"] = self.current_player
                if self.check_winner(i):
                    self.animate_winning_line(i, self.current_player)
                    return
                self.board[i]["text"] = ''

        for i in range(9):
            if not self.board[i]["text"]:
                self.board[i]["text"] = player
                if self.check_winner(i):
                    self.animate_winning_line(i, player)
                    self.board[i]["text"] = self.current_player
                    self.board[i]["state"] = 'disabled'
                    return
                self.board[i]["text"] = ''

        self.bot_move_easy()

    def bot_move_extreme(self):
        player = 'X' if self.current_player == 'O' else 'O'

        for i in range(9):
            if not self.board[i]["text"]:
                self.board[i]["text"] = self.current_player
                if self.check_winner(i):
                    self.animate_winning_line(i, self.current_player)
                    return
                self.board[i]["text"] = ''

        for i in range(9):
            if not self.board[i]["text"]:
                self.board[i]["text"] = player
                if self.check_winner(i):
                    self.animate_winning_line(i, player)
                    self.board[i]["text"] = self.current_player
                    self.board[i]["state"] = 'disabled'
                    return
                self.board[i]["text"] = ''

        prioritized_cells = [4, 0, 2, 6, 8, 1, 3, 5, 7]
        for cell in prioritized_cells:
            if not self.board[cell]["text"]:
                self.make_move(cell)
                return

        self.bot_move_easy()

    def check_winner(self, index):
        winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for combo in winning_combinations:
            if all(self.board[i]["text"] == self.current_player for i in combo):
                return True
        return False

    def animate_winning_line(self, index, player):
        winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for combo in winning_combinations:
            if index in combo and all(self.board[i]["text"] == player for i in combo):
                for i in combo:
                    self.board[i]["bg"] = 'green'
                    self.root.update()
                break

    def reset_board(self):
        for button in self.board:
            button["text"] = ''
            button["state"] = 'active'
            button["bg"] = 'SystemButtonFace'
        self.current_player = 'X'
        self.start_time = time()
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time() - self.start_time)
            time_left = max(self.timer_duration - elapsed_time, 0)
            self.timer_label.config(text=f"Time Left: {time_left}")
            if time_left > 0:
                self.root.after(1000, self.update_timer)
            else:
                if self.opponent_bot and self.current_player == 'O':
                    self.bot_move()
                else:
                    self.make_move(self.board.index([button for button in self.board if not button["text"]][0]))

    def set_timer(self):
        try:
            self.timer_duration = int(self.timer_entry.get())
            if self.timer_duration < 0:
                self.timer_duration = 0
            self.timer_running = True
            self.timer_entry.config(state='disabled')
            self.set_timer_button.config(state='disabled')
            self.stop_timer_button.config(state='active')
            self.no_timer_button.config(state='active')
            self.start_time = time()
            self.update_timer()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer for the timer duration.")

    def stop_timer(self):
        self.timer_running = False
        self.timer_entry.config(state='normal')
        self.set_timer_button.config(state='active')
        self.stop_timer_button.config(state='disabled')
        self.no_timer_button.config(state='active')

    def no_timer(self):
        self.timer_running = False
        self.timer_duration = -1
        self.timer_label.config(text="No Timer")
        self.timer_entry.config(state='disabled')
        self.set_timer_button.config(state='disabled')
        self.stop_timer_button.config(state='disabled')
        self.no_timer_button.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
