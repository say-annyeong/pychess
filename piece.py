from typing import Callable, Type


# noinspection PyMethodMayBeStatic
class Convert:
    def convert_chess_move_to_index(self, move: str) -> str:
        chess_to_index_map = {
            'a': '0', 'b': '1', 'c': '2', 'd': '3',
            'e': '4', 'f': '5', 'g': '6', 'h': '7',
            '1': '7', '2': '6', '3': '5', '4': '4',
            '5': '3', '6': '2', '7': '1', '8': '0'
        }

        piece_info = move[0:3]
        start_col_index = chess_to_index_map[move[4]]
        start_row_index = chess_to_index_map[move[3]]

        if 'x' in move:
            target_col_index = chess_to_index_map[move[7]]
            target_row_index = chess_to_index_map[move[6]]
            capture_info = move[8:]
            return f"{piece_info}{start_col_index}{start_row_index}{target_col_index}{target_row_index}x{capture_info}"
        else:
            target_col_index = chess_to_index_map[move[6]]
            target_row_index = chess_to_index_map[move[5]]
            move_info = move[7:]
            return f"{piece_info}{start_col_index}{start_row_index}{target_col_index}{target_row_index}{move_info}"


class Moves:
    def __init__(self, board: list[list[str]]):
        self.board = board
        self.piece_types = ["P", "N", "B", "R", "Q", "K"]

    def step(self, x: int, y: int, takes_color: str, color: str, piece_type: str, capture=True, move=True)\
            -> tuple[list, bool]:
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
             piece_type: str, capture=True, move=True) -> list:
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
    def __init__(self, board: list[list[str]]):
        super().__init__(board)
        self.knight_directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (-2, -1), (-2, 1), (2, -1)]
        self.bishop_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.rook_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.QaK_directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def pawn(self, x: int, y: int, color: str, takes_color: str) -> list[list]:
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

    def knight(self, x: int, y: int, color: str, takes_color: str) -> list[list]:
        moves = []
        for dx, dy in self.knight_directions:
            self.walk(x, y, dx, dy, moves, takes_color, color, 1, "N")
        return moves

    def bishop(self, x: int, y: int, color: str, takes_color: str) -> list[list]:
        moves = []
        for dx, dy in self.bishop_directions:
            self.walk(x, y, dx, dy, moves, takes_color, color, -1, "B")
        return moves

    def rook(self, x: int, y: int, color: str, takes_color: str) -> list[list]:
        moves = []
        for dx, dy in self.rook_directions:
            self.walk(x, y, dx, dy, moves, takes_color, color, -1, "R")
        return moves

    def queen(self, x: int, y: int, color: str, takes_color: str) -> list[list]:
        moves = []
        for dx, dy in self.QaK_directions:
            self.walk(x, y, dx, dy, moves, takes_color, color, -1, "Q")
        return moves

    def king(self, x: int, y: int, color: str, takes_color: str) -> list[list]:
        moves = []
        for dx, dy in self.QaK_directions:
            self.walk(x, y, dx, dy, moves, takes_color, color, 1, "K")
        return moves


class CustomPieces(Moves):
    def amazon(self, x: int, y: int, color: str, takes_color: str) -> list[list]:
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

    def __call__(self) -> tuple[list[list], list[list]]:
        return self.search_piece()

    def calculate_move(self, piece: str, row: int, col: int, color: str, takes_color: str) -> list[list]:
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

    def search_piece(self) -> tuple[list[list], list[list]]:
        white_moves, black_moves = [], []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece.startswith("Wp"):
                    white_moves.extend(self.calculate_move(piece, row, col, "Wp", "Bp"))
                elif piece.startswith("Bp"):
                    black_moves.extend(self.calculate_move(piece, row, col, "Bp", "Wp"))
                elif piece.startswith("-"):
                    continue
                else:
                    raise ValueError("잘못된 색상")
        return white_moves, black_moves


if __name__ == "__main__":
    chess_board = [
        ["-", "-", "-", "-", "-", "-", "-", "BpK"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "BpQ", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "BpR"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["WpK", "-", "-", "-", "-", "-", "-", "-"]
    ]
    cal = CalculateMoves(chess_board)
    print(cal())
