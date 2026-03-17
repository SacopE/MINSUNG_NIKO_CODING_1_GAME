import curses
import random
import time

game_data = {
    'width': 7,
    'height': 7,
    'player': {'snake': [(1, 1)],
               'score': 0,
               'direction': 'south'},
    'collectibles': [
        {"x": 2, "y": 1, "collected": False},
    ],


    # ASCII icons
    'snake': "\U0001F40D",
    'empty': "  ",
    'apple': '\U0001F34E',
    'boarder': '\U00002B1B'

}

def display_welcome_screen():
    print(" ")
    print("Welcome to Snake!")
    print(" ")
    print("Use WSAD for movement")
    print("Avoid the sides")
    print("Eat All of the Apples!")

def draw_board(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)

    stdscr.clear()
    for y in range(game_data['height']):
        row = ""
        for x in range(game_data['width']):
            # Black Perimeter
            if y == 0 or y == game_data['height'] - 1 or x == 0 or x == game_data['width'] - 1:
                row += game_data['boarder']
            # Player
            elif (x, y) in game_data['player']['snake']:
                row += game_data['snake']   
            # Collectibles
            elif any(c['x'] == x and c['y'] == y and not c['collected'] for c in game_data['collectibles']):
                row += game_data['apple']
            else:
                row += game_data['empty']
        stdscr.addstr(y, 0, row, curses.color_pair(1))
    
    stdscr.addstr(game_data['height'] + 1, 0,
                  f"Score: {game_data['player']['score']}",
                  curses.color_pair(1))
    stdscr.addstr(game_data['height'] + 2, 0,
                  "Move with W/A/S/D, Q to quit",
                  curses.color_pair(1))
    stdscr.refresh()


def move_player(key):
    key = key.lower()

    if key == "w":
        game_data['player']['direction'] = 'north'
    elif key == "s":
        game_data['player']['direction'] = 'south'
    elif key == "a":
        game_data['player']['direction'] = 'west'
    elif key == "d":
        game_data['player']['direction'] = 'east'

def update_position():
    snake = game_data['player']['snake']
    head_x, head_y = snake[0]
    direction = game_data['player']['direction']

    if direction == 'north':
        head_y -= 1
    elif direction == 'south':
        head_y += 1
    elif direction == 'west':
        head_x -= 1
    elif direction == 'east':
        head_x += 1

    new_head = (head_x, head_y)

    if head_x == 0 or head_x == game_data['width'] - 1 or head_y == 0 or head_y == game_data['height'] - 1:
        return False
    
    if new_head in snake:
        return False
    
    snake.insert(0, new_head)

    ate_apple = False
    for c in game_data['collectibles']:
        if not c["collected"] and (head_x, head_y) == (c["x"], c["y"]):
            c["collected"] = True
            game_data['player']['score'] += 1
            spawn_apple()
            ate_apple = True
            break
    if not ate_apple:
        snake.pop()

    return True

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    draw_board(stdscr)

def spawn_apple():
    while True:
        x = random.randint(1, game_data['width'] - 2)
        y = random.randint(1, game_data['height'] - 2)

        # Don't spawn on the snake
        if (x, y) in game_data['player']['snake']:
            continue

        # Replace the apple list with ONE apple
        game_data['collectibles'] = [{"x": x, "y": y, "collected": False}]
        break

def play_snake(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)

    stdscr.nodelay(True)

    draw_board(stdscr)

    while True:
        try:
            key = stdscr.getkey()
        except:
            key = None

        if key:
            if key.lower() == 'q':
                break
            move_player(key)
        moved = update_position()

        if not moved:
            break


        draw_board(stdscr)

        time.sleep(0.5)

    stdscr.clear()
    stdscr.addstr(2, 2, "GAME OVER")
    stdscr.addstr(3, 2, f"Final Score: {game_data['player']['score']}")
    stdscr.refresh()
    time.sleep(3)

display_welcome_screen()
time.sleep(.0)
curses.wrapper(play_snake)

