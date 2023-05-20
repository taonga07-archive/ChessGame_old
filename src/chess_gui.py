from pygame import QUIT, RESIZABLE, VIDEORESIZE, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE
from pygame.display import flip, set_caption, set_mode, set_icon
from pygame.mouse import get_pos as get_mouse_pos
from socket import create_connection, socket, SOCK_STREAM, AF_INET
from pygame.image import load as load_image
from pygame.event import get as get_events
from pygame.draw import rect as draw_rect
from pygame import init as pygame_init
# from pygame._sdl2 import messagebox
from json import loads as json_loads
from pygame.transform import scale
from sys import exit as sys_exit
from requests import get
from io import BytesIO
from time import sleep
from math import ceil


class ChessGUI():
    def __init__(self, colours=[[50.2]*3, [255]*3], ) -> None:
        self.piece_images = load_image(BytesIO(get(URL+"pieces.svg").content))
        self.window_icon = load_image(BytesIO(get(URL+"icon.png").content))
        self.board_colours = colours#, self.chessgame.board = colours, board
        self.window = set_mode((400,400), RESIZABLE)
        self.conn = socket(AF_INET, SOCK_STREAM)
        self.pieces = self.squares = {}
        self.connected = False
        self.msg_id = 0

    def __call__(self) -> None:
        "main game loop for the GUI"
        set_icon(self.window_icon), set_caption("ChessGame"), self.window.fill([178]*3)
        self.window.blit(scale(self.window_icon, self.window.get_size()), [0,0])
        flip(), sleep(0.75), self.window.fill([255]*3), flip()
        self.create_socket_connection()
        while self.connected:
            recvied_data_sting = self.conn.recv(1024)
            recvied_data_decode = recvied_data_sting.decode("utf-8")
            print(recvied_data_sting)
            recvied_data = json_loads(recvied_data_decode) if recvied_data_decode is not None else None
            if (recvied_data["highlighted_squares"] == recvied_data["pieces"]) is not None:
                for event in get_events():
                    if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == QUIT): sys_exit()
                    if event.type == MOUSEBUTTONDOWN:
                        for square_id, square in enumerate(self.squares):
                            if square.collidepoint(get_mouse_pos()):
                                print(square_id)
                    if event.type == VIDEORESIZE:
                        self.update_board(recvied_data["pieces"], recvied_data["highlighted_squares"])
                    if recvied_data["msg_id"] > self.msg_id:
                        self.update_board(recvied_data["pieces"], recvied_data["highlighted_squares"])
                        self.msg_id = recvied_data["msg_id"]
                flip()

    def update_board(self, pieces, highlighted_squares={}) -> None:
        "Draws the board and pieces while updating the their dictionaries to match the new board"
        square_size, image_size = ceil(min(self.window.get_size()))/8, (self.piece_images.get_width()/6, self.piece_images.get_height()/2)
        self.squares = [draw_rect(self.window, (self.board_colours[(x+y)%2] if (8*x)+y not in highlighted_squares.keys() else highlighted_squares[(8*x)+y]), [square_size*y,square_size*x]+[square_size]*2) for x in range(8) for y in range(8)]
        self.pieces = [self.window.blit(scale(self.piece_images.subsurface([image_size[0]*piece[0], image_size[1]*piece[1]], image_size), [square_size]*2), [square_size*x for x in piece[2]]) for piece in pieces]

    def create_socket_connection(self, port=5555) -> None:
        "Creates a socket connection to the server"
        server = self.conn.connect(("localhost", port))
        if server is False: # connection failed to server
            server = self.conn.connect(("192.168.1.255", port))
            if server is False: # connection failed to differnt server
                self.conn.close()
        self.connected = True
        return server

URL = "https://raw.githubusercontent.com/Taonga07/ChessGame/master/resources/"

if __name__== "__main__":
    pygame_init()
    ChessGUI()()