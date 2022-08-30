#########################################################################
# FILE: boggle.py
# WRITER: Daniel Sinai
# DESCRIPTION: This program implements the controller of the boggle game
#########################################################################
import boggle_utils as utils
import boggle_gui as bg
from game import Game
import tkinter as tk
from tkinter import messagebox


class BoggleController:
    """
    This class control's the boggle game and combines between the GUI and the
    logical part
    """
    INVALID_WORD_MSG = "Your word is not in the dictionary or your path is" \
                       " illegal. Please try again"
    FOUND_SAME_WORD_MSG = 'You already found this word'
    TIME_OVER_MSG = "Your time is over! Would you like to start a new game? "

    def __init__(self):
        """
        This function initializes a new controller
        """
        self.__mainframe = Game()
        self.random_board = self.__mainframe.get_board_values()
        self.__gui = bg.BoggleGUI(self.random_board,
                                  self.__mainframe.get_board_object().get_cells(),
                                  self.reset)
        self.words_list = self.__mainframe.get_board_object().get_words_list()
        self.__gui.check_word_button.bind("<Button-1>",
                                          func=self.click_check_word)

    def get_gui(self):
        """
        This function returns the GUI object of the controller
        :return:
        """
        return self.__gui

    def click_check_word(self, event):
        """
        This function handles an event where the player selects letters and
         wants to check if they make up a valid word
        :param event: Object
        :return: None
        """
        potential_word = utils.is_valid_path(self.__mainframe.get_board_as_list(),
                                             self.__gui.get_current_word_path(),
                                             self.words_list)
        if potential_word in self.__gui.words_found:
            tk.messagebox.showinfo("Word already found",
                                   self.FOUND_SAME_WORD_MSG)
            self.__gui.reset_word()
        elif potential_word:
            self.__gui.current_score += self.__mainframe.calculate_word_score(
                self.__gui.get_current_word_path())
            self.__gui.update_score()
            self.__gui.update_words_found_list(potential_word)
            self.__gui.update_words_found_frame()
            self.__gui.reset_word()
        else:
            tk.messagebox.showinfo("Invalid Word", self.INVALID_WORD_MSG)
            self.__gui.reset_word()
        return "break"

    def run(self):
        """
        This function runs the game
        :return: None
        """
        self.__gui.run()

    def reset(self):
        """
        This function resets the game and starts a new one if the player
        choose to play again
        :return: None
        """
        time_over = messagebox.askquestion("Time's Up", self.TIME_OVER_MSG)
        if time_over == "no":
            self.__gui.root.destroy()
        else:
            self.__gui.root.destroy()
            new_game = BoggleController()
            new_game.run()


if __name__ == "__main__":
    new = BoggleController()
    new.run()
