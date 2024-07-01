from math import pi
import piece
import re

# super thanks
# 셜뭉중(mjseol06)
# oɥɐꓷ(daho0980)
# GPT-4 for wrtn(주석, 최적화 담당 노예)


def check_moves(moves: list, player_move: str, color: str):
    match = re.match(r"([PNBRQKpnbrqk]+)?([a-hA-H]?[1-8]?)?([Xx])?([a-hA-H][1-8])(=)?([NBRQnbrq])?", player_move, re.I)
    possible_moves = []

    if match:
        part1, part2, part3, part4, part5, part6 = match.groups()
        if part1 is None:
            part1 = 'p'
        if part1.upper() == "P" and part4[-1] in ['1', '8']:
            part5 = "="
        for cx, cy, dx, dy, move_type, piece_type, color, takes_color, takes_piece_type in moves:
            if part2:
        if possible_moves:
            return possible_moves
        else:
            return "No possible move"
    else:
        return "Invalid input"



def check_move_convert(result):
    """
    체스 게임에서 특정 기물의 움직임 결과를 받아서 문자열 형태로 변환하는 함수입니다.

    Args:
    result: 움직임의 결과를 나타내는 데이터. 리스트 또는 문자열 형태일 수 있습니다.

    Returns:
    str: 움직임 결과를 문자열로 변환한 값. 결과에 따라 "Duplicated", 움직임 위치, 특정 오류 메시지,
         "Unknown result" 중 하나를 반환합니다.
    """

    # 결과값이 리스트인 경우
    if isinstance(result, list):
        # 리스트에 원소가 두 개 이상 있는 경우, 중복된 움직임이 있음을 나타냅니다.
        if len(result) >= 2:
            return "Duplicated"
        # 리스트에 원소가 하나 있는 경우, 해당 움직임을 문자열로 변환하여 반환합니다.
        elif len(result) == 1:
            return result[0]
    # 결과값이 문자열인 경우, 특정 오류 메시지들을 그대로 반환합니다.
    elif isinstance(result, str):
        # 알려진 오류 메시지인 경우 해당 메시지를 반환합니다.
        if result in ["No possible move", "Invalid input", "Invalid color"]:
            return result
    # 그 외의 경우는 알 수 없는 결과로 처리합니다.
    else:
        return "Unknown result"


def board_move(board: list, move: str, color: str):
    # 말의 체스 보드 이동을 처리하는 함수입니다.

    # 실제 체스 이동을 인덱스 기반으로 변환합니다.
    index_move = Piece.convert_chess_move_to_index(move)

    # 색상에 따라 적절한 정규 표현식을 사용하여 이동을 분석합니다.
    if color == "Wp":
        match_index_move = re.match(r"Wp([PNBRQK]+)([0-7])([0-7])([0-7])([0-7])", index_move)
    elif color == "Bp":
        match_index_move = re.match(r"Bp([PNBRQK]+)([0-7])([0-7])([0-7])([0-7])", index_move)
    else:
        return "Invalid color"

    # 정규 표현식으로부터 추출한 그룹을 변수에 할당합니다.
    part1, part2, part3, part4, part5 = match_index_move.groups()

    # 첫 번째 부분에 색상을 추가합니다.
    part1 = color + part1

    # 나머지 부분들은 정수로 변환합니다.
    part2, part3, part4, part5 = int(part2), int(part3), int(part4), int(part5)

    # 해당 위치에 말이 존재하면 이동을 수행합니다.
    if board[part2][part3] == part1:
        board[part4][part5] = part1  # 목적지에 말을 배치합니다.
        board[part2][part3] = "-"  # 기존 위치를 비웁니다.
    else:
        return "No piece"

    # 함수에서는 이동이 성공적으로 수행되었음을 특별히 표시하지 않습니다.
    # 필요하다면, 이동 성공 메시지나 다른 값을 반환하도록 수정할 수 있습니다.


def print_board(board: list):
    # 체스 보드 출력
    for row in board:
        formatted_row: list = [' - ' if i == '-' else i for i in row]
        print(' '.join(map(str, formatted_row)))


def play_move(color: str, possible_moves: list, board: list):
    checkmate = False
    if color == "Wp":
        player_move: str = input("하얀색 말의 움직임을 입력하시오")
        move: str = check_move_convert(check_moves(possible_moves, player_move, "Wp"))
    elif color == "Bp":
        player_move: str = input("검은색 체스말 움직임을 입력하시오")
        move: str = check_move_convert(check_moves(possible_moves, player_move, "Bp"))
    else:
        print("Invalid color")
        return "Invalid color"
    if move in ["No possible move", "Invalid input", "Unknown result", "Duplicated"]:
        print(move)
        return move
    if color == "Wp":
        board_move(board, move, "Wp")
    elif color == "Bp":
        board_move(board, move, "Bp")
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
