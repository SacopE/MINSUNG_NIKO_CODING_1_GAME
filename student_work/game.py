import curses
import random
import time

game_data = {
    'width': 7,
    'height': 7,
    'player': {"x": 1, "y": 1, "score": 0, 'direction': 'south'},
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
            elif x == game_data['player']['x'] and y == game_data['player']['y']:
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

def check_collectibles():
    for c in game_data['collectibles']:
        if (not c["collected"] and
            game_data['player']["x"] == c["x"] and
            game_data['player']["y"] == c["y"]):

            c["collected"] = True
            game_data['player']['score'] += 1

def move_player(key):
    key = key.lower()
    x = game_data['player']['x']
    y = game_data['player']['y']

    new_x, new_y = x, y

    if key == "w" and y > 0:
        new_y -= 1
    elif key == "s" and y < game_data['height'] - 1:
        new_y += 1
    elif key == "a" and x > 0:
        new_x -= 1
    elif key == "d" and x < game_data['width'] - 1:
        new_x += 1
    else:
        return  # Invalid key or move off board

    # Update position and increment score
    game_data['player']['x'] = new_x
    game_data['player']['y'] = new_y

    return True

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    draw_board(stdscr)

def spawn_apple():
    active_apples = [c for c in game_data['collectibles'] if not c['collected']]
    if len(active_apples) >= 3:
        return
    if random.random() > 0.2:
        return

    while True:
        x = random.randint(1, game_data['width'] - 2)
        y = random.randint(0, game_data['height'] - 2)

        if (x, y) == (game_data['player']['x'], game_data['player']['y']):
            continue
        if any(c['x'] == x and c['y'] == y and not c['collected'] for c in game_data['collectibles']):
            continue

        game_data['collectibles'].append({"x": x, "y": y, "collected": False})
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
            if key.lower() == "q":
                break

            moved = move_player(key)

            if moved:
                check_collectibles()
                spawn_apple()


        draw_board(stdscr)

        time.sleep(0.1)

    stdscr.clear()
    stdscr.addstr(2, 2, "GAME OVER")
    stdscr.addstr(3, 2, f"Final Score: {game_data['player']['score']}")
    stdscr.refresh()
    time.sleep(3)

display_welcome_screen()
time.sleep(5.0)
curses.wrapper(play_snake)

