#!/usr/bin/env python3

from monster import gamestate


def main():
    RUNNING = True
    monsters = []
    players = []
    gameboard = gamestate.Board(monsters, players)
    while RUNNING == True:
        choice = input("H for help :>")
        if choice.lower()[:1] == "h":
            print("Menu:")
            print("c: Create")
            print("p: Print board")
            print("a: attack")
            print("h: hit")
            print("r: end round")
        elif choice.lower()[:1] == "c":
            if choice.lower()[1:2] == "m":
                gameboard.create_monster(choice[3:], len(monsters)+1)
            elif choice.lower()[1:2] == "p":
                gameboard.create_player(choice[3:])
        elif choice.lower()[:1] == "p":
            gameboard.print_board()
        elif choice.lower()[:1]
        else:
            print("I'm sorry, that's not an option.")
            continue