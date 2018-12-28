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
    for (height, width), char in snowflakes.items():
        max_height, max_width  = window.getmaxyx()
        if height >= max_height - 1 or width >= max_width:
            continue
        window.addch(height, width, char)


def main(window):
    curses.curs_set(0)
    window.border()
    window.clear()
    snowflakes = {}
    
    while True:
        snowflakes = update_snowflakes(snowflakes, window)
        snowflake = snowflake_char(window)
        snowflakes[(snowflake[0], snowflake[1])] = snowflake[2]
        window.clear()
        redisplay(snowflakes, window)
        window.refresh()
        time.sleep(0.2)

    
if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
