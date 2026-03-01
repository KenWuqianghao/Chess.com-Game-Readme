from chessdotcom import get_player_games_by_month_pgn, Client
from flask import Flask, Response
from dotenv import load_dotenv
import chess.svg
import chess.pgn
import datetime
import chess
import io
import os

load_dotenv()


def generate_card():
    date_time = datetime.datetime.utcnow()
    username = os.getenv("username")
    email = os.getenv("email")

    Client.request_config['headers']['User-Agent'] = 'My Chess.com Github Readme Application.You can find it on my Github profile https://github.com/KenWuqianghao. Contact me at {}'.format(email)

    try:
        games = get_player_games_by_month_pgn(username = username, datetime_obj = date_time)
    except Exception:
        date_time = date_time.replace(day=1) - datetime.timedelta(days=1)
        games = get_player_games_by_month_pgn(username = username, datetime_obj = date_time)
    pgn_io = io.StringIO(games.json['pgn']['pgn'])
    game = None
    while True:
        g = chess.pgn.read_game(pgn_io)
        if g is None:
            break
        game = g

    board = game.end().board() if game else chess.Board()

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