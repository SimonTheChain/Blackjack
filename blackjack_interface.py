#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Blackjack Interface
#
# Author: Simon Lachaîne


import time
from colorama import init
from colorama import deinit

from blackjack_engine import Player
from blackjack_engine import BlackjackEngine


class BlackjackApp(object):

    def __init__(self):
        self.bje = BlackjackEngine()

    @staticmethod
    def hello():
        """
        Shows title
        :return: Sleep time
        """
        init()
        print("\n{}__Welcome to Blackjack__{}\n".format(
            '\x1b[1;37;44m',
            '\x1b[0m'))
        return time.sleep(0.5)

    @staticmethod
    def goodbye():
        """
        Shows credits and exits
        :return: Sleep time
        """
        print("\n\n{}Coded by Simon Lachaîne{}\n\n".format(
            '\x1b[1;37;44m',
            '\x1b[0m'))
        time.sleep(1)
        deinit()
        raise SystemExit

    def set_game_options(self):
        try:
            nb_of_players = int(input("Enter the number of human players: \n> "))

            try:
                self.bje.set_player_count(nb_of_players)

            except ValueError as e:
                return print(e)

        except TypeError:
            return print("Please enter an integer")

        try:
            nb_of_decks = int(input("Enter the number of decks to use: \n> "))

            try:
                self.bje.set_deck_count(nb_of_decks)

            except ValueError as e:
                return print(e)

        except TypeError:
            return print("Please enter an integer")

        return print("Game options set")

    def hand_results(self, agent):
        self.bje.calculate_hand(agent)

        if self.bje.has_blackjack(agent):
            print("{} has a blackjack!".format(agent.name))

        if self.bje.has_busted(agent):
            print("{} has busted!".format(agent.name))

        print("{}'s score: {}".format(agent.name, agent.score))
        print("{}'s hand: {}".format(agent.name, [card.name for card in agent.hand]))

    def player_turn(self, player):
        if isinstance(player, Player):
            self.hand_results(player)

            if player.blackjack:
                print("\nCongratulations, you have a blackjack!")
                return

            elif player.busted:
                print("\nYou have busted.")
                return

            while True:
                print("\nAvailable actions:")
                print("[1] Hit")
                print("[2] Stand")

                question = input("\nPlease select an action:\n> ")

                if question == "1":
                    card = self.bje.deck.give_first_card()
                    player.hit(card)

                if question == "2":
                    player.stand()
                    break

                else:
                    print("\n{}Please answer '1' or '2'{}".format(
                        '\x1b[1;37;41m',
                        '\x1b[0m'))

            self.hand_results(player)


def main():
    """
    Main program flow
    :return: None
    """
    app = BlackjackApp()
    app.hello()

    repeat = True
    while repeat:
        app.bje.reset_engine()
        app.set_game_options()
        app.bje.start_game()

        for player in app.bje.players:
            app.player_turn(player)

        while True:
            question = input("\nGame over; Play again? (y/n)\n> ")

            if question.lower() == "y" or question.lower() == "yes":
                app.bje.reset_engine()
                break

            elif question.lower() == "n" or question.lower() == "no":
                repeat = False
                break

            else:
                print("\n{}Please answer 'y' or 'n'{}".format(
                    '\x1b[1;37;41m',
                    '\x1b[0m'))

    app.goodbye()


if __name__ == "__main__":
    main()
