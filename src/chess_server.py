from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SO_SNDBUF
from chess_headless import HeadlessChess
from os.path import join, dirname
from json import loads, load, dumps, dump
from requests import get
import threading
import sys

class Server():
    def __init__(self, port=5555) -> None:
        self.host, self.port = "localhost", port
        self.server_active, self.games = True, []

    def __call__(self) -> None:
        self.start_sock()
        self.client_handler()

    def start_sock(self) -> None:
        self.sock_server = socket(AF_INET, SOCK_STREAM)
        self.sock_server.setsockopt(SOL_SOCKET, SO_SNDBUF, 8096)
        self.sock_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock_server.bind(("", self.port))
        self.sock_server.listen(True)

    def client_handler(self) -> None:
        players, connected_players = [], 0
        addr = f"tcp://127.0.0.1:{self.port}"
        print(f"\nWaiting for a connection on {addr}")
        while self.server_active:
            try:
                while True:
                    for i in range(2):
                        connected_players += 1
                        connection = self.sock_server.accept()
                        players.append((connection, connected_players))
                        if (i == 1) and (len(players) == 2): 
                            self.games.append(ChessGame(players))
                            self.games[-1].start()
                    players = []
            except KeyboardInterrupt:
                print("\nShutting down server")
                for game, _  in enumerate(self.games):
                    self.games[game].active = False
                self.server_active = False
        self.sock_server.close()
        sys.exit()

class ChessGame(threading.Thread, HeadlessChess):
    def __init__(self, clients) -> None:
        threading.Thread.__init__(self)
        HeadlessChess.__init__(self)
        self.players = [threading.Thread(target=self.player, args=clients[i]) for i in range(2)]
        self.active, self.player_turn = True, 0

    def run(self):
        print("chessgame started")
        [player.start() for player in self.players]
        while self.active:
            pass

    def player(self, connection, ID):
        print(f" ... connection established from {connection[1]}", flush=True)
        active, waiting, mssg_id = True, True, 0
        while active:
            # data_to_send = {
            #     "msg_id": mssg_id,
            #     "pieces": self.get_pieces(),
            #     "highlighted_squares": []
            #     }
            connection[0].send(bytes(dumps({"hi":"hi"}), encoding="utf-8"))
        print(f"Bye from Client{ID}")
        connection.close()
        sys.exit()

chess_server = Server()
chess_server()