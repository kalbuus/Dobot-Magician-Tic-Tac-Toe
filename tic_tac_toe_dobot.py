import math
import random
import os
from lib.dobot import Dobot
from serial.tools import list_ports


hard_mode = True #  Режим хардкора. При нём бота невозможно победить :3

debug_mode = False # Режим отладки, лучше не трогать

upward_ammount = 15 # На сколько бот поднимается вверх
cell_size = 25 # Размер одной клетки поля

# Настройки клавиш ввода
key_mapping = {"q": (0, 0), "w": (0, 1), "e": (0, 2),
                   "a": (1, 0), "s": (1, 1), "d": (1, 2),
                   "z": (2, 0), "x": (2, 1), "c": (2, 2)}

# Дальше этой точки ничего не трогать. 

idle_pos = [238, 72, -45]

clear = lambda: os.system('cls')
def print_board(board):
    for row in board:
        print(" ".join(row))
    print()
 
def check_winner(board, main_check, up_center, bot):
    for row in range(len(board)):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != " ":
            if main_check:
                start = [up_center[0] + (cell_size * row), up_center[1] - cell_size / 2, up_center[2]]
                end = [up_center[0] + (cell_size * row), up_center[1] + cell_size * 2.5, up_center[2]]
                path = [[start[0], start[1], start[2] + upward_ammount], start, end, [end[0], end[1], end[2] + upward_ammount]]
                if bot != None:
                    bot.follow_path(path)
                else: print(path)
            return board[row][0]
 
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            if main_check:
                start = [up_center[0] - cell_size / 2, up_center[1] + (cell_size * col), up_center[2]]
                end = [up_center[0] + cell_size * 2.5, up_center[1] + (cell_size * col), up_center[2]]
                path = [[start[0], start[1], start[2] + upward_ammount], start, end, [end[0], end[1], end[2] + upward_ammount]]
                if bot != None:
                    bot.follow_path(path)
                else: print(path)
            return board[0][col]
 
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        # top left to down right
        #   #
        #     #
        #       #

        if main_check:
            start = [up_center[0] - cell_size / 2, up_center[1] - cell_size / 2, up_center[2]]
            end = [up_center[0] + cell_size * 2.5, up_center[1] + cell_size * 2.5, up_center[2]]
            path = [[start[0], start[1], start[2] + upward_ammount], start, end, [end[0], end[1], end[2] + upward_ammount]]
            if bot != None:
                bot.follow_path(path)
            else: print(path)
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        # top right to down left
        #       #
        #     #
        #   #

        if main_check: 
            start = [up_center[0] - cell_size / 2, up_center[1] + cell_size * 2.5, up_center[2]]
            end = [up_center[0] + cell_size * 2.5, up_center[1] - cell_size / 2, up_center[2]]
            path = [[start[0], start[1], start[2] + upward_ammount], start, end, [end[0], end[1], end[2] + upward_ammount]]
            if bot != None:
                bot.follow_path(path)
            else: print(path)
        return board[0][2]
 
    return None
 
def is_full(board):
    return all(cell != " " for row in board for cell in row)
 
def minimax(board, depth, is_maximizing):
    winner = check_winner(board, False, None, None)
    if winner == "X":
        return -10 + depth
    if winner == "O":
        return 10 - depth
    if is_full(board):
        return 0
 
    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score
 
