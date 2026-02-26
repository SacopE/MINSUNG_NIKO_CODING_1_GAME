import curses

game_data = {
    'width': 5,
    'height': 5,
    'player': {"x": 0, "y": 0, "score": 0,},
    'collectibles': [
        {"x": 2, "y": 1, "collected": False},
    ],


    # ASCII icons
    'snake': "\U0001F40D",
    'empty': "  ",
    'apple': '\U0001F34E'
}

def draw_board(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)

    stdscr.clear()
    for y in range(game_data['height']):
        row = ""
        for x in range(game_data['width']):
            # Player
            if x == game_data['player']['x'] and y == game_data['player']['y']:
                row += game_data['snake']
            # Collectibles
            elif any(c['x'] == x and c['y'] == y and not c['collected'] for c in game_data['collectibles']):
                row += game_data['apple']
            else:
                row += game_data['empty']
        stdscr.addstr(y, 0, row, curses.color_pair(1))

    stdscr.refresh()
    stdscr.getkey()  # pause so player can see board

curses.wrapper(draw_board)

game_data = {
    
}

<<<<<<< HEAD
def draw_board(screen):
    # Print the board and all game elements using curses


# Good Luck!
print("HI")
=======
>>>>>>> 8332e17 (Added icons)
