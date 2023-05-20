from flask import Flask, request
from chess_headless import HeadlessChess
from os.path import join, dirname
from json import loads, load, dumps, dump
from requests import get
import threading
import sys

app = Flask(__name__)

class ChessGame(threading.Thread, HeadlessChess):
    def __init__(self, connection, ID) -> None:
        threading.Thread.__init__(self)
        HeadlessChess.__init__(self)
        self.connection = connection
        self.ID = ID
        self.active = True

    def run(self):
        print("chessgame started")
        while self.active:
            self.connection.send(bytes(dumps({"hi":"hi"}), encoding="utf-8"))
        print(f"Bye from Client{self.ID}")
        self.connection.close()
        sys.exit()

@app.route('/chess', methods=['POST'])
def chess_game():
    # get the request data as a JSON object
    request_data = request.get_json()

    # create a new ChessGame object
    game = ChessGame(request_data["connection"], request_data["ID"])
    game.start()

    # create the response data
    response_data = {'message': 'Success!'}

    # convert the response data to a JSON string
    response_json = json.dumps(response_data)

    # create a response object with the appropriate headers
    response = Response(response_json, status=200, mimetype='application/json')

    # return the response
    return response

if __name__ == '__main__':
    app.run(port=8080)