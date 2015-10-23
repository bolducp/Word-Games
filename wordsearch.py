import random
import math
import string


class Board(object):
    def __init__(self, num_letters):
        self.num_letters = num_letters
        self.letters = self.get_board_letters()
        self.row_size = int(math.sqrt(self.num_letters))

    def get_board_letters(self):
        board_letters = []
        vowels = ['a', 'e', 'i', 'o', 'u']
        consonants = ['b', 'c', 'c', 'd', 'd', 'f', 'g', 'h', 'h', 'j', 'l', 'm', 'n', 'n', 'p', 'r', 'r', 'r', 's', 's', 's', 't', 't', 't', 'v', 'w', 'x', 'y', 'z']

        num_vowels = self.num_letters / 4
        num_consonants = self.num_letters - num_vowels

        for num in xrange(num_vowels):
            board_letters.append(random.choice(vowels))
        for num in xrange(num_consonants):
            board_letters.append(random.choice(consonants))

        random.shuffle(board_letters)
        return board_letters

    def print_board(self):
        for index in xrange(self.num_letters):
            print self.letters[index] + " ",
            if (index + 1) % self.row_size == 0:
                print


class Player(object):
    def __init__(self, player_symbol, board):
        self.player_symbol = player_symbol
        self.board = board
        self.words = []

    def get_player_words(self):
        while True:
            word = raw_input("Enter a word. Enter 'done!' to end turn or 'print!' to reprint the board. ")
            if word == "done!":
                return self.words
            elif word == "print!":
                self.board.print_board()
            else:
                self.words.append(word)
        return self.words


