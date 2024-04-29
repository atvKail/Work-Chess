from flask import Flask, render_template, request, redirect, url_for
import chess.engine
import chess.svg
import chess


app = Flask(__name__)

board = chess.Board()

winner = None

gl_move = ''


def get_bot_move(board, color):
    with chess.engine.SimpleEngine.popen_uci('./stockfish/stockfish-windows-x86-64-avx2.exe') as engine:
        result = engine.play(board, chess.engine.Limit(time=0.1))
        return result.move
    

@app.route('/')
def index():
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
                
            # Если нет победителя, делаем ход бота
            if not winner:
                bot_move = get_bot_move(board, chess.WHITE if board.turn else chess.BLACK)
                board.push(bot_move)
                
                # Проверяем наличие победителя после хода бота
                result = board.result()
                if result == '1-0':
                    winner = "White wins!"
                elif result == '0-1':
                    winner = "Black wins!"
                elif result == '1/2-1/2':
                    winner = "It's a draw."
                else:
                    winner = None
            
    except ValueError:
        pass
    
    # Перенаправляем на главную страницу
    return redirect(url_for('index'))

@app.route('/restart', methods=['GET', 'POST'])
def restart():
    global board, winner, gl_move
    board = chess.Board()
    winner = None
    gl_move = ''
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
