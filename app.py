from flask import Flask, render_template, request, redirect, url_for
import chess.svg
import chess

app = Flask(__name__)

# Инициализация шахматной доски
board = chess.Board()

# Переменная для хранения информации о победе
winner = None

# Переменная для хранения хода
gl_move = ''

@app.route('/')
def index():
    # Генерируем SVG для текущего состояния доски
    board_svg = chess.svg.board(board=board, coordinates=False)
    return render_template('index.html', board_svg=board_svg, winner=winner)

@app.route('/move', methods=['POST'])
def make_move():
    global gl_move
    # Получаем ход из POST-запроса
    move_str = request.form.get('move')
    if move_str:
        gl_move += move_str + ' '
    move_str = move_str.replace(' ', '')

    print(move_str)

    try:
        move = chess.Move.from_uci(move_str)
        if move in board.legal_moves:
            board.push(move)
    except ValueError:
        pass

    # Проверяем наличие победителя
    result = board.result()
    if result == '1-0':
        winner = "White wins!"
    elif result == '0-1':
        winner = "Black wins!"
    elif result == '1/2-1/2':
        winner = "It's a draw."
    else:
        winner = None
    
    # Перенаправляем на главную страницу
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
