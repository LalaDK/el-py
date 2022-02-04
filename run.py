#!/usr/bin/env python3
from actions import fetchAll, fetchLatest, show_latest
from utils import clear
from q import Q


def main_menu():
    clear()
    options = [
        "Vis data",
        "Hent data",
        "Afslut"
    ]

    answer = Q.ask("OK Data Downloader", options)
    if answer == 0:
        show_menu()
    elif answer == 1:
        fetch_menu()
    elif answer == 2:
        exit(0)


def show_menu():
    clear()
    options = [
        "Vis seneste data",
        "Vis i periode",
        "Tilbage..."
    ]

    answer = Q.ask("Hvilke data skal vises?", options)
    if answer == 0:
        fetchLatest()
        show_latest()
    elif answer == 1:
        fetchAll()
        main_menu()
    elif answer == 2:
        main_menu()


def fetch_menu():
    clear()
    options = [
        "Hent seneste data",
        "Hent alt data",
        "Tilbage..."
    ]

    answer = Q.ask("Hvilke data skal hentes?", options)
    if answer == 0:
        fetchLatest()
        main_menu()
    elif answer == 1:
        fetchAll()
        main_menu()
    elif answer == 2:
        main_menu()


main_menu()
