import tkinter, Rules, File, os
from tkinter import messagebox

# sets the value of our global varibles#
board = None                           #
window = None                          #
########################################

def set_up_window():
    global window # makes vaible window global so we can use it anywhere
    window = tkinter.Tk() # creates a tkinter window
    window.title('chess') # gives the window a title 
    window.tk.call('wm', 'iconphoto', window._w, tkinter.PhotoImage(file = Rules.path +'icon.gif')) # gives the window an image icon
    # calls starting functions #
    start(window)              #
    menu(window)               #
    ############################
    window.mainloop() # end of code

def start(window): # this function creates the starting page
    photo = tkinter.PhotoImage(file = Rules.path + "Intro.gif") # sets 'intro.gif' as the background image we are to put on the window
    ########## places image on window ##########
    w = tkinter.Label(window, image = photo)   #
    w.image = photo                            #
    w.pack()                                   #
    ############################################

def play_chess(window): # the function that calls other functions to run our game
    global board # makes vaible board global so we can use it anywhere
    # calls chess_game functions #
    destroy_all_widgets(window)  #
    menu(window)                 #
    board = reset_board()        # gets the list of the board to layout_board
    layout_board(window, board)  #
    ##############################

def menu(window): # this function hold the menubar on starting screen
    
    menubar = tkinter.Menu(window) # creates menubar
 
    filemenu = tkinter.Menu(menubar, tearoff = 0)
    editmenu = tkinter.Menu(menubar, tearoff = 0)
    viewmenu = tkinter.Menu(menubar, tearoff = 0 )
    toolmenu = tkinter.Menu(menubar, tearoff = 0)
    helpmenu = tkinter.Menu(menubar, tearoff = 0)

    filemenu.add_command(label="New", command = lambda: play_chess(window)) #starts chess game
    filemenu.add_command(label="Open", command = lambda: File.onOpen(window, board))
    filemenu.add_command(label="Save", command = lambda: File.onSave(board))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command = lambda: window.destroy())

    editmenu.add_command(label="custormise pieces", command = lambda:  File.openGuide())
    editmenu.add_command(label="custormise board", command = lambda:  File.openGuide())
    editmenu.add_checkbutton(label='Blindfold Chess', command = lambda:  File.openGuide())
    
    viewmenu.add_checkbutton(label='points', command = lambda:  File.openGuide())
    viewmenu.add_checkbutton(label='pieces taken', command = lambda:  File.openGuide())
    viewmenu.add_checkbutton(label='computer evaluation', command = lambda:  File.openGuide())
    viewmenu.add_command(label="game history", command = lambda:  File.openGuide())

    toolmenu.add_command(label="takeback", command = lambda:  File.openGuide())
    toolmenu.add_command(label="flip board", command = lambda:  File.openGuide())
    toolmenu.add_command(label="Request stalemate", command = lambda:  File.openGuide())
    toolmenu.add_command(label="Resighn", command = lambda:  File.openGuide())
    toolmenu.add_command(label="hint", command = lambda:  File.openGuide())

    helpmenu.add_command(label="Open Guide", command = lambda:  File.openGuide())

    menubar.add_cascade(label="File", menu = filemenu)
    menubar.add_cascade(label="Edit", menu = editmenu)
    menubar.add_cascade(label="View", menu = viewmenu)
    menubar.add_cascade(label="Tools", menu = toolmenu)
    menubar.add_cascade(label="Help", menu = helpmenu)
    
    window.config(menu = menubar)
    ##img1 = tkinter.PhotoImage(Rules.path+'icon.png')
    ##b = tkinter.Button(menubar, image=img1, width=6)
    ##b.image = img1
    ##b.pack(side=tkinter.RIGHT)

def destroy_all_widgets(window): # closes everything on start screen but menubar
    for widget in window.winfo_children():
        if widget.winfo_class() != 'menubar':
            widget.destroy()

def mssg_bar(window, mssg): # this function shows information about the game at the botum of the screen  
    messageLabel = tkinter.Label(window, text = mssg) # creates mssg_bar
    messageLabel.grid(row=9, column=3 , columnspan = 5, sticky = tkinter.N+tkinter.S+tkinter.W+tkinter.E) # places mssg bar on screen as part of the grid


def reset_board(): # resets the game to the begining
    board = [] # creates a list of where we will later
    for row in range(0,8):
        rowlist = []
        for column in range(0,8):
            ##for board_list in range(8, 0) #for balck (0, 8) for white
            if row == 6:
                rowlist.append(Rules.Pawn('Pawn', Rules.path+'White_Pawn.gif', 'white', column, row))
            elif row == 1:
                rowlist.append(Rules.Pawn('Pawn', Rules.path+'Black_Pawn.gif', 'black', column, row))
            else:
                rowlist.append(None)
        board.append(rowlist)
    return board

