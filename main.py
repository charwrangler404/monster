#!/usr/bin/env python3

from monster import gamestate

def main():
    RUNNING = True
    monsters = []
    players = []
    gameboard = gamestate.Board(monsters, players)
    while RUNNING == True:
        choice = input(":> ")
        if choice.lower()[:4] == "help":
            print("Menu:")
            print("c: Create")
            print('Monsters: cm <num> zombie.json')
            print('Player: cp <init_roll>')
            print("p: Print board")
            print("a: Attack - a")
            print("h: Hit - h <index> <tohit> <dmg>")
            print("r: end Round")
            print("q: Quit")
        elif choice.lower()[:1] == "c":
            if choice.lower()[1:2] == "m":
                
                gameboard.create_monster(choice[3:], len(monsters)+1)
            elif choice.lower()[1:2] == "p":
                gameboard.create_player(choice[3:])
        elif choice.lower()[:1] == "p":
            gameboard.print_board()
        elif choice.lower()[:1] == "a":
            for monster in gameboard.monsters:
                monster.attack()
        elif choice.lower()[:1] == 'h':
            tohit = int(choice[5:7])
            damage = int(choice[8:])
            gameboard.monsters[int(choice[2:4])].hit(tohit, damage)
        elif choice.lower()[:1] == 'q':
            exit() 
        else:
            print(f"{choice}: Not a valid option")
            continue