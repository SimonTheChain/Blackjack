#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Blackjack Engine
#
# Author: Simon Lachaîne


from deck_of_cards.deck_of_cards import Card, DeckOfCards

import logging

logging.basicConfig(level=logging.WARNING)


class EngineError(Exception):
    pass


class Player(object):

    def __init__(self):
        """
        Initializes the player object
        """
        self.id = 0
        self.name = "Player {}".format(self.id)
        self.hand = []
        self.bet = 0
        self.bank = 0
        self.score = 0
        self.blackjack = False
        self.busted = False

    def hit(self, card):
        """
        Adds a card to the player's hand
        :param card: instance of Card
        :return: player's hand
        """
        if isinstance(card, Card):
            self.hand.append(card)
            return self.hand

        else:
            raise ValueError("The parameter for the 'hit' method must be an instance of Card")

    def stand(self):
        """
        Dummy method to make things more readable
        :return: none
        """
        pass

    def double_down(self, percent):
        """
        Increases the player's bet
        :param percent: percentage by which to increase the bet
        :return: player's bet
        """
        if isinstance(percent, int):
            self.bet = self.bet * percent
            return self.bet

        else:
            raise ValueError("The parameter for the double_down method must be an integer")

    def split(self):
        pass

    def surrender(self):
        pass


class Dealer(object):

    def __init__(self):
        """
        Initializes the dealer object
        """
        self.name = "Dealer"
        self.hand = []
        self.bank = 0
        self.score = 0
        self.blackjack = False
        self.busted = False

    def hit(self, card):
        """
        Adds a card to the dealer's hand
        :param card: instance of Card
        :return: dealer's hand
        """
        if isinstance(card, Card):
            self.hand.append(card)
            return self.hand

        else:
            raise ValueError("The parameter for the 'hit' method must be an instance of Card")

    def stand(self):
        """
        Dummy method to make things more readable
        :return: none
        """
        pass


class BlackjackEngine(object):

    def __init__(self):
        """
        Initializes the engine object
        """
        self.deck = self._adjust_values(DeckOfCards())
        self.dealer = Dealer()
        self.players = []

    @staticmethod
    def _adjust_values(deck_obj):
        """
        Adjusts the values of the cards for blackjack
        :param deck_obj: an instance of DeckOfCards
        :return: deck object
        """
        # add if isintance(deck_obj, Deck)
        for card in deck_obj.deck:
            if card.value == 11 or card.value == 12 or card.value == 13:
                card.value = 10

            elif card.value == 1:
                card.value = 11

        return deck_obj

    def _add_player(self, index_player=0):
        """
        Adds a player to the list of players
        :return: list of players
        """
        player = Player()
        player.id = index_player
        return self.players.append(player)

    @staticmethod
    def calculate_hand(agent):
        """
        Calculates the values in the hand
        :param agent: dealer or player object
        :return: score
        """
        score = 0
        for card in agent.hand:
            score += card.value

        # adjust the value of the aces
        if score > 21:
            for card in agent.hand:
                if card.rank == 1 and card.value == 11:
                    card.value = 1
                    score = score - 10

                    if score < 21:
                        break

        agent.score = score
        return agent.score

    @staticmethod
    def has_busted(agent):
        """
        Verifies if the agent has busted
        :param agent: player or dealer
        :return: True if busted else False
        """
        if agent.score > 21:
            agent.busted = True
            return agent.busted

        return False

    @staticmethod
    def has_blackjack(agent):
        """
        Verifies if the agent has a blackjack
        :param agent: player or dealer
        :return: True if blackjack else False
        """
        if agent.score == 21 and len(agent.hand) <= 2:
            agent.blackjack = True
            return agent.blackjack

        return False

    def set_deck_count(self, nb_of_decks):
        """
        Sets the number of decks to use
        :param nb_of_decks: number of decks to use
        :return: deck object
        """
        if isinstance(nb_of_decks, int):
            if nb_of_decks > 1:
                for deck_nb in range(2, nb_of_decks + 1):
                    self._adjust_values(DeckOfCards())

            return self.deck

        else:
            raise ValueError("The parameter for the 'set_deck_count' method must be an integer")

    def set_player_count(self, nb_of_players):
        """
        Sets the number of human players
        :param nb_of_players: number of active players
        :return: players list
        """
        if isinstance(nb_of_players, int):
            if nb_of_players >= 1:
                for player_nb in range(1, nb_of_players + 1):
                    self._add_player(index_player=player_nb)

                return self.players

            else:
                raise ValueError("There must be at least one human player")

        else:
            raise ValueError("The parameter for the 'set_player_count' method must be an integer")

    def start_game(self):
        self.deck.shuffle_deck()

        for player in self.players:
            for i in range(2):
                player.hit(self.deck.give_first_card())

        self.dealer.hit(self.deck.give_first_card())

    def dealer_turn(self):
        event = self.check_score(self.dealer)

        while self.dealer.score < 17:
            self.dealer.hit(self.deck.give_first_card())
            event = self.check_score(self.dealer)

            if event:
                break

    def player_turn(self, player, action):

        event = self.check_score(player)

        if event:
            return event

        return None

    def reset_engine(self):
        self.deck = self._adjust_values(DeckOfCards())
        self.dealer = Dealer()
        self.players.clear()


def main():
    """
    Example usage
    :return: None
    """
    def hand_results(agent):
        bje.calculate_hand(agent)

        if bje.has_blackjack(agent):
            print("{} has a blackjack!".format(agent.name))

        if bje.has_busted(agent):
            print("{} has busted!".format(agent.name))

        print("{}'s score: {}".format(agent.name, agent.score))
        print("{}'s hand: {}".format(agent.name, [card.name for card in agent.hand]))

    print("Welcome to blackjack\n")
    bje = BlackjackEngine()
    bje.set_player_count(1)
    bje.set_deck_count(1)
    bje.start_game()

    # player turn
    hand_results(bje.dealer)
    print("_{}'s turn_\n".format(bje.players[-1].name))
    hand_results(bje.players[-1])
    
    
    

    # while True:
    #     hit = input("\nDo you want to hit? (y/n)\n> ")
    #
    #     if hit[0].lower() == "y":
    #         bje.players[-1].hit(bje.deck.give_first_card())
    #         bje.calculate_hand(bje.players[-1])
    #         print("\nPlayer's score: {}".format(bje.players[-1].score))
    #         print("Player's hand: {}".format([card.name for card in bje.players[-1].hand]))
    #
    #     else:
    #         break


if __name__ == "__main__":
    main()
