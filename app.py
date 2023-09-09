from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)

app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True

boggle_game = Boggle()


@app.route("/")
def serve_index():
    """Create new board and place in cookies"""

    board = boggle_game.make_board()
    session['board'] = board

    high_score = session.get("high_score", 0)
    count = session.get("count", 0)

    return render_template(
        "index.html",
        board=board,
        high_score=high_score,
        count=count
    )


@app.route("/check/<word>")
def check_if_word_in_board(word):
    """Check if word is in board, return correlated string message"""

    return jsonify({
        'result': boggle_game.check_valid_word(session["board"], word)
    })


@app.route("/score")
def post_score():
    """if high score is beaten, update high score, increment count"""
    score = request.json["score"]
    high_score = session.get("high_score", 0)
    count = session.get("count", 0)

    session['count'] = count + 1
    if score > high_score:
        session['high_score'] = max(score, high_score)
