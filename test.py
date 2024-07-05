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
    def __init__(self, board: list[list[str]]):
        self.board = board
        self.piece_types = list(PieceType)

    def step(self, x: int, y: int, takes_color: Color, color: Color, piece_type: PieceType, capture=True, move=True) \
            -> tuple[list[int | str | PieceType | Color | None] | list, bool]:
        if self.board[x][y] == "-":
            if move:
                return [x, y, "m", piece_type, color, takes_color, None], True
        elif str(takes_color) in self.board[x][y]:
            if capture:
                for takes_piece_type in self.piece_types:
                    if str(takes_color) + takes_piece_type.value in self.board[x][y]:
                        return [x, y, "x", piece_type, color, takes_color, takes_piece_type], False
        return [], False

    def walk(self, cx: int, cy: int, dx: int, dy: int, moves: list, takes_color: Color, color: Color, times: int,
             piece_type: PieceType, capture=True, move=True) \
            -> list[list[int | str | PieceType | Color | None]] | list:
        pass
        # ... (기존 코드와 동일, 타입 힌팅만 변경)


class Pieces(Moves):
    def __init__(self, board: list[list[str]]):
        super().__init__(board)
        self.knight_directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (-2, -1), (-2, 1), (2, -1)]
        self.bishop_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.rook_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.QaK_directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def pawn(self, x: int, y: int, color: Color, takes_color: Color) -> list[list[int | str | PieceType | Color | None]] | list:
        moves = []
        direction = 1 if color == Color.BLACK else -1

        self.walk(x, y, direction, 0, moves, takes_color, color, 1, PieceType.PAWN, False)
        self.walk(x, y, direction, 1, moves, takes_color, color, 1, PieceType.PAWN, True, False)
        self.walk(x, y, direction, -1, moves, takes_color, color, 1, PieceType.PAWN, True, False)

        return moves

    def knight(self, x: int, y: int, color: Color, takes_color: Color) -> list[list[int | str | None]] | list:
        moves = []
        for dx, dy in self.knight_directions:
            self.walk(x, y, dx, dy, moves, takes_color, color, 1, PieceType.KNIGHT)
        return moves

    # 다른 말들의 메서드도 비슷하게 수정


class CalculateMoves(Pieces):
    def __init__(self, board: list[list[str]]):
        super().__init__(board)

    def calculate_move(self, piece: str, row: int, col: int, color: Color, takes_color: Color)\
            -> list[list[int | str | PieceType | Color | None]] | list:
        piece_type = PieceType(piece[2:])
        method_name = piece_type.name.lower()
        method = getattr(self, method_name, None)
        if method:
            return method(row, col, color, takes_color)
        return []

    def search_piece(self) -> tuple[list[list[int | str | PieceType | Color | None]], list[list[int | str | PieceType | Color | None]]]:
        white_moves = [
            move
            for row in range(8)
            for col in range(8)
            if self.board[row][col].startswith(str(Color.WHITE))
            for move in self.calculate_move(self.board[row][col], row, col, Color.WHITE, Color.BLACK)
        ]

        black_moves = [
            move
            for row in range(8)
            for col in range(8)
            if self.board[row][col].startswith(str(Color.BLACK))
            for move in self.calculate_move(self.board[row][col], row, col, Color.BLACK, Color.WHITE)
        ]

        if any(not piece.startswith((str(Color.WHITE), str(Color.BLACK), "-")) for row in self.board for piece in row):
            raise ValueError("잘못된 색상")
        return white_moves, black_moves