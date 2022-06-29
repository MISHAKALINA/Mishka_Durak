import random as r


def new_deck(a):
    while len(a) != 36:
        b = [suit[r.randint(0, 3)], value[r.randint(0, 8)]]
        if b not in a:
            a.append(b)
    for i in range(50):
        b = r.randint(0, 35)
        c = r.randint(0, 35)
        a[b], a[c] = a[c], a[b]


def distribution(a, b):
    global trump
    global deck
    new_deck(deck)
    for i in range(12):
        if i % 2 == 0:
            a.append(deck[i])
        elif i % 2 != 0:
            b.append(deck[i])
    deck = deck[12:]
    trump = deck[-1]


suit = ['♠', '♣', '♥', '♦']
value = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
player1 = []
player2 = []
name_player1 = ''
name_player2 = ''
deck = []
trump = []
flag = 1
playing_field = []
flag2 = 1


def start_game():
    global name_player1
    global name_player2
    print('''Добро пожаловать в дурака в Python.
Предупреждение! Если можно так сказать это альфа
Правила игры:
Без переводного!
При выборе карты индексация идёт от 1
Ответ, чтоб выполнилось действие только 'Да', остальные ответы считаются за 'Нет'
Я не писал финал игры, так что скорее всего она крашнется, исправлю
Будет приятно, если будет фидбек и по багам в самой программе и по её написанию!(Не бейте сильно)

Представьтесь, пожалуйста.''')
    name_player1 = input('Первый игрок: ')
    name_player2 = input('Второй игрок: ')
    print()
    distribution(player1, player2)
    print('Козырь в этой партии:', *trump, end='\n')
    first_game(name_player1, player1)


def first_game(a, b):
    global flag
    global flag2
    flag2 = 0
    if flag == 1:
        while len(player2) < 6 and len(deck) > 0:
            player2.append(deck[0])
            deck.pop(0)
        while len(player1) < 6 and len(deck) > 0:
            player1.append(deck[0])
            deck.pop(0)
    else:
        while len(player1) < 6 and len(deck) > 0:
            player1.append(deck[0])
            deck.pop(0)
        while len(player2) < 6 and len(deck) > 0:
            player2.append(deck[0])
            deck.pop(0)
    print('Колода игрока', a + ':', *[b[i][0] + ' ' + b[i][1] + '.' for i in range(len(b))])
    w = input('Вы играете карту номер: ')
    e = check(w, b)
    playing_field.append(b[e])
    b.pop(e)
    flag2 += 1
    game()


def game():
    global flag
    global flag2
    if (flag == 1 and flag2 % 2 == 0) or (flag == 2 and flag2 % 2 == 1):
        move(name_player1, player1)
    elif (flag == 1 and flag2 % 2 == 1) or (flag == 2 and flag2 % 2 == 0):
        move(name_player2, player2)
    flag2 += 1
    game()


def move(a, b):
    global playing_field
    global flag
    global flag2
    print('Колода игрока', a + ':', *[b[i][0] + ' ' + b[i][1] + '.' for i in range(len(b))])
    print('На столе сейчас: ',
          *[playing_field[i][0] + ' ' + playing_field[i][1] + '.' for i in range(len(playing_field))],
          'Вы играете против', *playing_field[-1], 'Козырь -',
          *trump)
    if flag == 1 and flag2 % 2 == 0:
        y = input('Бито? ')
        if y == 'Да':
            playing_field = []
            flag = 2
            first_game(name_player2, player2)
        attack(a, b)
    elif flag == 1 and flag2 % 2 == 1:
        y = input('Берете? ')
        if y == 'Да':
            for i in playing_field:
                b.append(i)
            playing_field = []
            first_game(name_player1, player1)
        defense(a, b)
    elif flag == 2 and flag2 % 2 == 0:
        y = input('Бито? ')
        if y == 'Да':
            playing_field = []
            flag = 1
            first_game(name_player1, player1)
        attack(a, b)
    elif flag == 2 and flag2 % 2 == 1:
        y = input('Берете? ')
        if y == 'Да':
            for i in playing_field:
                b.append(i)
            playing_field = []
            first_game(name_player2, player2)
        defense(a, b)


def check(a, q):
    f2 = False
    while not f2:
        if int(a) not in range(1, len(q) + 1):
            a = input('Пожалуйста назовите правильный номер карты от 1 до ' + str(len(q)) + ': ')
        else:
            print('Вы играете карту:', *q[int(a) - 1])
            e = int(a) - 1
            return e


def check_bito(q):
    global playing_field
    global trump
    if q[0] != trump[0] and playing_field[-1][0] == trump[0]:
        return False
    if q[0] == trump[0] and playing_field[-1][0] != trump[0]:
        return True
    if q[0] == playing_field[-1][0]:
        if int(iz_str_v_int(q[1])) > int(iz_str_v_int(playing_field[-1][1])):
            return True
        else:
            return False
    if q[0] != playing_field[-1][0]:
        return False


def iz_str_v_int(q):
    q = q.replace('J', '11')
    q = q.replace('Q', '12')
    q = q.replace('K', '13')
    q = q.replace('A', '14')
    return q


def defense(a, b):
    print('Вы играете против карты:', *playing_field[-1])
    w = input('Вы играете карту номер: ')
    e = check(w, b)
    if check_bito(b[e]):
        playing_field.append(b[e])
        b.pop(e)
    else:
        print('Выберете другую карту')
        move(a, b)


def attack(a, b):
    w = input('Вы играете карту номер: ')
    e = check(w, b)
    if may_attack(b[e]):
        playing_field.append(b[e])
        b.pop(e)
    else:
        print('Выберете другую карту')
        move(a, b)


def may_attack(b):
    global playing_field
    list1 = [playing_field[i][1] for i in range(len(playing_field))]
    if b[1] in list1:
        return True
    else:
        return False


start_game()
