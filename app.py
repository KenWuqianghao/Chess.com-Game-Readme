from chessdotcom import get_player_games_by_month_pgn
from flask import Flask, Response
from dotenv import load_dotenv
import chess.svg
import datetime
import chess
import os

load_dotenv()

def generate_card():
    date_time = datetime.datetime.now()
    username = os.getenv("username")

    games = get_player_games_by_month_pgn(username = username, datetime_obj = date_time)
    for line in games.json['pgn']['pgn'].splitlines():
        if line[:16] == "[CurrentPosition":
            pgn = line[18:-2]
            break
    
    board = chess.Board(pgn)

    return chess.svg.board(board, size=350)

app = Flask(__name__)

@app.route("/")
def handle_all():
    svg = generate_card()
    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp

if __name__ == "__main__":
    app.run(debug=True)