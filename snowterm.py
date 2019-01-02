import curses
import random
import sys
import time


def max_dimensions(window):
    height, width = window.getmaxyx()
    return height - 2, width - 1


def snowflake_char(window):
    width = max_dimensions(window)[1]
    char = random.choice(['+', '*', '.'])
    position = random.randrange(1, width)
    return (0, position, char)


def update_snowflakes(prev, window):
    new = {}
    for (height, position), char in prev.items():
        max_height = max_dimensions(window)[0]
        new_height = height + 1
        if new_height > max_height or prev.get((new_height, position)):
            new_height -= 1
        new[(new_height, position)] = char
    return new


def redisplay(snowflakes, window):
    for (height, position), char in snowflakes.items():
        max_height, max_width = max_dimensions(window)
        if height > max_height or position >= max_width:
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
    start_position = max_dimensions(window)[1] - 10
    window.attrset(curses.color_pair(1))
    for height, line in enumerate(moon, start=1):
        for position, sym in enumerate(line, start=start_position):
            window.addch(height, position, sym)
    window.attrset(curses.color_pair(0))


def main(window, speed):
    if curses.can_change_color():
        curses.init_color(curses.COLOR_BLACK, 0,0,0)
        curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000)
        curses.init_color(curses.COLOR_YELLOW, 1000, 1000, 0)
    curses.init_pair(1, curses.COLOR_YELLOW, 0)
    try:
        curses.curs_set(0)
    except Exception:
        pass  # Can't hide cursor in 2019 huh?
    snowflakes = {}
    while True:
        height, width = max_dimensions(window)
        if len(snowflakes.keys()) >= 0.95 * (height * width):
            snowflakes.clear()
        snowflakes = update_snowflakes(snowflakes, window)
        snowflake = snowflake_char(window)
        snowflakes[(snowflake[0], snowflake[1])] = snowflake[2]
        window.clear()
        draw_moon(window)
        redisplay(snowflakes, window)
        window.refresh()
        try:
            time.sleep((0.2) / (speed / 100))
        except ZeroDivisionError:
            time.sleep(0.2)


if __name__ == '__main__':
    speed = 100
    if len(sys.argv) > 1:
        try:
            speed = int(sys.argv[1])
        except ValueError:
            print(
                'Usage:\npython snowterm.py [SPEED]\n'
                'SPEED is integer representing percents.',
            )
            sys.exit(1)
    try:
        curses.wrapper(main, speed)
    except KeyboardInterrupt:
        sys.exit(0)
