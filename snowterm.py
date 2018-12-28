import curses
import random
import sys
import time


def snowflake_char(window):
    _, width = window.getmaxyx()
    char = random.choice(['+', '*', '.'])
    position = random.randrange(1, width)
    return (0, position, char)


def update_snowflakes(prev, window):
    new = {}
    for (height, position), char in prev.items():
        max_height, _ = window.getmaxyx()
        if height + 1 >= max_height - 1:
            new_height = height
        elif prev.get((height + 1, position)):
            new_height = height
        else:
            new_height = height + 1
        new[(new_height, position)] = char
    return new


def redisplay(snowflakes, window):
    for (height, position), char in snowflakes.items():
        max_height, max_width  = window.getmaxyx()
        if height >= max_height - 1 or position >= max_width:
            continue
        window.addch(height, position, char)


def draw_moon(window):
    moon = [
        '  **   ',
        '   *** ',
        '    ***',
        '    ***',
        '   *** ',
        '  **   ',
    ]
    start_position = window.getmaxyx()[1] - 10
    window.attrset(curses.color_pair(1))
    for height, line in enumerate(moon, start=1):
        for position, sym in enumerate(line, start=start_position):
            if sym.strip():
                window.addch(height, position, sym)
    window.attrset(curses.color_pair(0))


def main(window):
    if curses.can_change_color():
        curses.init_color(curses.COLOR_BLACK, 0,0,0)
        curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000)
        curses.init_color(curses.COLOR_YELLOW, 1000, 1000, 0)
    curses.init_pair(1, curses.COLOR_YELLOW, 0)
    curses.curs_set(0)
    window.border()
    snowflakes = {}
    while True:
        height, width = window.getmaxyx()
        if len(snowflakes.keys()) >= (height - 2) * width:
            snowflakes.clear()
        snowflakes = update_snowflakes(snowflakes, window)
        snowflake = snowflake_char(window)
        snowflakes[(snowflake[0], snowflake[1])] = snowflake[2]
        window.clear()
        draw_moon(window)
        redisplay(snowflakes, window)
        window.refresh()
        time.sleep(0.2)


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
