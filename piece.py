from typing import Callable
from enum import Enum, auto


class Color(Enum):
    WHITE = auto()
    BLACK = auto()

    @property
    def opposite(self):
        return Color.BLACK if self == Color.WHITE else Color.WHITE

    def __str__(self):
        return "Wp" if self == Color.WHITE else "Bp"


class PieceType(Enum):
    PAWN = "P"
    KNIGHT = "N"
    BISHOP = "B"
    ROOK = "R"
    QUEEN = "Q"
    KING = "K"
    AMAZON = "A"


class Moves:
    def __init__(self, board: list[list[str, str, str, str, str, str, str, str]]):
        self.board = board
        self.piece_types = ["P", "N", "B", "R", "Q", "K"]

    def step(self, x: int, y: int, takes_color: str, color: str, piece_type: str, capture=True, move=True) \
            -> tuple[list[list[int | str | None]] | list, bool]:
        if self.board[x][y] == "-":
            if move:
                return [x, y, "m", piece_type, color, takes_color, None], True
        elif takes_color in self.board[x][y]:
            if capture:
                for takes_piece_type in self.piece_types:
                    if takes_color + takes_piece_type in self.board[x][y]:
                        return [x, y, "x", piece_type, color, takes_color, takes_piece_type], False
        return [], False

    def walk(self, cx: int, cy: int, dx: int, dy: int, moves: list, takes_color: str, color: str, times: int,
             piece_type: str, capture=True, move=True) \
            -> list[list[int | str | None]] | list:
        x, y = cx, cy
        count = 0
        while times == -1 or count < times:
            x += dx
            y += dy
            if not (0 <= x <= 7 and 0 <= y <= 7):
                break
            if cx != x or cy != y:
                move, continue_walking = self.step(x, y, takes_color, color, piece_type, capture, move)
                if move:
                    moves.append([cx, cy] + move)
                    if not continue_walking:
                        break
            count += 1
        return moves


class Pieces(Moves):
    def __init__(self, board: list[list[str, str, str, str, str, str, str, str]]):
        super().__init__(board)
        self.knight_directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (-2, -1), (-2, 1), (2, -1)]
        self.bishop_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.rook_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.QaK_directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def pawn(self, x: int, y: int, color: str, takes_color: str) -> list[list[int | str | None]] | list:
        moves = []
        direction = 1 if color == "Bp" else -1

        self.walk(x, y, direction, 0, moves, takes_color, color, 1, "P", False)
        self.walk(x, y, direction, 1, moves, takes_color, color, 1, "P", True, False)
        self.walk(x, y, direction, -1, moves, takes_color, color, 1, "P", True, False)

        # 앙파상 구현시 부활 예정
        # if (color == "Wp" and x == 6) or (color == "Bp" and x == 1):
        #     self.walk(x, y, direction, 0, moves, takes_color, color, 2, "P", False)
        # else:
        #     self.walk(x, y, direction, 0, moves, takes_color, color, 1, "P", False)

        return moves

    def knight(self, x: int, y: int, color: str, takes_color: str) -> list[list[int | str | None]] | list:
        moves = []
        for dx, dy in self.knight_directions:
            self.walk(x, y, dx, dy, moves, takes_color, color, 1, "N")
        return moves

    def bishop(self, x: int, y: int, color: str, takes_color: str) -> list[list[int | str | None]] | list:
        moves = []
        for dx, dy in self.bishop_directions:
            self.walk(x, y, dx, dy, moves, takes_color, color, -1, "B")
        return moves

    def rook(self, x: int, y: int, color: str, takes_color: str) -> list[list[int | str | None]] | list:
        moves = []
        for dx, dy in self.rook_directions:
            self.walk(x, y, dx, dy, moves, takes_color, color, -1, "R")
        return moves

    def queen(self, x: int, y: int, color: str, takes_color: str) -> list[list[int | str | None]] | list:
        moves = []
        for dx, dy in self.QaK_directions:
            self.walk(x, y, dx, dy, moves, takes_color, color, -1, "Q")
        return moves

    def king(self, x: int, y: int, color: str, takes_color: str) -> list[list[int | str | None]] | list:
        moves = []
        for dx, dy in self.QaK_directions:
            self.walk(x, y, dx, dy, moves, takes_color, color, 1, "K")
        return moves


class CustomPieces(Moves):
    def amazon(self, x: int, y: int, color: str, takes_color: str) -> list[list[int | str | None]] | list:
        moves = []
        directions1 = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (-2, -1), (-2, 1), (2, -1)]
        directions2 = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions1:
            self.walk(x, y, dx, dy, moves, takes_color, color, 1, "A")
        for dx, dy in directions2:
            self.walk(x, y, dx, dy, moves, takes_color, color, -1, "A")
        return moves


class CalculateMoves(Pieces, CustomPieces):
    def __init__(self, board: list[list[str]]):
        super().__init__(board)

    def __call__(self) -> tuple[list[list[int | str | None]], list[list[int | str | None]]]:
        return self.search_piece()

    def calculate_move(self, piece: str, row: int, col: int, color: str, takes_color: str)\
            -> list[list[int | str | None]] | list:
        piece_type = piece[2:]
        method_name = {
            "P": "pawn",
            "N": "knight",
            "B": "bishop",
            "R": "rook",
            "Q": "queen",
            "K": "king",
            "A": "amazon"
        }.get(piece_type, None)

        if method_name:
            method: Callable[[int, int, str, str], list[list]] = getattr(self, method_name, None)
            if method:
                return method(row, col, color, takes_color)
        return []

    def search_piece(self) -> tuple[list[list[int | str | None]], list[list[int | str | None]]]:
        white_moves = [
            move
            for row in range(8)
            for col in range(8)
            if self.board[row][col].startswith("Wp")
            for move in self.calculate_move(self.board[row][col], row, col, "Wp", "Bp")
        ]

        black_moves = [
            move
            for row in range(8)
            for col in range(8)
            if self.board[row][col].startswith("Bp")
            for move in self.calculate_move(self.board[row][col], row, col, "Bp", "Wp")
        ]

        if any(not piece.startswith(("Wp", "Bp", "-")) for row in self.board for piece in row):
            raise ValueError("잘못된 색상")
        return white_moves, black_moves


if __name__ == "__main__":
    chess_board = [
        ["-", "-", "-", "-", "-", "-", "-", "BpK"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["WpK", "-", "-", "-", "-", "-", "-", "-"]
    ]
    cal = CalculateMoves(chess_board)
    print(cal())
