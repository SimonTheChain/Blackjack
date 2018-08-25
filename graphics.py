#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Deck of cards - Graphics
#
# Author: Simon Lachaîne

from PIL import Image
import numpy as np

import time
import logging

logging.basicConfig(level=logging.DEBUG)


class CardImages(object):
    """
    """
    def __init__(self, source_img_path):
        self.source_img_path = source_img_path
        self.source_img = self._open_source()
        self.cards = {}  # (suit, rank): img

    def _open_source(self):
        """
        """
        try:
            self.source_img = Image.open(self.source_img_path)
            logging.debug("Source image opened")
            return self.source_img

        except IOError as e:
            logging.warning("An error occurred while opening the source image:\n{}".format(e))

    def _crop_source(self, left, upper, right, lower, suit, rank):
        """
        """
        try:
            int(left)
            int(upper)
            int(right)
            int(lower)
            int(suit)
            int(rank)

        except TypeError as e:
            logging.warning("The arguments must be integers:\n{}".format(e))

        else:
            box = (left, upper, right, lower)
            region = self.source_img.crop(box)
            self.cards[(suit, rank)] = region

            # for dev only
            # region.save(
            #     "cards/{suit}-{rank}.png".format(
            #         suit=suit,
            #         rank=rank
            #     )
            # )
            # logging.debug("Card image saved")

    def create_cards(self):
        """
        """



        left_range = range(0, 2179, 168)
        left = [
            item for item in left_range
            for i in range(5)
        ]
        print("Left")
        print(len(left))
        logging.debug(left)

        upper_range = range(0, 1217, 243)
        upper = [
            item for item in upper_range
            for i in range(5)
        ]
        print("Upper")
        print(len(upper))
        logging.debug(upper)

        right_range = range(168, 2179, 168)
        right = [
            item for item in right_range
            for i in range(5)
        ]
        print("Right")
        print(len(right))
        logging.debug(right)

        lower_range = range(243, 1217, 243)
        lower = [
            item for item in lower_range
            for i in range(13)
        ]
        print("Lower")
        print(len(lower))
        logging.debug(lower)

        ###
        values = zip(
            left,
            upper,
            right,
            lower,
        )
        coordinates = list(values)
        logging.debug("Coordinates")
        logging.debug(coordinates)

        suits_ranks = [
            (
                i % 4,  # suit
                13 if i % 13 == 0 else i % 13  # rank
            )
            for i in range(1, 53)
        ]
        suits_ranks.sort()

        parameters = zip(
            coordinates,
            [suit_rank for suit_rank in suits_ranks]
        )
        # print("\nparameters:\n")
        # print(parameters)

        for p in parameters:
            # logging.debug(p)
            self._crop_source(
                left=p[0][0],
                upper=p[0][1],
                right=p[0][2],
                lower=p[0][3],
                suit=p[1][0],
                rank=p[1][1]
            )


def main():
    app = CardImages("cards.png")
    app.create_cards()

    # for card in app.cards:
    #     print(card)


if __name__ == "__main__":
    # main()
    grid = np.zeros((5, 13))
    # print(grid)
    points_left = np.linspace(0, 2179-167.54, 13)
    print("Left")
    print(len(points_left))
    print(points_left)

    points_upper = np.linspace(0, 1217 - 243.2, 5)
    print("Upper")
    print(len(points_upper))
    print(points_upper)

    points_right = np.linspace(167.54, 2179, 13)
    print("Right")
    print(len(points_right))
    print(points_right)

    points_lower = np.linspace(243.2, 1217, 5)
    print("Lower")
    print(len(points_lower))
    print(points_lower)