def layout_board(window, board):
    bttnclr=Rules.light_bttnlcr
    for column_number in range(0, len(board)):
        for row_number in range(0, len(board[column_number])):
            if board[row_number][column_number] == None:
                square = tkinter.Label(window, text = "                 \n\n\n", bg = bttnclr)
            else:
                img = tkinter.PhotoImage(file = board[row_number][column_number].icon)
                square = tkinter.Label(window, bg = bttnclr, image = img)
                square.image = img

            if bttnclr == "white":
                bttnclr = "grey"
            else:
                bttnclr = "white"

            square.grid(row = row_number, column = column_number, sticky = tkinter.N+tkinter.S+tkinter.W+tkinter.E)
            square.bind("<Button-1>", on_click)

        if bttnclr == "white":
            bttnclr = "grey"
        else:
            bttnclr = "white"

    mssg_turn = ''
    mssg = ''

    if Rules.turn == 0:
        mssg_turn  = 'White\'s Move'
    else:
        mssg_turn  = 'Black\'s Move'  
    
    mssg_bar(window, mssg)
    turnLabel = tkinter.Label(window, text = mssg_turn)
    turnLabel.grid(row=9, column=0 , columnspan = 2, sticky = tkinter.N+tkinter.S+tkinter.W+tkinter.E)
    
def on_click(event):
    square = event.widget
    Rules.onclick += 1 # a bit tidier than rules.onclick = rules.onclick + 1
    row_number = int(square.grid_info()["row"])
    column_number  = int(square.grid_info()["column"])
    # lets save our row and column numbers in a tuple here, rather than in several places
    square_clicked = (row_number, column_number)
    piece_clicked = board[row_number][column_number]
    try:
        if ((Rules.onclick == 1 and ((Rules.turn == 0 and piece_clicked.colour == 'white') or (Rules.turn == 1 and piece_clicked.colour == 'black'))) or Rules.onclick == 2):            
            if Rules.onclick == 1:
                square.config(bg='blue')
                mssg = "Where would you like to move your " + piece_clicked.piece + " to!"
                Rules.old_colour = piece_clicked.colour
                # you're not actually saving the piece, you're saving the square that has been clicked
                Rules.square_clicked = square_clicked #row_number,column_number
                mssg_bar(window, mssg)
                return
            else:
                if piece_clicked == None: #nothing at the square we're moving to
                    move_piece = True
                else:#click a square with piece on
                    if (isinstance(piece_clicked, Rules.GameObject) and Rules.old_colour != piece_clicked.colour): # check were not tacking the same colour piece
                        move_piece = True
                    else:
                        tkinter.messagebox.showinfo("Move Not Allowed", "You can not take your own piece!")
                        mssg = "You can not take your own piece!"
                        move_piece = False
                        mssg_bar(window, mssg)

                if move_piece == True:
                    if board[row_number][column_number] == None:
                        attacking = False
                    else:
                        attacking = True
                    print(attacking)
                    check_move = board[Rules.square_clicked[0]][Rules.square_clicked[1]].check_move(square_clicked, attacking)
                    if check_move == True : #checks rules ## did not have == True on end
                        board[row_number][column_number] = board[Rules.square_clicked[0]][Rules.square_clicked[1]]#moves piece there
                        # new line of code below
                        board[row_number][column_number].move_piece(square_clicked) # update our piece with its new position
                        board[Rules.square_clicked[0]][Rules.square_clicked[1]] = None # sets square was at to None
                        # reset our click counter - 
                        Rules.onclick = 0
                        #change turn
                        if Rules.turn == 0:
                            Rules.turn = 1
                        else:
                            Rules.turn = 0
                    else:
                        tkinter.messagebox.showinfo("Move Not Allowed", check_move)
                        mssg_bar(window, check_move)
                    # stop
                    move_piece = False

        layout_board(window, board) # tkinter grid to board list

    except:
        if Rules.onclick == 1:
            tkinter.messagebox.showinfo("Move Not Allowed","Your/No piece there, try again")
            mssg = 'Your/No piece there, try again'
            mssg_bar(window, mssg)
        else:
            tkinter.messagebox.showerror("Error","An error has ocurred!")
            mssg = "An error has ocurred!"
            mssg_bar(window, mssg)
        raise
    Rules.onclick = 0



if __name__ =="__main__":
    set_up_window()

# Globals #
#could be replaced with Chess.________ 
#______ being varible name
