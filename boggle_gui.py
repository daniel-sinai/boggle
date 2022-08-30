###################################################################
# FILE: boggle_gui.py
# WRITER: Daniel Sinai
# DESCRIPTION: This program implements the GUI of the boggle game
###################################################################
import tkinter as tk
from tkinter import messagebox

WOODEN_BOARD_PATH = "wooden_boggle_board.gif"
TITLE = "Boggle Game"
ALREADY_CHOSEN = "You have already chosen that word"


class BoggleGUI:
    """
    This class implements the GUI of the boggle game
    """

    def __init__(self, button_names_list, cells_list, reset_game_func):
        """
        This function initializes a new GUI object
        :param button_names_list: List of strings - letters for the board
        :param cells_list: List of tuples - board cells
        :param reset_game_func: Function to reset the game if necessary
        """
        self.current_word = ''
        self.button_names_list = button_names_list
        self.root = tk.Tk()
        self.root.title(TITLE)
        self.root.resizable(False, False)
        self.words_found = []
        self.locations_list = cells_list
        self.__current_word_path = []
        self.current_score = 0
        self.reset_game_func = reset_game_func
        self.background_image = tk.PhotoImage(file=WOODEN_BOARD_PATH)

        self.__buttons_list = \
            [self.__create_single_button(self.root, "", "") for _ in range(16)]

        self.__board_canvas = tk.Canvas(self.root, width=650, height=500)
        self.__board_canvas.pack()
        self.__main_window = self.__board_canvas

        self.__mins = tk.StringVar()
        self.__sec = tk.StringVar()
        self.__total_time = 0
        self.__score_var = tk.StringVar()
        self.__words_found_var = tk.StringVar()

        self.__init_background_label()
        self.__init_start_game_button()
        self.__init_timer_frame()
        self.__init_score_frame()
        self.__init_words_found()
        self.__init_check_word_button()
        self.__init_reset_word_button()
        self.__init_current_word_label()

        self.root.protocol('WM_DELETE_WINDOW', self.__on_close)

    def __init_background_label(self):
        """
        This function creates the background label
        :return: None
        """
        self.__background_label = tk.Label(self.root,
                                           image=self.background_image)
        self.__background_label.place(x=0, y=50)

    def __init_current_word_label(self):
        """
        This function creates the current word label
        :return: None
        """
        self.your_word_is_label = tk.Label(self.root, text="Your Word Is:",
                                           font="Helvetica 10 bold")
        self.your_word_is_label.place(x=508, y=200)

        self._current_word_label = tk.Label(self.root, text=self.current_word)
        self._current_word_label.place(x=508, y=220)

    def __init_reset_word_button(self):
        """
        This function creates the "reset word" button
        :return: None
        """
        self.__reset_word_button = tk.Button(self.root, text="Reset Word",
                                             bg="#c07202",
                                             font="Helvetica 10 bold",
                                             command=self.reset_word)
        self.__reset_word_button.place(x=508, y=150)

    def __init_check_word_button(self):
        """
        This function creates the "check word" button
        :return: None
        """
        self.check_word_button = tk.Button(self.root, text="Check Word",
                                           font="Helvetica 10 bold",
                                           bg="#c07202")
        self.check_word_button.place(x=506, y=110)

    def __init_start_game_button(self):
        """
        This function creates the "start game" button
        :return: None
        """
        self.__game_start = lambda: [self.__countdown_timer(),
                                     self.__create_buttons(
                                         self.root, self.button_names_list),
                                     self.root.after(181000,
                                                     self.reset_game_func)]

        self.__start_game_button = tk.Button(self.root, text="Start The Game",
                                             font="Helvetica 10 bold",
                                             bg="#c07202",
                                             command=self.__game_start)
        self.__start_game_button.place(x=500, y=12)

    def __init_timer_frame(self):
        """
        This function creates the timer frame
        :return: None
        """
        self.__timer_frame = tk.Frame(self.root, width=70, height=30,
                                      relief='solid', bd=1)
        self.__timer_frame.place(x=505, y=53)
        self.__show_time()
        self.__mins_label = tk.Label(self.__timer_frame,
                                     textvariable=self.__mins,
                                     width=3, font="Helvetica 20")
        self.__mins_label.pack(side=tk.LEFT)

        self.__sec_label = tk.Label(self.__timer_frame,
                                    textvariable=self.__sec,
                                    width=2, font="Helvetica 20")
        self.__sec_label.pack(side=tk.RIGHT)

    def __init_words_found(self):
        """
        This function creates the "words found" frame
        :return: None
        """
        self.general_label = tk.Label(self.root,
                                      text='Words Found:',
                                      font="Helvetica 10 bold")
        self.general_label.place(x=508, y=240)

        self.__words_found_frame = tk.Frame(self.root, width=160, height=20,
                                            relief="solid", bd=1)
        self.__words_found_frame.place(x=460, y=265)
        self.__words_found_var.set(self.__words_found_var.get() +
                                   "\n".join(self.words_found))

        self.__words_label = tk.Label(self.__words_found_frame,
                                      textvariable=self.__words_found_var,
                                      width=25, height=15, font="Helvetica 9")
        self.__words_label.pack(fill=tk.BOTH, expand=True)

    def __init_score_frame(self):
        """
        This function creates the score frame
        :return: None
        """
        self.__score_frame = tk.Frame(self.root)
        self.__score_frame.place(x=170, y=8)
        self.update_score()
        self._score_label = tk.Label(self.__score_frame, borderwidth=2,
                                     relief="ridge",
                                     textvariable=self.__score_var,
                                     font=("Ariel", 20))
        self._score_label.grid(row=0, column=0)

    def get_guess_word(self):
        """
        This function returns the current chosen word
        :return: String - word
        """
        return self.current_word

    def get_current_word_path(self):
        """
        This function returns the current word chosen path
        :return: List of tuples - path
        """
        return self.__current_word_path

    def reset_word(self):
        """
        This function resets the current word chosen
        :return: None
        """
        self.current_word = ''
        self.__current_word_path = []
        self._current_word_label.config(text='')
        [self.__make_enabled(self.__buttons_list[i]) for i in range(16)]

    def __add_click_to_word(self, letter):
        """
        This function adds a letter to the current word when the player clicks
        on a letter's button
        :param letter: String - letter
        :return: None
        """
        self.current_word += letter
        self._current_word_label.config(text=self.current_word)

    def update_words_found_frame(self):
        """
        This function updates the "words found" frame when the player finds
        a new word
        :return: None
        """
        self.__words_found_var.set("" + "\n".join(self.words_found))

    def __on_close(self):
        """
        This function pops up a window when the player wants to leave the game
        :return: None
        """
        response = messagebox.askyesno('Exit',
                                       'Are you sure you want to exit?')
        if response:
            self.root.destroy()

    def __show_time(self):
        """
        This function sets the timer for the beginning of the game
        :return: None
        """
        self.__mins.set("03")
        self.__sec.set("00")

    def update_score(self):
        """
        This function updates the player's score when a new word is found
        :return: None
        """
        self.__score_var.set("Score: " + str(self.current_score))

    def __countdown_timer(self):
        """
        This function creates a countdown timer for the game
        :return: None
        """
        self.__make_disabled(self.__start_game_button)
        self.__total_time = int(self.__mins.get()) * 60 + int(self.__sec.get())
        if self.__total_time > 0:
            self.__total_time -= 1
            minute, second = divmod(self.__total_time, 60)
            self.__sec.set(str(second))
            self.__mins.set(str(minute))
            self.root.update()
            self.root.after(1000, self.__countdown_timer)

    def __create_single_button(self, root, bt_text, cmd):
        """
        This function creates a single button
        :param root: Current tkinter root
        :param bt_text: String - letter
        :param cmd: Function - command to the button
        :return: Tkinter button
        """
        return tk.Button(root, text=bt_text, height=5, width=11,
                         command=cmd, bg='#c07202', fg='white',
                         disabledforeground='blue', font=('Lucida Grande', 9,
                                                          'bold'))

    def __make_disabled(self, button):
        """
        This function disables a button
        :param button: Button to be disabled
        :return: None
        """
        button['state'] = 'disabled'

    def __make_enabled(self, button):
        """
        This function enables a given button
        :param button: Button to be enabled
        :return: None
        """
        button['state'] = 'normal'

    def add_to_location_list(self, i):
        """
        This function adds a cell to the current path list when the player
        clicks on a new letter button
        :param i: Integer number - index
        :return: None
        """
        self.__current_word_path.append(self.locations_list[i])

    def __create_buttons(self, root, button_text_lst):
        """
        This function creates the letters buttons for the game
        :param root: Tkinter root
        :param button_text_lst: List of string - letters
        :return: None
        """
        button1_actions = lambda: [self.__add_click_to_word(button_text_lst[0]),
                                   self.__make_disabled(self.__buttons_list[0]),
                                   self.add_to_location_list(0)]

        self.__buttons_list[0] = self.__create_single_button(root,
                                                             button_text_lst[0],
                                                             button1_actions)
        self.__buttons_list[0].place(x=40, y=80)

        button2_actions = lambda: [self.__add_click_to_word(button_text_lst[1]),
                                   self.__make_disabled(self.__buttons_list[1]),
                                   self.add_to_location_list(1)]

        self.__buttons_list[1] = self.__create_single_button(root,
                                                             button_text_lst[1],
                                                             button2_actions)
        self.__buttons_list[1].place(x=136, y=80)

        button3_actions = lambda: [self.__add_click_to_word(button_text_lst[2]),
                                   self.__make_disabled(self.__buttons_list[2]),
                                   self.add_to_location_list(2)]

        self.__buttons_list[2] = self.__create_single_button(root,
                                                             button_text_lst[2],
                                                             button3_actions)
        self.__buttons_list[2].place(x=232, y=80)

        button4_actions = lambda: [self.__add_click_to_word(button_text_lst[3]),
                                   self.__make_disabled(self.__buttons_list[3]),
                                   self.add_to_location_list(3)]

        self.__buttons_list[3] = self.__create_single_button(root,
                                                             button_text_lst[3],
                                                             button4_actions)
        self.__buttons_list[3].place(x=328, y=80)

        button5_actions = lambda: [self.__add_click_to_word(button_text_lst[4]),
                                   self.__make_disabled(self.__buttons_list[4]),
                                   self.add_to_location_list(4)]

        self.__buttons_list[4] = self.__create_single_button(root,
                                                             button_text_lst[4],
                                                             button5_actions)
        self.__buttons_list[4].place(x=40, y=174)

        button6_actions = lambda: [self.__add_click_to_word(button_text_lst[5]),
                                   self.__make_disabled(self.__buttons_list[5]),
                                   self.add_to_location_list(5)]

        self.__buttons_list[5] = self.__create_single_button(root,
                                                             button_text_lst[5],
                                                             button6_actions)
        self.__buttons_list[5].place(x=136, y=174)

        button7_actions = lambda: [self.__add_click_to_word(button_text_lst[6]),
                                   self.__make_disabled(self.__buttons_list[6]),
                                   self.add_to_location_list(6)]

        self.__buttons_list[6] = self.__create_single_button(root,
                                                             button_text_lst[6],
                                                             button7_actions)
        self.__buttons_list[6].place(x=232, y=174)

        button8_actions = lambda: [self.__add_click_to_word(button_text_lst[7]),
                                   self.__make_disabled(self.__buttons_list[7]),
                                   self.add_to_location_list(7)]

        self.__buttons_list[7] = self.__create_single_button(root,
                                                             button_text_lst[7],
                                                             button8_actions)
        self.__buttons_list[7].place(x=328, y=174)

        button9_actions = lambda: [self.__add_click_to_word(button_text_lst[8]),
                                   self.__make_disabled(self.__buttons_list[8]),
                                   self.add_to_location_list(8)]

        self.__buttons_list[8] = self.__create_single_button(root,
                                                             button_text_lst[8],
                                                             button9_actions)
        self.__buttons_list[8].place(x=40, y=275)

        button10_actions = lambda: [self.__add_click_to_word(button_text_lst[9]),
                                    self.__make_disabled(self.__buttons_list[9]),
                                    self.add_to_location_list(9)]

        self.__buttons_list[9] = self.__create_single_button(root,
                                                             button_text_lst[9],
                                                             button10_actions)
        self.__buttons_list[9].place(x=136, y=275)

        button11_actions = lambda: [self.__add_click_to_word(button_text_lst[10]),
                                    self.__make_disabled(self.__buttons_list[10]),
                                    self.add_to_location_list(10)]

        self.__buttons_list[10] = self.__create_single_button(root,
                                                              button_text_lst[10],
                                                              button11_actions)
        self.__buttons_list[10].place(x=232, y=275)

        button12_actions = lambda: [self.__add_click_to_word(button_text_lst[11]),
                                    self.__make_disabled(self.__buttons_list[11]),
                                    self.add_to_location_list(11)]

        self.__buttons_list[11] = self.__create_single_button(root,
                                                              button_text_lst[11],
                                                              button12_actions)
        self.__buttons_list[11].place(x=328, y=275)

        button13_actions = lambda: [self.__add_click_to_word(button_text_lst[12]),
                                    self.__make_disabled(self.__buttons_list[12]),
                                    self.add_to_location_list(12)]

        self.__buttons_list[12] = self.__create_single_button(root,
                                                              button_text_lst[12],
                                                              button13_actions)
        self.__buttons_list[12].place(x=40, y=370)

        button14_actions = lambda: [self.__add_click_to_word(button_text_lst[13]),
                                    self.__make_disabled(self.__buttons_list[13]),
                                    self.add_to_location_list(13)]

        self.__buttons_list[13] = self.__create_single_button(root,
                                                              button_text_lst[13],
                                                              button14_actions)
        self.__buttons_list[13].place(x=136, y=370)

        button15_actions = lambda: [self.__add_click_to_word(button_text_lst[14]),
                                    self.__make_disabled(self.__buttons_list[14]),
                                    self.add_to_location_list(14)]

        self.__buttons_list[14] = self.__create_single_button(root,
                                                              button_text_lst[14],
                                                              button15_actions)
        self.__buttons_list[14].place(x=232, y=370)

        button16_actions = lambda: [self.__add_click_to_word(button_text_lst[15]),
                                    self.__make_disabled(self.__buttons_list[15]),
                                    self.add_to_location_list(15)]

        self.__buttons_list[15] = self.__create_single_button(root,
                                                              button_text_lst[15],
                                                              button16_actions)
        self.__buttons_list[15].place(x=328, y=370)

    def update_words_found_list(self, word):
        """
        This function updates the words found list
        :param word: String - word to be added to the words found list
        :return: None
        """
        if word not in self.words_found:
            self.words_found.append(word)
        else:
            tk.messagebox.showinfo("Already Chose", ALREADY_CHOSEN)

    def run(self):
        """
        This function runs the main loop
        :return: None
        """
        self.__main_window.mainloop()
