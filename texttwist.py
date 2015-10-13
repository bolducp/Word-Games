import string
import random


def get_word_list(filename):
    with open(filename) as file:
        line = file.readline()
    wordlist = string.split(line)
    return wordlist


def get_game_word(wordlist):
    game_word = random.choice(wordlist)
    if len(game_word) <= 7:
        game_word = random.choice(wordlist)
    return game_word


def scramble_letters(word):
    new_word = ''
    for num in range(len(word)):
        index = random.choice(range(len(word)))
        letter = word[index]
        new_word += letter
        word = word[:index] + word[index + 1:]
    return new_word


def get_user_words(word):
    words = []
    while True:
        user_word = raw_input("Type 'done!' to end the game. Type 'scramble!' to scramble the letters. Type 'print!' to print the letters again.\nEnter a word: ")

        if user_word == "done!":
            print "Game ended.\n"
            return words
        elif user_word == "print!":
            print word
        elif user_word == "scramble!":
            print scramble_letters(word)
        else:
            words.append(user_word)


def guess_is_valid_word(guess, wordlist):
    return guess in wordlist


def guess_is_in_letters(guess, word):
    for char in guess:
        index = word.find(char)
        if index == -1:
            return False
        else:
            word = word[:index] + word[index + 1:]
    return True


def get_valid_user_words(user_words, word, word_list):
    valid_words = []
    for guess in user_words:
        if guess_is_in_letters(guess, word) and guess_is_valid_word(guess, word_list):
            valid_words.append(guess)
    return valid_words


def calculate_score(valid_words):
    total_score = 0
    print "The scores for your valid words: \n"
    for word in valid_words:
        if len(word) <= 1:
            word_score = 0
        else:
            word_score = len(word)
        total_score += word_score
        print word, ":", word_score
    print "\n" + "Game total score: %d" % total_score


def main():
    print "List all the words made from these letters that you can find:"
    word_list = get_word_list("words.txt")
    game_word = scramble_letters(get_game_word(word_list))

    print game_word, "\n"

    user_words = get_user_words(game_word)
    valid_words = get_valid_user_words(user_words, game_word, word_list)
    calculate_score(valid_words)


if __name__ == "__main__":
    main()