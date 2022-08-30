###################################################################
# FILE: board.py
# WRITER: Daniel Sinai
# DESCRIPTION: This program implements the Board class
###################################################################

FILE_PATH = "boggle_dict.txt"


class Board:
    """
    This class represents a single board
    """
    def __init__(self, board_size):
        """
        This function initializes a new instance
        :param board_size:
        """
        self.__board_size = board_size
        self.__cells = self.create_cells()
        self.__board = []
        self.__words_list = self.init_words(FILE_PATH)

    def init_board(self, game_board):
        """
        This function initializes the board
        :param game_board:
        :return: None
        """
        self.__board = game_board

    def init_words(self, file_path):
        """
        This function loads the words from the dictionary to the words list
        :param file_path: String - path to the dictionary file
        :return: List of string - words list
        """
        final_list = []
        with open(file_path) as f:
            for word in f:
                final_list.append(word.strip())
        return final_list

    def get_cells(self):
        """
        This function returns the board cells
        :return: List of tuples - board cells
        """
        return self.__cells

    def get_cube_value(self, x, y):
        """
        This function returns the value of (x, y) cube
        :param x:
        :param y:
        :return:
        """
        if (x, y) in self.__cells:
            return self.__board[x][y]
        return

    def get_words_list(self):
        """
        This function returns the board's words list
        :return:
        """
        return self.__words_list

    def get_board_values(self):
        """
        This function returns the board's values
        :return: List of string - board values
        """
        lst = []
        for i in range(self.__board_size):
            for j in range(self.__board_size):
                lst.append(self.get_cube_value(i, j))
        return lst

    def get_board(self):
        """
        This function returns the board
        :return: List of lists - board
        """
        return self.__board

    def create_cells(self):
        """
        This function creates the board cells
        :return: List of tuples - board cells
        """
        return [(i, j) for i in range(self.__board_size)
                for j in range(self.__board_size)]
