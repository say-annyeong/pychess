import piece
import re

# super thanks
# 셜뭉중(mjseol06)
# oɥɐꓷ(daho0980)
# GPT-4 for wrtn(주석, 최적화 담당 노예)


def check_moves(moves: list[list], player_move: str) -> list | str:
    match = re.match(r"([PNBRQKpnbrqk]+)?([a-hA-H])?([1-8])?([Xx])?([a-hA-H])([1-8])(=[NBRQnbrq]+)?", player_move, re.I)
    possible_moves = []
    if match:
        part1, part2, part3, part4, part5, part6, part7 = match.groups()
        match_part1, match_part2, match_part3, match_part4, match_part5, match_part6, match_part7 = False
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
            return possible_moves
        else:
            return "No possible move"
    else:
        return "Invalid input"


def check_move_convert(result: list | str) -> list | str:
    if isinstance(result, list):
        if len(result) >= 2:
            return "Duplicated"
        elif len(result) == 1:
            return result[0]
    elif isinstance(result, str):
        if result in ["No possible move", "Invalid input", "Invalid color"]:
            return result
    else:
        return "Unknown result"


def board_move(board: list[list], move: list):
    cx, cy, dx, dy, move_type, piece_type, color, takes_color, takes_piece_type = move
    piece_name = color + piece_type
    if board[cx][cy] == piece_name:
        board[cx][cy] = piece_name
        board[cx][cy] = "-"
    else:
        return "No piece"


def print_board(board: list):
    # 체스 보드 출력
    for row in board:
        formatted_row: list = [' - ' if i == '-' else i for i in row]
        print(' '.join(map(str, formatted_row)))


def play_move(color: str, possible_moves: list, board: list):
    checkmate = False
    if color == "Wp":
        player_move: str = input("하얀색 말의 움직임을 입력하시오")
        move = check_move_convert(check_moves(possible_moves, player_move, "Wp"))
    elif color == "Bp":
        player_move: str = input("검은색 체스말 움직임을 입력하시오")
        move = check_move_convert(check_moves(possible_moves, player_move, "Bp"))
    else:
        print("Invalid color")
        return "Invalid color"
    if isinstance(move, str):
        print(move)
        return move
    if color == "Wp":
        board_move(board, move)
    elif color == "Bp":
        board_move(board, move)
    else:
        print("Invalid color")
        return "Invalid color"
    # 움직임이 체크를 일으키는 경우, 움직임 문자열 끝에 "+"를 추가합니다.
    white_moves, black_moves = Piece.search_piece()
    for moves in white_moves:
        if moves[8:10] == "BK":
            move = move + "+"
    for moves in black_moves:
        if moves[8:10] == "WK":
            move = move + "+"



    print_board(chess_board)
    game_moves.append(move)
    print(game_moves)
    print(move)
    print(player_move)
    if checkmate:
        return "checkmate"


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
        check = play_move("Wp", white_possible_move, chess_board)
        urn = "Bp"
    elif turn == "Bp":
        check = play_move("Bp", black_possible_move, chess_board)
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
