import chess
import chess.svg
from pathlib import Path
import json
import re

CHESS_FOLDER = Path("chess")

# Unicode chess pieces untuk SVG
PIECE_SYMBOLS = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
}

def get_piece_svg(piece, is_light_square):
    """Generate SVG for a chess piece with proper styling"""
    if piece is None:
        return ""
    
    symbol = piece.symbol()
    unicode_char = PIECE_SYMBOLS.get(symbol, '')
    
    # White pieces = outlined, Black pieces = filled
    if piece.color:  # White
        return f'''<text x="22.5" y="35" font-size="32" text-anchor="middle" 
            fill="#fff" stroke="#000" stroke-width="1" font-family="serif">{unicode_char}</text>'''
    else:  # Black
        return f'''<text x="22.5" y="35" font-size="32" text-anchor="middle" 
            fill="#000" stroke="#000" stroke-width="0.5" font-family="serif">{unicode_char}</text>'''

def generate_square_svgs():
    """Generate all 64 square SVGs with cool gradient styling"""
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
        
        # Determine square color with cool gradient
        is_light = (chess.square_file(square) + chess.square_rank(square)) % 2 == 1
        
        if is_light:
            # Light square - elegant cream with subtle gradient
            bg_color = "#EEEED2"
            gradient = f'''<defs>
                <linearGradient id="light" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#FFFCE8"/>
                    <stop offset="100%" style="stop-color:#EEEED2"/>
                </linearGradient>
            </defs>
            <rect width="45" height="45" fill="url(#light)"/>'''
        else:
            # Dark square - rich green with gradient (chess.com style)
            bg_color = "#769656"
            gradient = f'''<defs>
                <linearGradient id="dark" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#8CAD6A"/>
                    <stop offset="100%" style="stop-color:#769656"/>
                </linearGradient>
            </defs>
            <rect width="45" height="45" fill="url(#dark)"/>'''
        
        piece_svg = get_piece_svg(piece, is_light)
        
        full_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45" width="45" height="45">
    {gradient}
    {piece_svg}
</svg>'''
        
        with open(CHESS_FOLDER / f"{square_name}.svg", 'w', encoding='utf-8') as f:
            f.write(full_svg)
        
        print(f"Generated {square_name}.svg")
    
    print(f"\n✅ Generated all 64 chess square SVGs!")

if __name__ == "__main__":
    generate_square_svgs()