def best_move(board):
    best_score = -math.inf
    move = None

    # Making it lose
    if board == [[' ', ' ', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']] and not hard_mode:
        return (random.randint(0, 2), random.randint(0, 1))
    elif board == [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']] and random.randint(0, 1) == 1 and not hard_mode:
        return (random.randint(0, 2), random.randint(1, 2))
    elif board == [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', 'X']] and random.randint(0, 1) == 1 and not hard_mode:
        return (random.randint(0, 1), random.randint(0, 2))
    elif board == [[' ', ' ', ' '], [' ', ' ', ' '], ['X', ' ', ' ']] and random.randint(0, 1) == 1 and not hard_mode:
        return (random.randint(0, 1), random.randint(0, 2))
        
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def connect_robot():
    available_ports = list_ports.comports()
    port = available_ports[0].device
    return Dobot(port)

def draw_circle(center, cell_size, upward_ammount):
    steps = 24
    scale = (cell_size / 2) - 1
    if debug_mode: print(center)
    path = [[center[0] + scale, center[1], center[2] + upward_ammount]]
    for i in range(steps + 2):
        x = math.cos(((math.pi * 2) / steps) * i)
        y = math.sin(((math.pi * 2) / steps) * i)

        path.append([center[0] + x * scale, center[1] + y * scale, center[2]])
    path.append([path[-1][0], path[-1][1], center[2] + upward_ammount])
    return path

def from_center(x, y, z, ct):
    return [ct[0] + x, ct[1] + y, ct[2] + z]

def to_idle_pos(bot):
    if bot != None:
        bot.follow_path([idle_pos])

def play(center, bot):
    board = [[" " for _ in range(3)] for _ in range(3)]

    board_draw_path = [
        from_center(0, 0, upward_ammount, center),
        from_center(cell_size / 2, cell_size * 1.5, upward_ammount, center),
        from_center(cell_size / 2, cell_size * 1.5, 0, center),
        from_center(cell_size / 2, -cell_size * 1.5, 0, center),
        from_center(cell_size / 2, -cell_size * 1.5, upward_ammount, center),
        from_center(-cell_size / 2, cell_size * 1.5, upward_ammount, center),
        from_center(-cell_size / 2, cell_size * 1.5, 0, center),
        from_center(-cell_size / 2, -cell_size * 1.5, 0, center),
        from_center(-cell_size / 2, -cell_size * 1.5, upward_ammount, center),

        from_center(cell_size * 1.5, cell_size / 2, upward_ammount, center),
        from_center(cell_size * 1.5, cell_size / 2, 0, center),
        from_center(-cell_size * 1.5, cell_size / 2, 0, center),
        from_center(-cell_size * 1.5, cell_size / 2, upward_ammount, center),
        from_center(cell_size * 1.5, -cell_size / 2, upward_ammount, center),
        from_center(cell_size * 1.5, -cell_size / 2, 0, center),
        from_center(-cell_size * 1.5, -cell_size / 2, 0, center),
        from_center(-cell_size * 1.5, -cell_size / 2, upward_ammount, center),
        from_center(0, 0, upward_ammount, center),
    ]

    if bot != None:
        bot.follow_path(board_draw_path)
    else: print(board_draw_path)

    to_idle_pos(bot)
    up_center = [center[0] - cell_size, center[1] - cell_size, center[2]]
    if debug_mode: print(up_center)

    for _ in range(9):
        if is_full(board) or check_winner(board, True, up_center, bot):
            break
 
        if _ % 2 == 0:
            while True:
                move = input("").lower()
                if move in key_mapping:
                    row, col = key_mapping[move]
                    if board[row][col] == " ":
                        board[row][col] = "X"
                        break
                    else:
                        print("Ячейка занята!")
                else:
                    print("Некорректный ввод.")
        else:
            move = best_move(board)
            if move:
                #     строка   столбец
                board[move[0]][move[1]] = "O"
            
            if debug_mode: print(move)
            if bot != None:
                clear()
                bot.follow_path(draw_circle([up_center[0] + (cell_size * move[0]), up_center[1] + (cell_size * move[1]), up_center[2]], cell_size, upward_ammount))
                to_idle_pos(bot)
                pass
            else:
                print(draw_circle([up_center[0] + (cell_size * move[0]), up_center[1] + (cell_size * move[1]), up_center[2]], cell_size, upward_ammount))
 
        if debug_mode: print_board(board)
        winner = check_winner(board, True, up_center, bot)
        if winner == "X":
            print("Победил Игрок!")
            return
        elif winner == "O":
            print("Победила Рука!")
            return
 
    print("Ничья!")

def main():
    if debug_mode:
        print("------ ВКЛЮЧЁН РЕЖИМ ОТЛАДКИ ------")
        useBot = bool(input("Использовать робота?\n"))
    else:
        useBot = True

    if useBot:
        try:
            bot = connect_robot()
        except:
            print("Бот не подключён. Продолжаем без него")
            input("Нажмите ENTER чтобы продолжить...")
            bot = None
    else: bot = None

    if bot != None:
        try:
            if debug_mode:
                if bool(input("Калибровать бота?\n")):
                    bot.home()
            else:
                bot.home()
        except:
            print("Возникла непредвиденная ошибка. Попробуйте ещё раз.")
            input()
            return

        input("Поставьте бота в центр.\n")

        center = bot.get_pose()
        bot.follow_path([[center[0], center[1], center[2] + upward_ammount]])
        to_idle_pos(bot)
    else:
        center = [0, 0, -60]

    while True:
        clear()
        if not debug_mode:
            print("------ Главное Меню ------")
        else:
            print("------ Главное Меню (Режим Отладки) ------")
        
        if bot == None and not debug_mode: print("0 - Новая Игра (ОТКЛЮЧЕНО)")
        else: print("0 - Новая Игра")
        if bot != None: print("1 - Калибровать Центр")
        else: print("1 - Калибровать Центр (ОТКЛЮЧЕНО)")
        if useBot: print("2 - Переподключить Робота")
        else: print("2 - Переподключить Робота (ОТКЛЮЧЕНО)")
        print("3 - Выход\n")
        if debug_mode:
            # Тут будут настройки режима отладки
            pass
        
        try:
            user_input = int(input())
        except:
            print("Введите число")
            continue

        if user_input == 0 and (bot != None or debug_mode):
            clear()
            play(center, bot)
            input("Нажмите ENTER чтобы продолжить...")
        elif user_input == 1 and bot != None:
            center = bot.get_pose()
            bot.follow_path([[center[0], center[1], center[2] + upward_ammount]])
            to_idle_pos(bot)
        elif user_input == 2 and useBot:
            try:
                bot = None
                bot = connect_robot()
                bot.home()
            except:
                print("Произошла ошибка, попробуйте ещё раз")
                input("Нажмите ENTER чтобы продолжить...")
        elif user_input == 3:
            break
        else:
            continue

if __name__ == "__main__":
    main()
    #play()
 