class Game(object):
    def __init__(self, players, board):
        self.players = players
        self.board = board
        self.player_scores_dict = self.evaluate_player_words_into_score_dict()

    def evaluate_player_words_into_score_dict(self):
        player_scores_dict = {}
        for player in self.players:
            player_count = 0
            player_words = []
            for word in player.words:
                if word in self.get_valid_board_words() and word not in player_words:
                    player_count += 1
                    player_words.append(word)
            player_scores_dict[player.player_symbol] = player_count
        return player_scores_dict

    def print_outcome(self):
        print "\nGame Results:"
        self.print_all_possible_words()
        print

        for player in self.players:
            print player.player_symbol, "'s words:"
            for word in player.words:
                print word
            print
        for key, value in self.player_scores_dict.items():
            print key, "scored", value, "points"

    def print_all_possible_words(self):
        print "\nAll possible board words:"
        for word in self.get_valid_board_words():
            print word

    def get_word_list(self):
        with open('words.txt') as words_file:
            line = words_file.readline()
            wordlist = string.split(line)
        return wordlist

    def get_valid_board_words(self):
        valid_words = []
        word_list = self.get_word_list()
        for word in self.get_board_position_combinations():
            if word in word_list:
                valid_words.append(word)
        return valid_words

    def get_board_position_combinations(self):
        board_position_combinations = []
        for word in self.get_horizontal_combinations():
            board_position_combinations.append(word)
        for word in self.get_vertical_combinations():
            board_position_combinations.append(word)
        for word in self.get_diagonal_combinations():
            board_position_combinations.append(word)
        return board_position_combinations

    def get_horizontal_combinations(self):
        horizontal_combinations = []

        for index in xrange(len(self.board.letters)):
            forward_working_word = self.board.letters[index]
            backward_working_word = self.board.letters[index]
            line_end_index = index + (self.board.row_size - (index % self.board.row_size))
            line_backward_end_index = index - (index % self.board.row_size)

            for next_index in xrange(index + 1, line_end_index):
                forward_working_word += self.board.letters[next_index]
                horizontal_combinations.append(forward_working_word)

            for previous_index in xrange(index - 1, line_backward_end_index - 1, -1):
                if previous_index < 0:
                    continue
                backward_working_word += self.board.letters[previous_index]
                horizontal_combinations.append(backward_working_word)
        return horizontal_combinations

    def get_vertical_combinations(self):
        vertical_combinations = []

        for index in xrange(len(self.board.letters)):
            downward_working_word = self.board.letters[index]
            upward_working_word = self.board.letters[index]

            line_end_index = self.board.num_letters - (self.board.row_size - (index % self.board.row_size))
            line_backward_end_index = index % self.board.row_size

            for next_index in xrange(index + self.board.row_size, line_end_index + self.board.row_size, self.board.row_size):
                downward_working_word += self.board.letters[next_index]
                vertical_combinations.append(downward_working_word)

            for previous_index in xrange(index - self.board.row_size, line_backward_end_index - self.board.row_size, -self.board.row_size):
                upward_working_word += self.board.letters[previous_index]
                vertical_combinations.append(upward_working_word)
        return vertical_combinations

    def get_diagonal_combinations(self):
        diagonal_combinations = []
        for word in self.get_right_diagonal_combinations():
            diagonal_combinations.append(word)
        for word in self.get_left_diagonal_combinations():
            diagonal_combinations.append(word)
        return diagonal_combinations

    def get_right_diagonal_combinations(self):
        right_diagonal_combinations = []

        for index in xrange(len(self.board.letters)):
            downward_working_word = self.board.letters[index]
            upward_working_word = self.board.letters[index]

            line_end_index = index
            while line_end_index == 0 or (line_end_index % self.board.row_size != 0 and line_end_index + (self.board.row_size + 1) <= self.board.num_letters -1):
                line_end_index += self.board.row_size + 1

            for next_index in xrange(index + self.board.row_size + 1, line_end_index + 1, self.board.row_size + 1):
                downward_working_word += self.board.letters[next_index]
                right_diagonal_combinations.append(downward_working_word)

            line_backward_end_index = index
            while line_backward_end_index == 99 or (line_backward_end_index % self.board.row_size != 0 and line_backward_end_index - (self.board.row_size + 1) >= 0):
                line_backward_end_index -= self.board.row_size + 1

            for previous_index in xrange(index - (self.board.row_size + 1), line_backward_end_index - 1, -(self.board.row_size + 1)):
                upward_working_word += self.board.letters[previous_index]
                right_diagonal_combinations.append(upward_working_word)
        return right_diagonal_combinations

    def get_left_diagonal_combinations(self):
        left_diagonal_combinations = []

        for index in xrange(len(self.board.letters)):
            downward_working_word = self.board.letters[index]
            upward_working_word = self.board.letters[index]

            line_end_index = index
            while line_end_index % self.board.row_size != 0 and line_end_index + (self.board.row_size - 1) <= self.board.num_letters -1:
                line_end_index += self.board.row_size - 1

            for next_index in xrange(index + self.board.row_size - 1, line_end_index + 1, self.board.row_size - 1):
                downward_working_word += self.board.letters[next_index]
                left_diagonal_combinations.append(downward_working_word)

            line_backward_end_index = index
            while (line_backward_end_index + 1) % self.board.row_size != 0 and line_backward_end_index - (self.board.row_size) >= 0:
                line_backward_end_index -= self.board.row_size - 1

            for previous_index in xrange(index - (self.board.row_size - 1), line_backward_end_index -1, -(self.board.row_size - 1)):
                upward_working_word += self.board.letters[previous_index]
                left_diagonal_combinations.append(upward_working_word)
        return left_diagonal_combinations


def main():
    board = Board(100)

    print "Welcome to the Crossword Puzzle Game"
    num_players = int(raw_input("Please enter the number of players: "))

    players = []
    for player in range(1, num_players + 1):
        player_symbol = raw_input("Please enter player %d name: " % player)
        player = Player(player_symbol, board)
        players.append(player)

    for player in players:
        player.board.print_board()
        print "Player ", player.player_symbol, "'s turn:"
        player.get_player_words()
        print

    game = Game(players, board)
    game.print_outcome()


if __name__ == "__main__":
    main()
