#import library
from tkinter import filedialog; from tkinter import *; from tkinter.font import Font; import os; from timeformation import *; from random import randint, shuffle
import time, datetime, json
from gensudoku import gensudoku
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#initialize root window
root = Tk(); root.config(bg='white'); root.title('SUDOKU'); root.geometry('1120x900+400+60'); root.resizable(False, False)

#set the font style
winfont, numfont, smallnumfont, buttonfont, counterfont = Font(size=30, family='Bahnschrift SemiBold'), Font(size=40, family='Bahnschrift SemiBold'), Font(size=12, family='Bahnschrift SemiBold'), Font(size=20, family='Bahnschrift'), Font(size=40, family='Bahnschrift')

def expandLine(line):
	global base
	base=3
	return line[0]+line[5:9].join([line[1:5]*(base-1)]*base)+line[9:13]

def sort():
	global ebox
	x, y, label, row, col = 10,10, [], [], []
	for i in range(9):
		row.append([]); label.append([]); col.append([]); x=10
		for i2 in range(9):
			fixnum = ebox[i][i2].get(); col[i].append(ebox[i2][i].get())
			if fixnum == '': row[i].append('0'); label[i].append('0')
			else: row[i].append(fixnum)
			root.update()
			x+=91
		y+=91

	col, box, count, count2, count3 = [[0 if col[i][i2]=='' else col[i][i2] for i2 in range(9)] for i in range(9)], [], 0, 0, 0
	for i4 in range(3):
		for i3 in range(3):
			box.append([])
			for i in range(3):
				[box[count3].append(row[i+count2][i2+count]) for i2 in range(3)]
			count, count3 = count+3, count3+1
		count2, count = count2+3, 0

	for i in range(9):
		for i2 in range(9):
			if len(ebox[i][i2].get()) != 1:
				status[i][i2] = 1
				lol = ebox[i][i2].get()
				ebox[i][i2].delete(0, END)
				ebox[i][i2].config(font=smallnumfont)
				ebox[i][i2].update()
				[ebox[i][i2].insert(END, str(n)) if str(n) not in row[i] and str(n) not in col[i2] and str(n) not in box[0 if i2 in range(0, 3) and i in range(0, 3) else 1 if i2 in range(3, 6) and i in range(0, 3) else 2 if i2 in range(6, 9) and i in range(0, 3) else 3 if i2 in range(0, 3) and i in range(3, 6) else 4 if i2 in range(3, 6) and i in range(3, 6) else 5 if i2 in range(6, 9) and i in range(3, 6) else 6 if i2 in range(0, 3) and i in range(6, 9) else 7 if i2 in range(3, 6) and i in range(6, 9) else 8 if i2 in range(6, 9) and i in range(6, 9) else ''] else '' for n in range(1, 10)]
				if len(ebox[i][i2].get()) == 1: ebox[i][i2].config(font=numfont); ebox[i][i2].update()
			if len(ebox[i][i2].get()) == 1:
				status[i][i2] = 0
	#button.config(state=DISABLED)
	print(status)

maincanvas = Canvas(root, width=900, height=900, bg='white', highlightthickness=0); maincanvas.place(x=30, y=10)

topLeft_x=10
topLeft_y=820

intDim=90
for row in range(0,10):
	if (row%3)==0:
		size = 3
	else:
		size = 1
	maincanvas.create_line(topLeft_x, topLeft_y-row*intDim, topLeft_x+9*intDim, topLeft_y-row*intDim, width=size, fill='#00A6FF')
for col in range(0,10):
	if (col%3)==0:
		size = 3
	else:
		size = 1   
	maincanvas.create_line(topLeft_x+col*intDim, topLeft_y, topLeft_x+col*intDim, topLeft_y-9*intDim, width=size, fill='#00A6FF')

