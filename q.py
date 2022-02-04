#! /usr/bin/env python3

import sys
import curses


class Q:
    __num_rows = 0
    __num_cols = 0
    __cursor = 0
    __options = []
    __screen = None

    def __init__(self, question, options):

        self.__screen = curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        self.__screen.keypad(True)

        self.__question = question
        self.__options = options
        self.__num_rows, self.__num_cols = self.__screen.getmaxyx()

    def __move_cursor(self, value):
        self.__cursor = self.__cursor + value
        if self.__cursor == len(self.__options):
            self.__cursor = 0
        elif self.__cursor < 0:
            self.__cursor = len(self.__options) - 1

    def __teardown(self):
        curses.endwin()

    def run(self):
        self.__draw()
        while True:
            try:
                char = self.__screen.getch()
            except KeyboardInterrupt:
                self.__teardown()
                sys.exit(0)

            if char == curses.KEY_UP:
                self.__move_cursor(-1)
            elif char == curses.KEY_DOWN:
                self.__move_cursor(1)
            elif char == 10:
                self.__teardown()
                return self.__cursor
            self.__draw()

    def __draw(self):
        self.__screen.erase()

        middle_row = int(self.__num_rows / 2) - \
            int(len(self.__options) / 2) - 1
        longest = max(self.__options)
        half_length_of_message = int(len(longest) / 2)
        middle_column = int(self.__num_cols / 2)
        x_position = middle_column - half_length_of_message

        self.__screen.addstr(middle_row, x_position,
                             self.__question, curses.A_BOLD)

        for idx, option in enumerate(self.__options):
            style = curses.A_REVERSE if idx == self.__cursor else 0
            self.__screen.addstr(
                middle_row + idx + 1, x_position, str(idx + 1) + ". " + option, style)

        self.__screen.refresh()

    @staticmethod
    def ask(question, options):
        q = Q(question, options)
        return q.run()


#Q.ask('Select option', ['Option A', 'Option B', 'Option C'])
