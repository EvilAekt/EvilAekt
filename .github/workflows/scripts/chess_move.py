import os
import sys
import chess
from pathlib import Path
import json

BOARD_STATE_FILE = Path("chess/board_state.json")
CHESS_FOLDER = Path("chess")

# Unicode chess pieces
PIECE_SYMBOLS = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
}

def load_board():
    if BOARD_STATE_FILE.exists():
        with open(BOARD_STATE_FILE, 'r') as f:
            data = json.load(f)
            board = chess.Board(data['fen'])
            return board
    return chess.Board()

def save_board(board):
    CHESS_FOLDER.mkdir(exist_ok=True)
    with open(BOARD_STATE_FILE, 'w') as f:
        json.dump({'fen': board.fen()}, f, indent=4)

def get_piece_svg(piece):
    """Generate SVG for a chess piece"""
    if piece is None:
        return ""
    
    symbol = piece.symbol()
    unicode_char = PIECE_SYMBOLS.get(symbol, '')
    
    # White pieces = white fill with black stroke, Black = black fill
    if piece.color:  # White
        return f'''<text x="22.5" y="35" font-size="32" text-anchor="middle" 
            fill="#fff" stroke="#000" stroke-width="1" font-family="serif">{unicode_char}</text>'''
    else:  # Black
        return f'''<text x="22.5" y="35" font-size="32" text-anchor="middle" 
            fill="#000" stroke="#000" stroke-width="0.5" font-family="serif">{unicode_char}</text>'''

def generate_square_svgs(board):
    """Generate all 64 square SVGs with chess.com style colors"""
    CHESS_FOLDER.mkdir(exist_ok=True)
    
    for square in chess.SQUARES:
        square_name = chess.square_name(square)
        piece = board.piece_at(square)
        
        # Chess.com style colors with gradient
        is_light = (chess.square_file(square) + chess.square_rank(square)) % 2 == 1
        
        if is_light:
            gradient = '''<defs>
                <linearGradient id="light" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#FFFCE8"/>
                    <stop offset="100%" style="stop-color:#EEEED2"/>
                </linearGradient>
            </defs>
            <rect width="45" height="45" fill="url(#light)"/>'''
        else:
            gradient = '''<defs>
                <linearGradient id="dark" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#8CAD6A"/>
                    <stop offset="100%" style="stop-color:#769656"/>
                </linearGradient>
            </defs>
            <rect width="45" height="45" fill="url(#dark)"/>'''
        
        piece_svg = get_piece_svg(piece)
        
        full_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45" width="45" height="45">
    {gradient}
    {piece_svg}
</svg>'''
        
        with open(CHESS_FOLDER / f"{square_name}.svg", 'w', encoding='utf-8') as f:
            f.write(full_svg)

def main():
    issue_title = sys.argv[1]
    parts = issue_title.split('|')
    
    if len(parts) != 3 or parts[0] != 'chess' or parts[1] != 'move':
        print("Invalid issue title format")
        return
    
    target_square = parts[2].strip().lower()
    board = load_board()
    
    print(f"Current turn: {'White' if board.turn else 'Black'}")
    print(f"Target square: {target_square}")
    print(f"Legal moves: {[str(m) for m in board.legal_moves]}")
    
    # Find a legal move to this square
    move_made = False
    for move in board.legal_moves:
        if chess.square_name(move.to_square) == target_square:
            print(f"Making move: {move}")
            board.push(move)
            move_made = True
            break
    
    if not move_made:
        print(f"No legal move to {target_square}")
        return
    
    save_board(board)
    generate_square_svgs(board)
    
    print("Board updated successfully!")
    
    # Commit changes
    os.system('git config user.name "GitHub Actions Bot"')
    os.system('git config user.email "actions@github.com"')
    os.system('git add chess/')
    os.system(f'git commit -m "Chess move to {target_square}"')
    os.system('git push')

if __name__ == "__main__":
    main()