import json
import os
import random
from tkinter import *
from tkinter.font import Font
from tkinter import messagebox

import string
from functools import partial
import requests
from fake_useragent import UserAgent as ua
from base64 import b85decode, b85encode
import copy

class GameGrid(Tk):
    def __init__(self):
        super(GameGrid, self).__init__()
        
        self.board_width, self.board_height = (9, 9)
        self.region_width, self.region_height = (3, 3)
        self.outer_border_width, self.inner_border_width = (5, 2)
        self.cell_width, self.cell_height = (70, 70)
        self.font_size = 28
        self.candidate_font_size = 12

        self.background = "#f6f5f7"
        self.uneditable_foreground = "#4450ff"
        self.editable_foreground = "#222222"

        self.hover_background = "#D8D8D8"
        self.uneditable_hover_foreground = "#4450ff"
        self.editable_hover_foreground = "#222222"

        self.selected_background = "#4450ff"
        self.uneditable_selected_foreground = "#ffffff"
        self.editable_selected_foreground = "#ffffff"

        self.new_icon = PhotoImage(file="assets/new.png")
        self.check_icon = PhotoImage(file="assets/check.png")
        self.file_icon = PhotoImage(file="assets/file.png")
        self.hint_icon = PhotoImage(file="assets/hint.png")
        self.cleanup_icon = PhotoImage(file="assets/cleanup.png")
        self.highlight_icon = PhotoImage(file="assets/highlight.png")
        self.play_icon = PhotoImage(file="assets/play.png")
        self.pause_icon = PhotoImage(file="assets/pause.png")
        self.replay_icon = PhotoImage(file="assets/replay.png")
        self.settings_icon = PhotoImage(file="assets/settings.png")

        self.current_selected_cell = None
        self.current_highlight_cells = []
        self.current_board = [[0 for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.question_board = []
        self.current_board_editable_map = [[True for _ in range(self.board_width)] for _ in range(self.board_height)]

        self.title('Sudoku')
        self.config(background=self.background)
        self.iconbitmap('./assets/logo.ico')
        self.newgame_window = None

        self.setupWidget()
        self.placeWidget()
        self.setupEvent()
        self.generateBoard()

    def setupWidget(self):
        self.grid_container = Frame(self, bg=self.uneditable_foreground)
        self.cell_container = [[Frame(self.grid_container, width=self.cell_width, height=self.cell_height) for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.grid = [
            [
                Entry(
                    self.cell_container[y][x], 
                    width=3, 
                    justify="center", 
                    relief="flat",
                    bg=self.background,
                    disabledbackground=self.background,
                    disabledforeground=self.editable_foreground if self.current_board_editable_map[y][x] else self.uneditable_foreground,
                    state="disabled",
                    font=Font(size=self.font_size, weight="bold"),
                    cursor="arrow"
                ) for x in range(self.board_width)
            ] for y in range(self.board_height)
        ]

        self.button_container = Frame(self, bg=self.background)
        self.new_button = Button(self.button_container, image=self.new_icon, relief="flat", bg=self.background, command=self.newBoard)
        self.check_button = Button(self.button_container, image=self.check_icon, relief="flat", bg=self.background, command=self.checkBoard)
        self.file_button = Button(self.button_container, image=self.file_icon, relief="flat", bg=self.background, command=self.loadBoard)
        self.highlight_button = Button(self.button_container, image=self.highlight_icon, relief="flat", bg=self.background, command=self.highlightCells)
        self.hint_button = Button(self.button_container, image=self.hint_icon, relief="flat", bg=self.background, command=self.getCandidate)
        self.cleanup_button = Button(self.button_container, image=self.cleanup_icon, relief="flat", bg=self.background, command=self.cleanupBoard)
        self.play_button = Button(self.button_container, image=self.pause_icon, relief="flat", bg=self.background, command=self.pauseGame)
        self.replay_button = Button(self.button_container, image=self.replay_icon, relief="flat", bg=self.background, command=self.redoBoard)
        self.settings_button = Button(self.button_container, image=self.settings_icon, relief="flat", bg=self.background)

    def placeWidget(self):
        self.grid_container.pack(padx=(20, 0), pady=20, side="left")
        [
            [
                self.cell_container[y][x].pack_propagate(False)
                for x in range(self.board_width)
            ] for y in range(self.board_height)
        ]
        [
            [
                self.cell_container[y][x].grid(
                    row=y, 
                    column=x,
                    padx=(self.outer_border_width, 0) if not x%self.region_width else (self.inner_border_width, self.outer_border_width if (x+1) == self.board_width else 0), 
                    pady=(self.outer_border_width, 0) if not y%self.region_height else (self.inner_border_width, self.outer_border_width if (y+1) == self.board_height else 0)
                ) for x in range(self.board_width)
            ] for y in range(self.board_height)
        ]
        [
            [
                self.grid[y][x].pack(
                    expand=True,
                    fill="both"
                ) for x in range(self.board_width)
            ] for y in range(self.board_height)
        ]

        self.button_container.pack(side="left", padx=(10, 20))
        self.new_button.pack(pady=10)
        self.play_button.pack(pady=10)
        self.replay_button.pack(pady=10)
        self.hint_button.pack(pady=10)
        self.cleanup_button.pack(pady=10)
        self.highlight_button.pack(pady=10)
        self.check_button.pack(pady=10)
        self.file_button.pack(pady=10)
        self.settings_button.pack(pady=10)

    def setupEvent(self): 
        [
            [
                [
                    self.grid[y][x].bind('<Enter>', partial(self.onCellMouseEnterCallback, y, x)),
                    self.grid[y][x].bind('<Leave>', partial(self.onCellMouseLeaveCallback, y, x)),
                    self.grid[y][x].bind('<Button-1>', partial(self.selectCellCallback, y, x)),
                ]
                for x in range(self.board_width)
            ] for y in range(self.board_height)
        ]
        [self.bind(str(i), partial(self.insertNumberCallback, i)) for i in range(1, 10)]
        [self.bind(f'<Control-Key-{i}>', partial(self.insertCandidateCallback, i)) for i in range(1, 10)]
        self.bind('<BackSpace>', self.clearCellCallback)
        self.bind('<Escape>', self.escapeHighlightCallback)

    def writeCell(self, y, x, i):
        cell = self.grid[y][x]
        cell.config(state='normal')
        cell.delete(0, 'end')
        cell.insert(0, str(i))
        cell.config(state='disabled', font=Font(size=self.font_size, weight="bold"))

    def writeCandidate(self, y, x, i):
        cell = self.grid[y][x]

        if str(i) not in cell.get():
            cell.config(state='normal')
            cell.insert(0, str(i))
            cell.config(state='disabled', font=Font(size=self.candidate_font_size, weight="bold"))
        else:
            cell.config(state='normal')
            new = cell.get().replace(str(i), "")
            cell.delete(0, 'end')
            cell.insert(0, new)
            cell.config(state='disabled', font=Font(size=self.candidate_font_size, weight="bold"))

    def updateBoard(self, run="ingame"):
        if run == "ingame":
            for y in range(self.board_height):
                for x in range(self.board_width):
                    cell_content = self.grid[y][x].get()
                    if not cell_content or not cell_content.isdigit(): num = 0
                    else: num = int(cell_content)
                    self.current_board[y][x] = num

        elif run == "new":
            for y in range(self.board_height):
                for x in range(self.board_width):
                    num = self.current_board[y][x]
                    self.writeCell(y, x, num if num else "")
        else: return

    def updateHighlight(self):
        if self.current_selected_cell:
            _y, _x = self.current_selected_cell
            current_selected_cell = self.grid[_y][_x].get()
            if not current_selected_cell or not current_selected_cell.isdigit(): 
                self.current_highlight_cells = []
                return
            else: current_selected_num = int(current_selected_cell)

            for y in range(self.board_height):
                for x in range(self.board_width):
                    cell = (y, x)
                    cell_content = self.grid[y][x].get()
                    if not cell_content or not cell_content.isdigit(): continue
                    else: num = int(cell_content)

                    if num == current_selected_num:
                        if cell not in self.current_highlight_cells:
                            if num == current_selected_num and cell:
                                self.current_highlight_cells.append(cell)
                    else:
                        if cell in self.current_highlight_cells:
                            self.current_highlight_cells.remove(cell)

    def updateForeground(self):
        for y in range(self.board_height):
            for x in range(self.board_width):
                if self.current_board_editable_map[y][x]:
                    self.grid[y][x].config(disabledforeground=self.editable_foreground)
                else:
                    self.grid[y][x].config(disabledforeground=self.uneditable_foreground)

    def renderHighlight(self):
        for y in range(self.board_height):
            for x in range(self.board_width):
                is_editable = self.current_board_editable_map[y][x]
                cell = (y, x)
                if cell in self.current_highlight_cells or cell == self.current_selected_cell:
                    self.grid[y][x].config(
                        disabledbackground=self.selected_background, 
                        disabledforeground=self.editable_selected_foreground if is_editable else self.uneditable_selected_foreground
                    )
                else:
                    self.grid[y][x].config(
                        disabledbackground=self.background, 
                        disabledforeground=self.editable_foreground if is_editable else self.uneditable_foreground
                    )

    def onCellMouseLeaveCallback(self, y, x, e):
        is_editable = self.current_board_editable_map[y][x]
        if self.current_selected_cell == (y, x) or (y, x) in self.current_highlight_cells:
            e.widget.configure(
                disabledbackground=self.selected_background, 
                disabledforeground=self.editable_selected_foreground if is_editable else self.uneditable_selected_foreground
            )
        else:
            e.widget.config(
                disabledbackground=self.background, 
                disabledforeground=self.editable_foreground if is_editable else self.uneditable_foreground
            )

    def onCellMouseEnterCallback(self, y, x, e):
        is_editable = self.current_board_editable_map[y][x]
        if self.current_selected_cell != (y, x) and (y, x) not in self.current_highlight_cells:
            e.widget.configure(
                disabledbackground=self.hover_background, 
                disabledforeground=self.editable_hover_foreground if is_editable else self.uneditable_hover_foreground
            )

    def selectCellCallback(self, y, x, e):
        self.current_selected_cell = (y, x)

        self.updateHighlight()
        self.renderHighlight()

    def insertNumberCallback(self, n, e):
        if self.current_selected_cell:
            y, x = self.current_selected_cell
            if self.current_board_editable_map[y][x]:
                self.writeCell(y, x, n)

                self.updateBoard()
                self.updateHighlight()
                self.renderHighlight()

    def insertCandidateCallback(self, n, e):
        if self.current_selected_cell:
            y, x = self.current_selected_cell
            if self.current_board_editable_map[y][x]:
                self.writeCandidate(y, x, n)
                
                self.updateBoard()
                self.updateHighlight()
                self.renderHighlight()

    def clearCellCallback(self, e):
        if self.current_selected_cell:
            y, x = self.current_selected_cell
            if self.current_board_editable_map[y][x]:
                self.writeCell(y, x, "")

                self.updateBoard()
                self.updateHighlight()
                self.renderHighlight()

    def escapeHighlightCallback(self, e):
        self.current_selected_cell = None
        self.current_highlight_cells = []

        self.renderHighlight()

    def generateEditableMap(self):
        editable_map = []
        for y in range(self.board_height):
            editable_map.append([])
            for x in range(self.board_width):
                if self.current_board[y][x]: is_editable = False
                else: is_editable = True
                editable_map[-1].append(is_editable)

        self.current_board_editable_map = editable_map
        self.updateForeground()

    def generateBoard(self, difficulty="hard"):
        if difficulty == "custom": return
        request_headers = {
            'x-requested-with': 'XMLHttpRequest', 
            'user-agent': ua().random
        }
        response = requests.get(f'https://sudoku.com/api/level/{difficulty}', headers=request_headers).json()
        if response:
            raw_data = response["mission"]
            self.question_board = [[int(j) for j in raw_data[i:i+self.board_width]] for i in range(0, self.board_width*self.board_height, self.board_height)]
            
            if len(self.question_board[0]) == self.board_width and len(self.question_board) == self.board_height:
                self.current_board = copy.deepcopy(self.question_board)
                self.updateBoard(run="new")
                self.generateEditableMap()
            else:
                raise RuntimeError('Sudoku board size doesn\'t match')
        else:
            raise RuntimeError('Sudoku board fetching failed')

    def redoBoard(self):
        confirm = messagebox.askquestion("Are you sure?","Are you sure you wanna redo the board? This operation is not reversible.", icon="warning")
        if confirm == "yes":
            for y in range(self.board_height):
                for x in range(self.board_width):
                    if self.current_board_editable_map[y][x]:
                        self.writeCell(y, x, "")
                        self.current_board[y][x] = 0
            self.escapeHighlightCallback(None)

    def cleanupBoard(self):
        confirm = messagebox.askyesnocancel("Wanna clear all?","Do you wanna keep cells with less than two candidates? Select NO to clean up the whole board and leave cells with definite answer only.", icon="warning")
        if confirm != None:
            for y in range(self.board_height):
                for x in range(self.board_width):
                    cell = self.current_board[y][x]
                    if len(str(cell)) > (2 if confirm else 1):
                        self.writeCell(y, x, "")

    def pauseGame(self):
        for y in range(self.board_height):
            for x in range(self.board_width):
                self.writeCell(y, x, "")

        self.play_button.config(image=self.play_icon, command=self.resumeGame)
        self.escapeHighlightCallback(None)

    def resumeGame(self):
        for y in range(self.board_height):
            for x in range(self.board_width):
                num = self.current_board[y][x]
                self.writeCell(y, x, num if num else "")

        self.play_button.config(image=self.pause_icon, command=self.pauseGame)

    def getCandidate(self):
        for y in range(self.board_height):
            for x in range(self.board_width):
                if self.current_board_editable_map[y][x]:
                    if self.current_board[y][x] == 0 or len(str(self.current_board[y][x])) > 1:
                        row = self.current_board[y]
                        col = list(list(zip(*self.current_board))[x])
                        region = [[self.current_board[_y][_x] for _x in range(x//3*3, x//3*3+3)] for _y in range(y//3*3, y//3*3+3)]
                        
                        collection = set(row+col+sum(region, []))
                        if 0 in collection: collection.remove(0)
                        num_range = set(range(1, self.board_width+1))
                        candidates = ''.join(list(map(str, num_range.difference(collection))))

                        cell = self.grid[y][x]
                        cell.config(state="normal")
                        cell.delete(0, 'end')
                        cell.insert(0, candidates)
                        cell.config(state="disabled", font=Font(size=self.candidate_font_size if len(candidates) > 1 else self.font_size, weight="bold"))

        self.updateBoard()

    def checkBoard(self):
        region_y_count = self.board_height//self.region_height
        region_x_count = self.board_width//self.region_width
        region_range = sum([[((y*3, y*3+3), (x*3, x*3+3)) for x in range(region_x_count)] for y in range(region_y_count)], [])
        region = [sum([i[x[0]:x[1]] for i in self.current_board[y[0]:y[1]]], []) for y, x in region_range]
        
        check_row = all(set(i) == set(range(1, self.board_width+1)) for i in self.current_board)
        check_col = all(set(i) == set(range(1, self.board_width+1)) for i in zip(*self.current_board))
        check_region = all(set(i) == set(range(1, self.board_width+1)) for i in region)
        if check_row and check_col and check_region:
            messagebox.showinfo('Congrats', 'You win the game!')
            self.escapeHighlightCallback(None)
            self.lockAllCell()
            self.saveBoardToHistory()
        else:
            messagebox.showerror('Oops!', 'Something went wrong! Please check your board carefully.')

    def lockAllCell(self):
        self.current_board_editable_map = [[False for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.updateForeground()

    def saveBoardToHistory(self):
        if not os.path.exists('history.sudoku'): open('history.sudoku', 'w')
        with open('history.sudoku', 'r') as encoded:
            try: data = json.loads(b85decode(encoded.read()[::2].encode('utf-8')).decode('utf-8').replace('\'', '"'))
            except: data = []
            data += [{
                'question': b85encode(''.join([''.join(str(j) for j in i) for i in self.question_board]).encode('utf-8')).decode('utf-8'),
                'answer': b85encode(''.join([''.join(str(j) for j in i) for i in self.current_board]).encode('utf-8')).decode('utf-8'),
                'difficulty': 'hard', 
                'ended': 0,
                'time_taken': 0
            }]
            with open('history.sudoku', 'w') as file:
                raw = b85encode(str(data).encode('utf-8')).decode('utf-8') 
                file.write(''.join([''.join(i) for i in zip(raw, random.choices(string.punctuation+string.ascii_letters, k=len(raw)))]))

    def newBoard(self):
        if not self.newgame_window:
            self.newgame_window = NewGameWindow(self)

        '''self.escapeHighlightCallback(None)
        self.generateBoard()
        self.resumeGame()'''

    def highlightCells(self):
        ...

    def loadBoard(self):
        ...

    def startGame(self, difficulty="medium"):
        self.escapeHighlightCallback(None)
        self.generateBoard(difficulty)
        self.resumeGame()
        if self.newgame_window:
            self.newgame_window.destroy()
            self.newgame_window = None

class NewGameWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.easy_icon = PhotoImage(file='assets/easy.png')
        self.medium_icon = PhotoImage(file='assets/medium.png')
        self.hard_icon = PhotoImage(file='assets/hard.png')
        self.custom_icon = PhotoImage(file='assets/custom.png')

        self.title('New Game')
        self.iconbitmap('assets/logo.ico')
        self.config(bg=self.master.background)
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.focus()

        self.setupWidget()
        self.setupBindings()
        self.placeWidget()

    def setupWidget(self):
        self.button_container = Frame(self, bg=self.master.background)
        self.difficulty = ['easy', 'medium', 'hard', 'custom']
        self.difficulty_buttons = [
            Button(
                self.button_container, 
                text='\n'+diff.title(),
                image=self.__dict__[diff+'_icon'],
                compound="top", 
                font=Font(size=14, weight="bold"),
                command=partial(self.master.startGame, diff), 
                bg=self.master.uneditable_foreground, 
                fg=self.master.uneditable_selected_foreground,
                relief='flat',
                width=100
            ) for diff in self.difficulty]

    def setupBindings(self):
        ...

    def placeWidget(self):
        self.button_container.pack(fill="both", expand=True, padx=20, pady=20)
        [button.grid(row=index//2, column=index-index//2*2, padx=5, pady=5, ipadx=20, ipady=20) for index, button in enumerate(self.difficulty_buttons)]

    def quit(self):
        self.master.newgame_window = None
        self.destroy()
        self.master.focus()

root = GameGrid()
root.mainloop()