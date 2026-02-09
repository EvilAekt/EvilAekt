import chess
from pathlib import Path
import json

CHESS_FOLDER = Path("chess")

# Unicode chess pieces
PIECE_SYMBOLS = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
}

def get_piece_svg(piece):
    """Generate SVG for a chess piece - noir style"""
    if piece is None:
        return ""
    
    symbol = piece.symbol()
    unicode_char = PIECE_SYMBOLS.get(symbol, '')
    
    # White pieces = light grey with dark stroke, Black pieces = dark with light stroke
    if piece.color:  # White
        return f'''<text x="22.5" y="35" font-size="32" text-anchor="middle" 
            fill="#E0E0E0" stroke="#1a1a1a" stroke-width="1.5" font-family="serif">{unicode_char}</text>'''
    else:  # Black
        return f'''<text x="22.5" y="35" font-size="32" text-anchor="middle" 
            fill="#1a1a1a" stroke="#404040" stroke-width="0.5" font-family="serif">{unicode_char}</text>'''

def generate_square_svgs():
    """Generate all 64 square SVGs with noir monochrome style"""
    CHESS_FOLDER.mkdir(exist_ok=True)
    
    # Load board state
    board_file = CHESS_FOLDER / "board_state.json"
    if board_file.exists():
        with open(board_file, 'r') as f:
            data = json.load(f)
            board = chess.Board(data['fen'])
    else:
        board = chess.Board()
    
    for square in chess.SQUARES:
        square_name = chess.square_name(square)
        piece = board.piece_at(square)
        
        # Noir theme - black and grey squares
        is_light = (chess.square_file(square) + chess.square_rank(square)) % 2 == 1
        
        if is_light:
            # Light square - silver/grey
            gradient = '''<defs>
                <linearGradient id="light" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#B8B8B8"/>
                    <stop offset="100%" style="stop-color:#909090"/>
                </linearGradient>
            </defs>
            <rect width="45" height="45" fill="url(#light)"/>'''
        else:
            # Dark square - deep black
            gradient = '''<defs>
                <linearGradient id="dark" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#2a2a2a"/>
                    <stop offset="100%" style="stop-color:#0a0a0a"/>
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
        
        print(f"Generated {square_name}.svg")
    
    print(f"\n♠ Generated all 64 noir chess squares!")

if __name__ == "__main__":
    generate_square_svgs()
