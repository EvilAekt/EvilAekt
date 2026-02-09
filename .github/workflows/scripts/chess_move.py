import os
import sys
import chess
import chess.svg
from cairosvg import svg2png
from pathlib import Path
import json

BOARD_STATE_FILE = "chess/board_state.json"
CHESS_FOLDER = Path("chess")

def load_board():
    if Path(BOARD_STATE_FILE).exists():
        with open(BOARD_STATE_FILE, 'r') as f:
            data = json.load(f)
            board = chess.Board(data['fen'])
            return board
    return chess.Board()

def save_board(board):
    CHESS_FOLDER.mkdir(exist_ok=True)
    with open(BOARD_STATE_FILE, 'w') as f:
        json.dump({'fen': board.fen()}, f)

def generate_square_svgs(board):
    CHESS_FOLDER.mkdir(exist_ok=True)
    
    for square in chess.SQUARES:
        square_name = chess.square_name(square)
        
        svg_content = chess.svg.piece(board.piece_at(square), size=45) if board.piece_at(square) else ""
        
        is_light = (chess.square_file(square) + chess.square_rank(square)) % 2 == 1
        color = "#F0D9B5" if is_light else "#B58863"
        
        full_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45" width="45" height="45">
            <rect width="45" height="45" fill="{color}"/>
            {svg_content}
        </svg>'''
        
        with open(CHESS_FOLDER / f"{square_name}.svg", 'w') as f:
            f.write(full_svg)

def make_move(board, move_uci):
    try:
        move = chess.Move.from_uci(move_uci)
        if move in board.legal_moves:
            board.push(move)
            return True
    except:
        pass
    return False

def main():
    issue_title = sys.argv[1]
    parts = issue_title.split('|')
    
    if len(parts) != 3 or parts[0] != 'chess' or parts[1] != 'move':
        print("Invalid issue title format")
        return
    
    square = parts[2]
    board = load_board()
    
    # Cek apakah ada piece yang bisa gerak ke square ini
    for move in board.legal_moves:
        if chess.square_name(move.to_square) == square:
            board.push(move)
            break
    
    save_board(board)
    generate_square_svgs(board)
    
    # Commit changes
    os.system('git config user.name "GitHub Actions Bot"')
    os.system('git config user.email "actions@github.com"')
    os.system('git add chess/')
    os.system(f'git commit -m "Chess move: {square}"')
    os.system('git push')

if __name__ == "__main__":
    main()