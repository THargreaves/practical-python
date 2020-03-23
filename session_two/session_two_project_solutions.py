# -*- coding: utf-8 -*-
"""
Model solution for session two of the AZ Practical Python Course.

This script implements a game of higher or lower using follower counts scraped
from various celebrity's Twitter accounts. On top of the basic functionality,
the solution allows for multiple 'lives' as well as a high score board. The
high score board is saved between execusions of the script in a special type of
file known as a pickle, which can then be loaded when the script is re-ran. As
with the previous solution, basic testing is performed when the script is ran.
Once testing is complete, the game will begin playing.

@author: Tim Hargreaves
"""


import os
import pickle
import random
import time
import unittest

from session_two_helpers import get_celeb_twitters, get_follower_count


def higher_or_lower(lives=1, high_score_board={}):
    """
    Play a game of higher or lower and update the high score board.

    Play a game of higher or lower with the specified number of lives. On
    completion, update the high score board as ask to play again.

    Args:
        lives (int): The number of lives for the game
        high_score_board (dict): The current high score for each named player

    Returns:
        high_score_board (dict): An updated high_score_board

    Raises:
        TypeError: If `lives` or any value of `high_score_board` is not an
                integer
        ValueError: If `lives` is non-positive or any value of
                `high_score_board` is negative
    """
    # validate inputs
    if not isinstance(lives, int):
        raise TypeError("lives must be a positive integer")
    if lives < 1:
        raise ValueError("lives must be a positive integer")
    if any(not isinstance(v, int) for v in high_score_board.values()):
        raise TypeError("high_score_board must have non-negative integer" +
                        "values")
    if any(v < 0 for v in high_score_board.values()):
        raise ValueError("high_score_board must have non-negative integer" +
                         "values")

    # collect celebrity twitter urls and convert to list for random choice
    print("Loading celebrity list...")
    twitter_urls = list(get_celeb_twitters(verbose=False).items())

    keep_playing = True
    name = None
    while keep_playing:
        # ask for name if not known
        if not name:
            name = input("What is your name?\r\n")

        incorrect_guesses = 0
        score = 0

        curr_celeb_name, curr_celeb_followers = random_celeb(twitter_urls)
        while incorrect_guesses < lives:
            next_celeb_name, next_celeb_followers = random_celeb(twitter_urls)

            clear_output()
            print("Your score is", score, "and you have",
                  lives - incorrect_guesses,
                  "life" if lives - incorrect_guesses == 1 else "lives",
                  "remaining")

            print(curr_celeb_name, "has", curr_celeb_followers,
                  "Twitter followers")
            print("Does", next_celeb_name, "have a higher or lower number",
                  "of followers? (h/l)")
            valid_response = False
            while not valid_response:
                response = input('')
                if response in ('h', 'l'):
                    valid_response = True
                else:
                    print("Please type one of 'h' (higher) or 'l' (lower)")
            correct = ((response == 'h' and
                        next_celeb_followers >= curr_celeb_followers) or
                       (response == 'l' and
                        next_celeb_followers <= curr_celeb_followers))
            if correct:
                print("Correct!", next_celeb_name, "has",
                      next_celeb_followers, "followers")
                curr_celeb_name, curr_celeb_followers = \
                    next_celeb_name, next_celeb_followers
                score += 1
            else:
                print("Not quite!", next_celeb_name, "has",
                      next_celeb_followers, "followers")
                incorrect_guesses += 1
            # pause for a second to give user a chance to read
            time.sleep(1)
        print("Sorry you've ran out of lives!")

        # update high score
        high_score_board[name] = max(score, high_score_board.get(name, 0))

        # ask to play again
        print("Would you like to play again? (y/n/c)")
        print("[y] yes")
        print("[n] no")
        print("[c] yes, and change name")
        valid_response = False
        while not valid_response:
            response = input()
            if response in ('y', 'n', 'c'):
                valid_response = True
            else:
                print("Please type one of 'y', 'n' or 'c'")
        if response == 'n':
            keep_playing = False
        elif response == 'c':
            name = None

    return high_score_board


def clear_output():
    """Clear the console output.

    This is the equivalent of `IPython.display.clear_output()` for
    non-interactive Python"""
    os.system('cls' if os.name == 'nt' else 'clear')


def random_celeb(twitter_urls):
    """Choose a random celebrity and return their name and follower count."""
    followers = None
    # some celebrities have no follower count so loop over these
    while followers is None:
        name, url = random.choice(twitter_urls)
        followers = get_follower_count(url)
    return name, followers


class TestHigherOrLower(unittest.TestCase):
    """A class for testing the Higher or Lower game."""

    def test_invalid_lives(self):
        with self.assertRaises(TypeError):
            higher_or_lower(lives='spam')
        with self.assertRaises(ValueError):
            higher_or_lower(lives=0)

    def test_invalid_high_score_board(self):
        with self.assertRaises(TypeError):
            higher_or_lower(high_score_board={'Ann': 'spam'})
        with self.assertRaises(ValueError):
            higher_or_lower(high_score_board={'Ann': -1})


if __name__ == '__main__':
    unittest.main()

    # load high scores if exist
    if os.path.exists('highscores.pkl'):
        print('Previous high score board found...loading')
        with open('highscores.pkl', 'rb') as f:
            high_score_board = pickle.load(f)
    else:
        high_score_board = {}

    high_score_board = higher_or_lower(3, high_score_board)

    print("High score board:")
    print({k: v for k, v in sorted(high_score_board.items(),
                                   key=lambda x: x[1])})

    with open('highscores.pkl', 'wb') as f:
        pickle.dump(high_score_board, f)
