import time
import os
import random
from pynput.keyboard import Listener, Key
from threading import Thread


def insert_gameboard(sym, coord):
    gameboard[coord[0]-1][coord[1]-1] = sym


def paint(game_board):
    global n
    global speed
    print("╔" + '═' * 2*n + "╗" + "     SCORE: " + str(speed-1))
    for row in game_board:
        print("║" + ''.join(row) + "║")
    print("╚" + '═' * 2*n + "╝")


def next_step(direction):
    global snake

    if direction == Key.left:
        if snake[0][1] - 1 < 1:
            return snake[0][0], snake[0][1] - 1 + n
        else:
            return snake[0][0], snake[0][1] - 1
    elif direction == Key.right:
        if snake[0][1] + 1 > n:
            return snake[0][0], snake[0][1] + 1 - n
        else:
            return snake[0][0], snake[0][1] + 1
    elif direction == Key.down:
        if snake[0][0] + 1 > m:
            return snake[0][0] + 1 - m, snake[0][1]
        else:
            return snake[0][0] + 1, snake[0][1]
    elif direction == Key.up:
        if snake[0][0] - 1 < 1:
            return snake[0][0] - 1 + m, snake[0][1]
        else:
            return snake[0][0] - 1, snake[0][1]


def move(direction):
    global snake
    snake.insert(0, next_step(direction))


def draw_food():
    global snake
    global food
    while (food in snake) or not food:
        food = (random.randint(1, m), random.randint(1, n))


def on_press(key):
    global current_direc
    global possible_directions
    global reversed_directions
    if key != current_direc:
        if key != reversed_directions[current_direc]:
            if (key in possible_directions) or key == Key.esc:
                current_direc = key


m = 15  # rows
n = 15  # columns
gameboard = [['  ' for i in range(n)] for i in range(m)]    # m wierszy po n kolumn
snake = [(5, 5)]
food = None  # wspolrzedne jedzenia
draw_food()

possible_directions = [Key.left, Key.right, Key.up, Key.down]   # kierunki
current_direc = random.choice(possible_directions)  # kierunek w ktorym sie obecnie poruszamy
reversed_directions = {possible_directions[0]: possible_directions[1], possible_directions[1]: possible_directions[0],
                       possible_directions[2]: possible_directions[3], possible_directions[3]: possible_directions[2]}

# poczatek programu, dane wejsciowe
insert_gameboard(u"\u2588" * 2, snake[0])
insert_gameboard(u"\u2593"*2, food)
speed = 1

while True:
    # rysujemy cala plansze
    # piksele zaktualizowane, teraz nalezy je wyswietlic
    os.system("cls")
    paint(gameboard)

    # teraz pora wybrac nowy kierunek

    with Listener(on_press=on_press) as ls:
        def time_out(period_sec: int):
            time.sleep(period_sec)  # Listen to keyboard for period_sec seconds
            ls.stop()


        Thread(target=time_out, args=(2*(speed**(-1/2)),)).start()
        ls.join()

    # wykonaj ruch - wprowadz nowe wspolrzedne do węża
    if current_direc == Key.esc:
        int(input("ile maksymalnie zywych z " + str(m*n) + " komórek? "))
        break
    else:
        move(current_direc)

        # pora sprawdzic warunki
        if snake[0] == food:
            draw_food()
            insert_gameboard(u"\u2593"*2, food)
            speed += 1
            # nie usuwamy koncowki ogona
        elif snake[0] in snake[1:]:
            os.system("cls")
            print("GAME OVER!!!")
            break

        else:
            insert_gameboard('  ', snake.pop()) # usuwamy koncowke ogona

        insert_gameboard(u"\u2588" * 2, snake[0])   # mozna oszczedzic linijke kodu i wstawic jedno


print("SCORE: " + str(speed-1))
input('Press ENTER to exit')

