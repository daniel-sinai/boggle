###################################################################
# FILE: boggle_utils.py
# WRITER: Daniel Sinai
# DESCRIPTION: This program implements various logical functions
#              for the boggle game
###################################################################
def create_cells(board):
    """
    This function creates cells from a given board
    :param board: List of lists - board
    :return: List of tuples - board's cells
    """
    return [(i, j) for i in range(len(board[0])) for j in range(len(board[0]))]


def valid_cells(board, row_location, col_location, size):
    """
    This function finds the valid cells that can be advanced on the board
    :param board: List of lists - game board
    :param row_location: Integer - row location
    :param col_location: Integer - column location
    :param size: Integer - radius
    :return: List of tuples - valid cells
    """
    result = []
    board_cells = create_cells(board)
    for i in range(row_location - size, row_location + size + 1):
        for j in range(col_location - size, col_location + size + 1):
            if (i, j) in board_cells and (i, j) != \
                    (row_location, col_location):
                result.append((i, j))
    return result


def is_valid_path(board, path, words):
    """
    This function checks if a given path represents a valid word in the
    dictionary
    :param board: List of lists - board
    :param path: List of tuples - path
    :param words: List of string of words
    :return: String - the word if the path is valid, else None
    """
    if path and len(path) == len(set(path)):
        temp_location = path[0]
        if temp_location in create_cells(board):
            my_word = board[temp_location[0]][temp_location[1]]
            for location in path[1:]:
                current_valid_cells = valid_cells(board, temp_location[0],
                                                  temp_location[1], 1)
                if location not in current_valid_cells:
                    return
                temp_location = location
                my_word += board[temp_location[0]][temp_location[1]]
            if my_word in words:
                return my_word
    return


def find_length_n_paths(n, board, words):
    """
    This function returns a list of all n-length paths representing words
    from the dictionary
    :param n: Integer number - path's length
    :param board: List of lists - board
    :param words: List of strings - word from the dictionary
    :return: List of lists of tuples - paths
    """
    final_list = []
    for cell in create_cells(board):
        find_length_n_paths_helper(n, board, words, final_list, [cell], cell,
                                   1, "paths")
    return final_list


def find_length_n_paths_helper(n, board, words, final_list, path_list, cell,
                               counter, flag):
    """
    This function is a help function for find_length_n_paths
    :param n: Integer number
    :param board: List of lists - board
    :param words: List of strings - words from the dictionary
    :param final_list: List
    :param path_list: List of tuples - path
    :param cell: Tuple - single cell
    :param counter: Integer number represents a counter
    :param flag: Boolean
    :return: None
    """
    if counter > n:
        return
    if counter == n:
        if is_valid_path(board, path_list, words):
            final_list.append(path_list)
        return

    next_valid_steps = valid_cells(board, cell[0], cell[1], 1)
    for step in next_valid_steps:
        if step not in path_list:
            if flag == "paths":
                find_length_n_paths_helper(n, board, words, final_list,
                                           path_list + [step], step,
                                           counter + 1, flag)
            elif flag == "words":
                find_length_n_paths_helper(n, board, words, final_list,
                                           path_list + [step], step, counter +
                                           len(board[step[0]][step[1]]), flag)


def find_length_n_words(n, board, words):
    """
    This function returns a list of all paths representing n-length words
    from the dictionary
    :param n: Integer number - word's length
    :param board: List of lists - board
    :param words: List of strings - words from the dictionary
    :return: List of lists of tuples - paths
    """
    final_list = []
    for cell in create_cells(board):
        find_length_n_paths_helper(n, board, words, final_list, [cell], cell,
                                   len(board[cell[0]][cell[1]]), "words")
    return final_list


def max_score_paths(board, words):
    """
    This function returns a list of paths that provide the maximum game score
     for the board and word collection provided.
    :param board: List of lists - board
    :param words: List of strings - words from the dictionary
    :return:
    """
    words_dict = {}
    min_word_len = len(min(words, key=len))
    max_word_len = len(max(words, key=len))
    for n in range(min_word_len, max_word_len + 1):
        current_n_words_list = find_length_n_words(n, board, words)
        for path in current_n_words_list:
            current_word = is_valid_path(board, path, words)
            if current_word not in words_dict:
                words_dict[current_word] = path
            elif len(words_dict[current_word]) < len(path):
                words_dict[current_word] = path
    return list(words_dict.values())