def checkclick(e):
	global eboxc
	eboxc = e.widget
	for a in range(9):
		for a2 in range(9):
			ebox[a][a2].config(bg='white', disabledbackground='white')
	for i in range(len(ebox)):
		if e.widget in ebox[i]:
			for a in range(9):
				for a2 in range(9):
					ebox[a][a2].config(bg='white', disabledbackground='white')
					if ebox[a][a2].get() == e.widget.get() and ebox[a][a2].get() != '':
						ebox[a][a2].config(bg='#DDDDDD')
						if ebox[a][a2]['state'] == DISABLED:
							ebox[a][a2].config(disabledbackground='#DDDDDD')
			e.widget.config(bg='#DDDDDD')

def refresh(e):
	row = [i for i in range(len(ebox)) if e.widget in ebox[i]][0]
	column = ebox[row].index(e.widget)
	refreshc = [i[column] for i in ebox]
	refreshbox = []
	wrong = False
	box_place = [range(row//3*3, row//3*3+3), range(column//3*3, column//3*3+3)]
	if not status[row][column]:
		for i in ebox[row]:
			content = i.get()
			if content == ebox[row][column].get() and ebox[row][column].get() and i != ebox[row][column]:
				wrong = True
				break
			if len(content) > 1 and not wrong:
				i.delete(0, END)
				i.insert(0, content.strip().replace(ebox[row][column].get().strip(), ''))
		for i in refreshc:
			content = i.get()
			if content == ebox[row][column].get() and ebox[row][column].get() and i != ebox[row][column]:
				wrong = True
				break
			if len(content) > 1 and not wrong:
				i.delete(0, END)
				i.insert(0, content.strip().replace(ebox[row][column].get().strip(), ''))
		for i in box_place[0]:
			for j in box_place[1]:
				if ebox[i][j] != ebox[row][column]:
					content = ebox[i][j].get()
					if content == ebox[row][column].get() and ebox[row][column].get():
						wrong = True
						break
					if len(content) > 1 and not wrong:
						ebox[i][j].delete(0, END)
						ebox[i][j].insert(0, content.strip().replace(ebox[row][column].get().strip(), ''))
		if wrong:
			ebox[row][column].config(bg='red')
		else:
			ebox[row][column].config(bg='#DDDDDD')
	content = e.widget.get()
	e.widget.delete(0, END)
	e.widget.insert(0, ''.join(sorted(list(set(list(content))))))

#entrybox
ebox = []
for i in range(9):
	ebox.append([])
	for i2 in range(9):
		ebox[i].append(Entry(root, relief=FLAT, bg='white', justify=CENTER, font=numfont, fg='black'))
root.bind('<Button-1>', checkclick)
[[j.bind('<KeyRelease>', refresh) for j in i] for i in ebox]

y = 22

ebox[0][0].place(x=42, y=21.5, width=88, height=88)
ebox[0][1].place(x=131, y=21.5, width=89, height=88)
ebox[0][2].place(x=221, y=21.5, width=88, height=88)
ebox[1][0].place(x=42, y=111, width=88, height=89)
ebox[1][1].place(x=131, y=111, width=89, height=89)
ebox[1][2].place(x=221, y=111, width=88, height=89)
ebox[2][0].place(x=42, y=201, width=88, height=88)
ebox[2][1].place(x=131, y=201, width=89, height=88)
ebox[2][2].place(x=221, y=201, width=88, height=88)

ebox[3][0].place(x=42, y=292, width=88, height=88)
ebox[3][1].place(x=131, y=292, width=89, height=88)
ebox[3][2].place(x=221, y=292, width=88, height=88)
ebox[4][0].place(x=42, y=381, width=88, height=89)
ebox[4][1].place(x=131, y=381, width=89, height=89)
ebox[4][2].place(x=221, y=381, width=88, height=89)
ebox[5][0].place(x=42, y=471, width=88, height=88)
ebox[5][1].place(x=131, y=471, width=89, height=88)
ebox[5][2].place(x=221, y=471, width=88, height=88)

ebox[6][0].place(x=42, y=562, width=88, height=88)
ebox[6][1].place(x=131, y=562, width=89, height=88)
ebox[6][2].place(x=221, y=562, width=88, height=88)
ebox[7][0].place(x=42, y=651, width=88, height=89)
ebox[7][1].place(x=131, y=651, width=89, height=89)
ebox[7][2].place(x=221, y=651, width=88, height=89)
ebox[8][0].place(x=42, y=741, width=88, height=88)
ebox[8][1].place(x=131, y=741, width=89, height=88)
ebox[8][2].place(x=221, y=741, width=88, height=88)

ebox[0][3].place(x=312, y=21.5, width=88, height=88)
ebox[0][4].place(x=401, y=21.5, width=89, height=88)
ebox[0][5].place(x=491, y=21.5, width=88, height=88)
ebox[1][3].place(x=312, y=111, width=88, height=89)
ebox[1][4].place(x=401, y=111, width=89, height=89)
ebox[1][5].place(x=491, y=111, width=88, height=89)
ebox[2][3].place(x=312, y=201, width=88, height=88)
ebox[2][4].place(x=401, y=201, width=89, height=88)
ebox[2][5].place(x=491, y=201, width=88, height=88)

ebox[3][3].place(x=312, y=292, width=88, height=88)
ebox[3][4].place(x=401, y=292, width=89, height=88)
ebox[3][5].place(x=491, y=292, width=88, height=88)
ebox[4][3].place(x=312, y=381, width=88, height=89)
ebox[4][4].place(x=401, y=381, width=89, height=89)
ebox[4][5].place(x=491, y=381, width=88, height=89)
ebox[5][3].place(x=312, y=471, width=88, height=88)
ebox[5][4].place(x=401, y=471, width=89, height=88)
ebox[5][5].place(x=491, y=471, width=88, height=88)

ebox[6][3].place(x=312, y=562, width=88, height=88)
ebox[6][4].place(x=401, y=562, width=89, height=88)
ebox[6][5].place(x=491, y=562, width=88, height=88)
ebox[7][3].place(x=312, y=651, width=88, height=89)
ebox[7][4].place(x=401, y=651, width=89, height=89)
ebox[7][5].place(x=491, y=651, width=88, height=89)
ebox[8][3].place(x=312, y=741, width=88, height=88)
ebox[8][4].place(x=401, y=741, width=89, height=88)
ebox[8][5].place(x=491, y=741, width=88, height=88)

ebox[0][6].place(x=582, y=21.5, width=88, height=88)
ebox[0][7].place(x=671, y=21.5, width=89, height=88)
ebox[0][8].place(x=761, y=21.5, width=88, height=88)
ebox[1][6].place(x=582, y=111, width=88, height=89)
ebox[1][7].place(x=671, y=111, width=89, height=89)
ebox[1][8].place(x=761, y=111, width=88, height=89)
ebox[2][6].place(x=582, y=201, width=88, height=88)
ebox[2][7].place(x=671, y=201, width=89, height=88)
ebox[2][8].place(x=761, y=201, width=88, height=88)

ebox[3][6].place(x=582, y=292, width=88, height=88)
ebox[3][7].place(x=671, y=292, width=89, height=88)
ebox[3][8].place(x=761, y=292, width=88, height=88)
ebox[4][6].place(x=582, y=381, width=88, height=89)
ebox[4][7].place(x=671, y=381, width=89, height=89)
ebox[4][8].place(x=761, y=381, width=88, height=89)
ebox[5][6].place(x=582, y=471, width=88, height=88)
ebox[5][7].place(x=671, y=471, width=89, height=88)
ebox[5][8].place(x=761, y=471, width=88, height=88)

ebox[6][6].place(x=582, y=562, width=88, height=88)
ebox[6][7].place(x=671, y=562, width=89, height=88)
ebox[6][8].place(x=761, y=562, width=88, height=88)
ebox[7][6].place(x=582, y=651, width=88, height=89)
ebox[7][7].place(x=671, y=651, width=89, height=89)
ebox[7][8].place(x=761, y=651, width=88, height=89)
ebox[8][6].place(x=582, y=741, width=88, height=88)
ebox[8][7].place(x=671, y=741, width=89, height=88)
ebox[8][8].place(x=761, y=741, width=88, height=88)

def bignum(e, lol):
	i = [r for r in range(len(ebox)) if e.widget in ebox[r]][0]
	j = ebox[i].index(e.widget)
	status[i][j] = 0
	ebox[i][j].delete(0, END)
	ebox[i][j].insert(END, str(lol))
	ebox[i][j].config(font=numfont)

def smallnum(e, lol):
	i = [r for r in range(len(ebox)) if e.widget in ebox[r]][0]
	j = ebox[i].index(e.widget)
	status[i][j] = 1
	ebox[i][j].config(font=smallnumfont)
	ebox[i][j].insert(END, str(lol))

for k in range(1, 10):
	[[j.bind(str(k), lambda e, lol=k: bignum(e, lol)) for j in i] for i in ebox]
	[[j.bind('<Control-Key-'+str(k)+'>', lambda e, lol=k: smallnum(e, lol)) for j in i] for i in ebox]

def clear():
	for i in range(9):
		for i2 in range(9):
			ebox[i][i2].delete(0, END)
	button.config(state=NORMAL)
	for i in range(9):
		for i2 in range(9):
			ebox[i][i2].config(bg='white', disabledbackground='white')
	
def imports():
	global starttime
	button.config(state=NORMAL)
	root.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes=[('Sudoku Files', '.sudoku')])
	if not root.filename:
		return
	winmessage.place_forget()
	reader = open(root.filename, 'r')
	lol = reader.readlines()
	for i in range(len(lol)):
		lol[i] = list(lol[i].replace('\n', ''))
	for i in range(9):
		for i2 in range(9):
			ebox[i][i2].config(state=NORMAL)
			lol[i][i2] = '' if lol[i][i2] == '0' else lol[i][i2]
			ebox[i][i2].delete(0, END)
			ebox[i][i2].insert(END, lol[i][i2])
			lol[i][i2] = '0' if lol[i][i2] == '' else lol[i][i2]
			ebox[i][i2].config(disabledforeground='#00A6FF', stat=DISABLED, disabledbackground='white') if lol[i][i2] != '0' else 0
	for i in range(9):
		for i2 in range(9):
			ebox[i][i2].config(bg='white', disabledbackground='white')
	starttime = time.time()

def exports():
	global board
	f = filedialog.asksaveasfilename(defaultextension=".sudoku" ,filetypes=[('Sudoku Files', '.sudoku')])
	if not f:
		return
	text2save = 'shit'
	f = open(f, 'w')
	for i in board:
		for i2 in i:
			f.write(str(i2))
		f.write('\n')
	f.close()

def new():
	global counterrun
	global board
	global starttime
	global answer
	global winmessage, board, button, starttime, counterrun, answer, ebox, inittab, diff, blank_board, status
	titlefont = Font(size=60, family='Bahnschrift Bold')
	btnfont = Font(size=30, family='Bahnschrift')
	inittab = Frame(root, width=1120, height=900, bg='white')

	def start(difficulty):

		global winmessage, board, button, starttime, counterrun, answer, ebox, inittab, diff, blank_board, status

		diff = 'elementary' if difficulty == 1 else 'intermediate' if difficulty == 10 else 'advanced' if difficulty == 20 else 'daily' if difficulty == 999 else ''
		
		winmessage.place_forget()
		if difficulty != 999:
			board  = gensudoku(difficulty)
			blank_board = board
		else:
			option = Options()
			option.add_argument('--headless')
			driver = webdriver.Chrome(options=option)
			driver.get('http://dailysudoku.com/cgi-bin/sudoku/get_board.pl')
			board = json.loads(driver.find_element_by_tag_name('body').get_attribute('innerHTML'))['numbers'].replace('.', '0')
			board = [board[x:x+9] for x in range(0, len(board), 9)]
			board = [[int(j) for j in list(i)] for i in board]
			blank_board = board
			driver.close()
			driver.quit
		button.config(state=NORMAL)
		starttime = time.time()
		counterrun = True

		base = 3
		side = 9

		inittab.place_forget()

		reader = open('answer.sudoku', 'r')
		answer = [list(i.replace('\n', '')) for i in reader.readlines()]
		status = [[0 for i in range(9)] for j in range(9)]

		for i in range(9):
			for i2 in range(9):
				ebox[i][i2].config(state=NORMAL, font=numfont)
				board[i][i2] = '' if board[i][i2] == 0 else board[i][i2]
				ebox[i][i2].delete(0, END)
				ebox[i][i2].insert(END, board[i][i2])
				board[i][i2] = 0 if board[i][i2] == '' else board[i][i2]
				ebox[i][i2].config(disabledforeground='#00A6FF', stat=DISABLED, disabledbackground='white') if board[i][i2] != 0 else 0

	def button_enter(e):
		if e.widget in [beginnerbutton, intermediatebutton, advancedbutton, dailybutton]:
			e.widget.config(bg='#00A6FF', fg='white')
	def button_leave(e):
		if e.widget in [beginnerbutton, intermediatebutton, advancedbutton, dailybutton]:
			e.widget.config(bg='white', fg='#00A6FF')
	
	bf = []
	for i in range(4):
		bf.append(Frame(inittab, bg='#00A6FF'))
	inittab.place(x=560, y=450, anchor='center')
	title = Label(inittab, text=' THE SUDOKU', bg='white', fg='#00A6FF', font=titlefont)
	title.place(x=560, y=250, anchor='center')
	beginnerbutton = Button(inittab, text='ELEMENTARY', bg='white', fg='#00A6FF', font=btnfont, command=lambda: start(1), relief=FLAT)
	intermediatebutton = Button(inittab, text='INTERMEDIATE', bg='white', fg='#00A6FF', font=btnfont, relief=FLAT, command=lambda: start(10))
	advancedbutton = Button(inittab, text='ADVANCED', bg='white', fg='#00A6FF', font=btnfont, relief=FLAT, command=lambda: start(20))
	dailybutton = Button(inittab, text='DAILY', bg='white', fg='#00A6FF', font=btnfont, relief=FLAT, command=lambda: start(999))
	beginnerbutton.place(x=560, y=380, anchor='center', height=70, width=350)
	intermediatebutton.place(x=560, y=480, anchor='center', height=70, width=350)
	advancedbutton.place(x=560, y=580, anchor='center', height=70, width=350)
	dailybutton.place(x=560, y=680, anchor='center', height=70, width=350)
	bf[0].place(x=560, y=380, anchor='center', height=74, width=354)
	bf[1].place(x=560, y=480, anchor='center', height=74, width=354)
	bf[2].place(x=560, y=580, anchor='center', height=74, width=354)
	bf[3].place(x=560, y=680, anchor='center', height=74, width=354)

	root.bind('<Enter>', button_enter)
	root.bind('<Leave>', button_leave)

def check():

	global counterrun, diff

	checklstr = []
	checklstc = []
	counterrun = True
	
	for i in range(9):
		checklstr.append([])
		checklstc.append([])
		for i2 in range(9):
			fixnum = ebox[i][i2].get()
			checklstc[i].append(ebox[i2][i].get())
			if fixnum == '':
				checklstr[i].append(0)
			else:
				checklstr[i].append(int(fixnum))

	checklstc = [[0 if checklstc[i][i2]=='' else int(checklstc[i][i2]) for i2 in range(9)] for i in range(9)]


	box = []
	count = 0
	count2 = 0
	count3 = 0
	for i4 in range(3):
		for i3 in range(3):
			box.append([])
			for i in range(3):
				for i2 in range(3):
					box[count3].append(checklstr[i+count2][i2+count])
			count+=3
			count3+=1
		count2+=3
		count=0

	win = True
		
	for i in checklstr:
		if list(sorted(i)) != [1,2,3,4,5,6,7,8,9]:
			win = False
	for i in checklstc:
		if list(sorted(i)) != [1,2,3,4,5,6,7,8,9]:
			win = False
	for i in box:
		if list(sorted(i)) != [1,2,3,4,5,6,7,8,9]:
			win = False
	if not all(all(not bool(j) for j in i) for i in status):
		win = False

	if win == True:
		winmessage.config(fg='#BDF000', text='COMPLETED')
		winmessage.place(anchor='center', x=990, y=790)
		counterrun = False
		for i in range(9):
			for i2 in range(9):
				ebox[i][i2].config(disabledbackground='white', background='white')
		print('YOU WIN')
		board = checklstr
		base = 3
		side = 9

		for i in range(9):
			for i2 in range(9):
				ebox[i][i2].config(state=NORMAL)
				ebox[i][i2].delete(0, END)
				ebox[i][i2].insert(END, board[i][i2])
				ebox[i][i2].config(disabledforeground=maincolor, stat=DISABLED, disabledbackground='white') if board[i][i2] != 0 else 0

		for i in range(9):
			for i2 in range(9):
				ebox[i][i2].config(state=NORMAL)
				ebox[i][i2].delete(0, END)
				ebox[i][i2].insert(END, board[i][i2])
				ebox[i][i2].config(disabledforeground=maincolor, stat=DISABLED, disabledbackground='white') if board[i][i2] != 0 else 0

		line0  = expandLine("ÉÍÍÍÑÍÍÍËÍÍÍ»")
		line1  = expandLine("º . ³ . º . º")
		line2  = expandLine("ÇÄÄÄÅÄÄÄ×ÄÄÄ¶")
		line3  = expandLine("ÌÍÍÍØÍÍÍÎÍÍÍ¹")
		line4  = expandLine("ÈÍÍÍÏÍÍÍÊÍÍÍ¼")

		symbol = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		nums   = [ [""]+[symbol[n] for n in row] for row in blank_board ]

		def deleteLine():
			fn = 'history.bat'
			f = open(fn)
			output = []
			str1="pause"
			for line in f:
				if not line.startswith(str1):
					output.append(line)
			f.close()
			f = open(fn, 'w')
			f.writelines(output)
			f.close()
		deleteLine()
		
		writer = open('history.bat', 'a')
		writer.write('\n@ echo off\n')
		writer.write('echo puzzle:\n')
		writer.write('echo '+line0+'\n')
		for r in range(1,side+1):
			writer.write('echo '+("".join(n+s for n,s in zip(nums[r-1],line1.split("."))))+'\n')
			writer.write('echo '+[line2,line3,line4][(r%side==0)+(r%base==0)]+'\n')
		writer.write('echo.\n')
		writer.close()

		symbol = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		nums   = [ [""]+[symbol[n] for n in row] for row in board ]

		def deleteLine():
			fn = 'history.bat'
			f = open(fn)
			output = []
			str1="pause"
			for line in f:
				if not line.startswith(str1):
					output.append(line)
			f.close()
			f = open(fn, 'w')
			f.writelines(output)
			f.close()
		deleteLine()
		
		writer = open('history.bat', 'a')
		writer.write('\n')
		writer.write('echo answer:\n')
		writer.write('echo '+line0+'\n')
		for r in range(1,side+1):
			writer.write('echo '+("".join(n+s for n,s in zip(nums[r-1],line1.split("."))))+'\n')
			writer.write('echo '+[line2,line3,line4][(r%side==0)+(r%base==0)]+'\n')
		writer.write('echo.\n')
		writer.write('echo Completed: ' + formattime() + '\n')
		writer.write('echo Time Used: ' + timeused + '\n')
		writer.write('echo Difficulty: '+ diff + '\n')
		writer.write('echo.\n')
		writer.write('pause > nul\n')
		writer.close()
	else:
		print('STUPID')
		winmessage.place_forget()
		winmessage.config(fg='#FF889D', text='ERROR')
		winmessage.place(anchor='center', x=990, y=790)
		root.update()
		time.sleep(1)
		root.update()
		winmessage.place_forget()

maincolor = '#00A6FF'

def settings():
	global settingsframeframe, settingsframe, okframe, okbtn, colorInput, maincolor, maincanvas, ebox, counterrun, starttime, counttime
	counterrun = False

	def donesettings():
		global settingsframeframe, settingsframe, okframe, okbtn, colorInput, maincolor, maincanvas, ebox, counterrun, starttime, counttime
		counterrun = True
		starttime = time.time() - counttime
		settingsframeframe.place_forget()
		settingsframe.place_forget()
		okframe.place_forget()
		okbtn.place_forget()
		try:
			if len(colorInput.get()) == 7 and colorInput.get().startswith('#'):
				for i in range(7):
					bf[i].config(bg=colorInput.get())
				buttonnew.config(fg=colorInput.get())
				button.config(fg=colorInput.get())
				buttonc.config(fg=colorInput.get())
				buttoncheck.config(fg=colorInput.get())
				buttoni.config(fg=colorInput.get())
				buttone.config(fg=colorInput.get())
				buttonsettings.config(fg=colorInput.get())
				timecounter.config(fg=colorInput.get())
				maincolor = colorInput.get()
				maincanvas.delete('all')
				topLeft_x=10
				topLeft_y=820

				intDim=90
				for row in range(0,10):
					if (row%3)==0:
						size = 3
					else:
						size = 1
					maincanvas.create_line(topLeft_x, topLeft_y-row*intDim, topLeft_x+9*intDim, topLeft_y-row*intDim, width=size, fill=maincolor)
				for col in range(0,10):
					if (col%3)==0:
						size = 3
					else:
						size = 1   
					maincanvas.create_line(topLeft_x+col*intDim, topLeft_y, topLeft_x+col*intDim, topLeft_y-9*intDim, width=size, fill=maincolor)

				for i in range(9):
					for i2 in range(9):
						ebox[i][i2].config(disabledforeground=maincolor)
		except:
			pass
		main()
	
	settingsframeframe = Frame(root, bg=maincolor, width=806, height=806)
	settingsframe = Frame(root, bg='white', width=800, height=800)
	okframe = Frame(root, bg=maincolor)
	okbtn = Button(root, text='OK', font=buttonfont, command=donesettings, bg='white', fg=maincolor, relief=FLAT)
	settingsframeframe.place(x=560, y=450, anchor='center')
	settingsframe.place(x=560, y=450, anchor='center')
	okbtn.place(x=560, y=700, width=200, height=60, anchor='center')
	okframe.place(x=560, y=700, width=204, height=64, anchor='center')
	colorLabel = Label(settingsframe, text='main color: ', bg='white', font=buttonfont)
	colorInput = Entry(settingsframe, font=buttonfont, relief=FLAT, highlightbackground='black', width=9, highlightcolor='black', highlightthickness=2, justify=CENTER)
	colorshow = Canvas(settingsframe, height=37, width=37, highlightbackground='black')
	colorLabel.place(x=50, y=20)
	colorInput.place(x=200, y=20)
	colorshow.place(x=350, y=20)
	colorInput.insert(END, maincolor)

	while True:
		try:
			root.update()
			if len(colorInput.get()) == 7 and colorInput.get().startswith('#'):
				colorshow.config(bg=colorInput.get())
		except:
			break

bf = []

for i in range(7):
	bf.append(Frame(root, bg='#00A6FF'))
buttonnew = Button(root, text='NEW', command=new, font=buttonfont, bg='white', fg='#00A6FF', relief=FLAT)
button = Button(root, text='GET', command=sort, font=buttonfont, bg='white', fg='#00A6FF', relief=FLAT)
buttonc = Button(root, text='CLEAR', command=clear, font=buttonfont, bg='white', fg='#00A6FF', relief=FLAT)
buttoncheck = Button(root, text='CHECK', command=check, font=buttonfont, bg='white', fg='#00A6FF', relief=FLAT)
buttoni = Button(root, text='CONTINUE', command=imports, font=buttonfont, bg='white', fg='#00A6FF', relief=FLAT)
buttone = Button(root, text='SAVE', command=exports, font=buttonfont, bg='white', fg='#00A6FF', relief=FLAT)
buttonsettings  = Button(root, text='SETTINGS', command=settings, font=buttonfont, bg='white', fg='#00A6FF', relief=FLAT)
timecounter = Label(root, font=counterfont, bg='white', fg='#00A6FF')
winmessage = Label(root, text='COMPLETED', font=winfont, bg='white', fg='#BDF000')

buttonnew.place(x=890, y=20, width=200, height=60)
button.place(x=890, y=110, width=200, height=60)
buttonc.place(x=890, y=200, width=200, height=60)
buttoncheck.place(x=890, y=290, width=200, height=60)
buttoni.place(x=890, y=380, width=200, height=60)
buttone.place(x=890, y=470, width=200, height=60)
buttonsettings.place(x=890, y=560, width=200, height=60)

bf[0].place(x=888, y=18, width=204, height=64)
bf[1].place(x=888, y=108, width=204, height=64)
bf[2].place(x=888, y=198, width=204, height=64)
bf[3].place(x=888, y=288, width=204, height=64)
bf[4].place(x=888, y=378, width=204, height=64)
bf[5].place(x=888, y=468, width=204, height=64)
bf[6].place(x=888, y=558, width=204, height=64)
timecounter.place(anchor='center', x=990, y=700)

new()

hour = 0
minute = 0
second = 0
counterrun = False

def counttimer():
	global timeused
	global counttime
	if counterrun == True:
		counttime = int(time.time()-starttime)
		timeused = str(datetime.timedelta(seconds=counttime))
		timecounter.config(text=timeused)
		timecounter.update()

def main():
	while True:
		counttimer()
		timecounter.update()
		try:
			for i in range(9):
				for i2 in range(9):
					if ebox[i][i2]['bg'] == '#DDDDDD' and ebox[i][i2]['bg'] != 'red':
						for a in range(9):
							for a2 in range(9):
								if ebox[a][a2] != eboxc:
									ebox[a][a2].config(bg='white', disabledbackground='white')
								if ebox[i][i2].get() == ebox[a][a2].get() and ebox[i][i2].get() != '' and ebox[a][a2]['bg'] != 'red':
									ebox[a][a2].config(bg='#DDDDDD', disabledbackground='#DDDDDD')
					if '0' in ebox[i][i2].get() or len(ebox[i][i2].get()) > 10:
						txt = ebox[i][i2].get()[:-1]
						ebox[i][i2].delete(0, END)
						ebox[i][i2].insert(0, txt)
					try:
						int(ebox[i][i2].get())
					except:
						txt = ebox[i][i2].get()[:-1]
						ebox[i][i2].delete(0, END)
						ebox[i][i2].insert(0, txt)
					if len(ebox[i][i2].get().strip()) > 9:
						txt = ebox[i][i2].get()[:-1]
						ebox[i][i2].delete(0, END)
						ebox[i][i2].insert(0, txt)
					if not status[i][i2] and len(ebox[i][i2].get().strip()) > 1:
						txt = ebox[i][i2].get()[:-1]
						ebox[i][i2].delete(0, END)
						ebox[i][i2].insert(0, txt)
			root.update()
		except:
			pass
	
main()
root.mainloop()