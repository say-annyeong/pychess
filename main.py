import piece
import re

# super thanks
# 셜뭉중(mjseol06)
# oɥɐꓷ(daho0980)
# GPT-4 for wrtn(주석, 최적화 담당 노예)
# Claude 3.5 Sonnet(코딩 고수)


def check_moves(moves: list[list[int | str | None]], player_move: str) -> list | str:
    match = re.match(r"([PNBRQKpnbrqk]+)?([a-hA-H])?([1-8])?([Xx])?([a-hA-H])([1-8])(=[NBRQnbrq]+)?", player_move, re.I)
    possible_moves = []
    if match:
        part1, part2, part3, part4, part5, part6, part7 = match.groups()
        if part1 is None:
            part1 = 'P'
        else:
            part1 = part1.upper()
        if part7:
            part7 = part7.upper()
        chess_to_index_map = {
            'a': '0', 'b': '1', 'c': '2', 'd': '3',
            'e': '4', 'f': '5', 'g': '6', 'h': '7',
            '1': '7', '2': '6', '3': '5', '4': '4',
            '5': '3', '6': '2', '7': '1', '8': '0'
        }
        for cx, cy, dx, dy, move_type, piece_type, color, takes_color, takes_piece_type in moves:
            match_part1 = (part1 == piece_type)
            match_part2 = (part2 is None or chess_to_index_map[part2] == cy)
            match_part3 = (part3 is None or chess_to_index_map[part3] == cx)
            match_part4 = (part4 is None or (part4 == move_type and takes_piece_type is not None))
            match_part5 = (chess_to_index_map[part5] == dy)
            match_part6 = (chess_to_index_map[part6] == dx)
            match_part7 = (part7 is None or (part1 == "P" and dx in ['0', '7']))
            if match_part1 and match_part2 and match_part3 and match_part4 and match_part5 and match_part6 and match_part7:
                possible_moves.append([cx, cy, dx, dy, move_type, piece_type, color, takes_color, takes_piece_type])
        if possible_moves:
            if len(possible_moves) > 1:
                return "Duplicated"
            return possible_moves[0]
        else:
            return "No possible move"
    else:
        return "Invalid input"


def board_move(board: list[list[str]], move: list[int | str | None]) -> str | None:
    cx, cy, dx, dy, move_type, piece_type, color, takes_color, takes_piece_type = move
    piece_name = color + piece_type
    if board[cx][cy] == piece_name:
        board[cx][cy] = piece_name
        board[cx][cy] = "-"
    else:
        return "No piece"


def checkmate():
    pass


def print_board(board: list[list[str]]):
    # 체스 보드 출력
    for row in board:
        formatted_row: list = [' - ' if i == '-' else i for i in row]
        print(' '.join(map(str, formatted_row)))


def play_move(color: str, possible_moves: list[list[int | str | None]], board: list[list]):
    if color == "Wp":
        player_move: str = input("하얀색 말의 움직임을 입력하시오")
    elif color == "Bp":
        player_move: str = input("검은색 말의 움직임을 입력하시오")
    else:
        print("Invalid color")
        return "Invalid color"
    move = check_moves(possible_moves, player_move)
    if isinstance(move, str):
        print(move)
        return move
    board_cache = board
    board_move(board_cache, move)
    cache_move = piece.CalculateMoves(board_cache)
    white_moves, black_moves = cache_move.search_piece()
    king_check = 0
    for _, _, _, _, _, _, _, _, takes_piece in white_moves:
        if takes_piece == "K":
            king_check = 1 if color == "Wp" else 2
    for _, _, _, _, _, _, _, _, takes_piece in black_moves:
        if takes_piece == "K":
            king_check = 2 if color == "Wp" else 1
    if king_check == 2:
        print("No possible move")
        return "No possible move"
    print_board(board_cache)
    game_moves.append(move)
    print(game_moves)
    print(move)
    print(player_move)
    if checkmate():
        return board_cache, "checkmate"
    return board_cache, king_check


def back_check(checking: str):
    if checking in ["No possible move", "Invalid input", "Unknown result", "Duplicated"]:
        return "Back"
    elif checking == "checkmate":
        return "checkmate"
    else:
        return "continue"


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

Piece = piece.CalculateMoves(chess_board)
game_moves = []
turn = "Wp"
print_board(chess_board)



while True:
    white_possible_move, black_possible_move = Piece.search_piece()
    print(white_possible_move)
    print(black_possible_move)
    if turn == "Wp":
        check = play_move(turn, white_possible_move, chess_board)
        turn = "Bp"
    elif turn == "Bp":
        check = play_move(turn, black_possible_move, chess_board)
        turn = "Wp"
    else:
        raise ValueError("Wp와 Bp가 아닙니다.")

    match back_check(check):
        case "continue":
            continue
        case "Back":
            if turn == "Bp":
                turn = "Wp"
            elif turn == "Wp":
                turn = "Bp"
            else:
                raise ValueError("Wp와 Bp가 아닙니다")
        case _:
            end = back_check(check)
            break
print(end)
