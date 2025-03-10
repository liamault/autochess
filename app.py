from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Initial chess board setup
board_state = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]

# File to store moves
MOVES_FILE = "chess_moves.txt"

@app.route('/')
def index():
    return render_template('chess.html', board=json.dumps(board_state))

@app.route('/move', methods=['POST'])
def move():
    global board_state

    data = request.json
    old_state = data.get('old_state')
    move_notation = data.get('move_notation')

    # print(old_state)
    print(move_notation)

    board_state = data.get('new_state')

    return jsonify({"message": "Move recorded successfully!"})

if __name__ == '__main__':
    app.run(debug=True)