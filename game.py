###################################################################
# FILE: game.py
# WRITER: Daniel Sinai
# DESCRIPTION: This program implements the Game class
###################################################################
import boggle_board_randomizer as bbr
from board import Board


class Game:
    """
    This class manages the logical part of the game
    """
    SCORE_POWER = 2

    def __init__(self):
        """
        This function initializes a new instance
        """
        self.__game_board = self.create_board()
        self.__words_list = self.__game_board.get_words_list()
        self.__words_found = []
        self.__path = []

    def create_board(self):
        """
        This function creates a new game board
        :return: Board object
        """
        game_board = Board(bbr.BOARD_SIZE)
        game_board.init_board(bbr.randomize_board())
        return game_board

    def get_board_object(self):
        """
        This function returns the current game board
        :return: Board object
        """
        return self.__game_board

    def get_board_values(self):
        """
        This function returns the game board values
        :return: List of strings with the board values
        """
        return self.__game_board.get_board_values()

    def get_board_as_list(self):
        """
        This function returns the game board as list of lists
        :return: List of lists - game board
        """
        return self.__game_board.get_board()

    def calculate_word_score(self, path):
        """
        This function calculates the score for the word founded
        :param path: List of tuples - letters locations on the board
        :return: Integer - score
        """
        return (len(path)) ** self.SCORE_POWER
