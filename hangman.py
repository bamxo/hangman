# assignment: programming assignment 1
# author: Landon Nguyen
# date: 1/18/2023
# file: hangman.py is a program that imitates the game Hangman. The user will have to guess a word, letter by letter, until they've run out of failed attempts
# input: The first input is a file cd "dictionary.txt" which is a text document filled with words that will be converted into a sorted dictionary. The other input is the user being first prompted to input their preferred word size and amount of lives and if they choose an invalid input, a random size will be chosen and the default lives will be chosen. Then the user will be prompted to input a single letter at a time to guess the unknown word. If an invalid letter is inputted, then the user will be asked to input another letter. Whether the user guesses the word write or runs out of lives the game will end, and the user will be prompted if they would like to play again.
# output: The output of the program greets the user to the game: Hangman, then prompts the user to input their preferred word size and amount of lives. Then the program will output the amount of lives the user inputted and the word size. If the word size input is invalid, then the program will output that the word size will be set to a random number. And if the lives input is invalid, then the program will output the default amount of lives. The program will then output the main game screen where the valid letters chosen will be displayed, underscores the represent the hidden word, along with the lives represented by a number and X's and O's. As the user is prompted to input letters, the program will output if the letter has already been chosen, if the input is invalid, if the guess is incorrect, or if the guess is correct. If the guess is incorrect, the program will output that a life has been removed. Whether the user guesses the word correctly or loses all of their lives, the program will output that the game has ended and will ask if the user if they would like to start a new game.

from random import choice, random, randint

dictionary_file = "dictionary.txt"   # make a dictionary.txt in the same folder where hangman.py is located

# write all your functions here
def print_playUI (chosenLetters, hiddenWord, lives, exo) :
    print("Letters chosen:", end=" ")
    for i in chosenLetters:
        if i == chosenLetters[len(chosenLetters)-1]:
            print(i.upper(), end="")
        else:
            print(i.upper(), end=", ")
    print()
    for i in hiddenWord:
        print(i, end=" ")
    print(f"lives: {lives} {exo}")

# make a dictionary from a dictionary file ('dictionary.txt', see above)
# dictionary keys are word sizes (1, 2, 3, 4, …, 12), and values are lists of words
# for example, dictionary = { 2 : ['Ms', 'ad'], 3 : ['cat', 'dog', 'sun'] }
# if a word has the size more than 12 letters, put it into the list with the key equal to 12

def import_dictionary (filename) :
    dictionary = {}
    max_size = 12
    with open(filename, "r") as fh:
        for line in fh:
            word = line[:-1].strip()
            size = len(word)
            if size in dictionary.keys():
                dictionary[size].append(word)
            elif max_size in dictionary.keys():
                if size >= max_size:
                    dictionary[max_size].append(word)
            else:
                dictionary[size] = [word]
    
    keys = list(dictionary.keys())
    keys.sort()
    sorted_dictionary = {i: dictionary[i] for i in keys}
    return sorted_dictionary

# print the dictionary (use only for debugging)
def print_dictionary (dictionary) :
    max_size = 12
    print(dictionary)

# get options size and lives from the user, use try-except statements for wrong input
def get_game_options () :
    try:
        size = int(input("Please choose a size of a word to be guessed [3 - 12, default any size]: "))
        assert (int(size) == size) and (size >= 3 and size <= 12)
        print(f"\nThe word size is set to {size}.")
    except:
        size = randint(3, 12)
        print("\nA dictionary word of any size will be chosen.")

    try:
        lives = int(input("Please choose a number of lives [1 - 10, default 5]: "))
        assert (int(lives) == lives) and (lives >= 1 and lives <= 10)
        print(f"\nYou have {lives} lives.")
    except:
        lives = 5
        print("\nYou have 5 lives.")

    return size, lives


# MAIN

if __name__ == '__main__' :

    # make a dictionary from a dictionary file
    dictionary = import_dictionary(dictionary_file)

    # print the dictionary (use only for debugging)
    #print_dictionary(dictionary)    # remove after debugging the dictionary function import_dictionary
    
    # print a game introduction
    print("Welcome to the Hangman Game!")

    # START MAIN LOOP (OUTER PROGRAM LOOP)
    while True:
    # set up game options (the word size and number of lives)
        size, lives = get_game_options()

    # select a word from a dictionary (according to the game options)
    # use choice() function that selects an item from a list randomly, for example:
    # mylist = ['apple', 'banana', 'orange', 'strawberry']
    # word = choice(mylist)
        word = choice(dictionary[size]).lower()
        letterCount = set(word)
        livesLost = 0
        foundLetters = []
        chosenLetters = []
        hiddenWord = []
        for i in range(0,size):
            if word[i] == "-":
                foundLetters.append("-")
                hiddenWord.append("- ")
            else:
                hiddenWord.append("__ ")
        exo = ""
        for i in range(0,lives):
            exo += "O"

        # START GAME LOOP   (INNER PROGRAM LOOP)
        while True:
            
        # format and print the game interface:
        # Letters chosen: E, S, P                list of chosen letters
        # __ P P __ E    lives: 4   XOOOO        hidden word and lives
            print_playUI(chosenLetters, hiddenWord, lives, exo)

        # ask the user to guess a letter
            while True:
                try:
                    while True:
                        try:
                            letter = str(input("\nPlease choose a new letter > "))
                            assert len(letter) == 1
                            assert letter.isnumeric() == False
                            assert letter != ";"
                            assert letter != "-"
                            break
                        except:
                            pass
                    assert letter not in chosenLetters
                    break
                except:
                    print("\nYou have already chosen this letter.")

        # update the list of chosen letters
            chosenLetters.append(letter)

        # if the letter is correct update the hidden word,
            if letter in word:
                hiddenWord = []
                foundLetters.append(letter)
                for i in range(0, size):
                    if word[i] in foundLetters:
                        hiddenWord.append(word[i].upper() + "  ")
                    else:
                        hiddenWord.append("__  ")
                print("\nYou guessed right!")

        # else update the number of lives
            else:
                exo = ""
                lives -= 1
                livesLost += 1
                for i in range(0, livesLost):
                    exo += "X"
                for i in range(0, lives):
                    exo += "O"
                print("\nYou guessed wrong, you lost one life.")

        # and print interactive messages      
        
        # END GAME LOOP   (INNER PROGRAM LOOP)

        # check if the user guesses the word correctly or lost all lives,
        # if yes finish the game
            if len(letterCount) == len(foundLetters):
                print_playUI(chosenLetters, hiddenWord, lives, exo)
                print(f"Congratulations!!! You won! The word is {word.upper()}!")
                break
            if lives == 0:
                print_playUI(chosenLetters, hiddenWord, lives, exo)
                print(f"You lost! The word is {word.upper()}!")
                break

    # END MAIN LOOP (OUTER PROGRAM LOOP)
        replay = str(input("Would you like to play again [Y/N]? "))
        print()
        if replay == 'Y' or replay == 'y':
            pass
        else:
            print("Goodbye!")
            break

    # ask if the user wants to continue playing, 
    # if yes start a new game, otherwise terminate the program
