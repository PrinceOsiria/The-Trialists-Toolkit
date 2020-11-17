########################################################################################################################
# Documentation: Project 108 - Module Branch
# This is an altered version of Project 108, intended for use as a module.
# Coded by Tyler Pryjda
########################################################################################################################


############################################################
# Imports
import os
from itertools import permutations
# Selects Current Directory as Filesystem
moduleFilesystem = os.path.dirname(os.path.abspath(__file__))
os.chdir(moduleFilesystem)

from pathlib import Path
rootFilesystem = str(Path(__file__).parent.parent)
############################################################


############################################################
# Custom Alphabet Generator
# *Returns alphabet as a list
def create_alphabet(AlphabetKey):
    # initializes variables for alphabet key cleaner
    i = 0
    StrippedAlphabetKey = ""
    Alphabet = list("abcdefghijklmnopqrstuvwxyz")
    AlphabetKey = clean_text(AlphabetKey, Alphabet)

    # cleans alphabet key
    while i < len(AlphabetKey):
        if AlphabetKey[i] not in StrippedAlphabetKey:
            StrippedAlphabetKey = StrippedAlphabetKey + AlphabetKey[i]
        i = i + 1

    # initializes variables for alphabet generator
    AlphabetKey = list(StrippedAlphabetKey)

    # Cleans standard alphabet
    i = 0
    while i < len(AlphabetKey):
        x = (ord(AlphabetKey[i]) - 97)
        Alphabet[x] = " "
        i = i + 1

    # creates alphabet and cleans for export
    Alphabet = "".join(Alphabet)
    AlphabetKey = "".join(AlphabetKey)
    Alphabet = AlphabetKey + Alphabet
    Alphabet = Alphabet.replace(" ", "")
    Alphabet = list(Alphabet)

    # Returns alphabet as a list
    return (Alphabet)


############################################################


############################################################
# Text standardization
# *Returns cleaned text in lowercase string by checking to see if each char exists in a given alphabet
def clean_text(DirtyText, Alphabet):
    # initializes text cleaner
    CleanText = ""
    DirtyText = list(DirtyText.lower())

    # cleans text
    x = 0
    while x < len(DirtyText):
        if DirtyText[x] in Alphabet:
            CleanText = CleanText + DirtyText[x]
        elif DirtyText[x] == "~":  # Used to clean keys without losing layers
            CleanText = CleanText + DirtyText[x]
        else:
            pass
        x = x + 1

    # returns cleaned text string
    return "".join(CleanText)


############################################################


############################################################
# Hels Labyrinth Brute Force Attacker
# *Generates Output File
# *Input = Raw Strings
def brute_hels(Alphabet, Keys, CipherText):

    # Initializes Variables
    Keys = clean_text(Keys.replace(" ", "~"), Alphabet)
    Keys = ("".join(Keys)).split("~")
    CipherText = clean_text(CipherText, Alphabet)

    Combos = []
    file = open(rootFilesystem + "\Results\BruteResults.txt", "w+")

    # Shuffles through combinations of keys
    x = 1
    while x <= len(Keys):
        for i in permutations(Keys, x):
            tmp = " ".join(list(i))
            foo = decode_hels(Alphabet, tmp, CipherText)
            output = "\n\n" +"Alphabet: " + Alphabet + "\n" + "Passphrases: " + str(tmp) + "\n" + "Result: " + str(foo)
            file.write(output)
            print(output)
        x = x + 1
    file.close()


############################################################


############################################################
# Hels Labyrinth Decoder
# *Returns lowercase cleartext
def decode_hels(Alphabet, Keys, CipherText):

    # Initializes Variables
    exportKeys = Keys
    Alphabet = Alphabet.split()
    Keys = clean_text(Keys.replace(" ", "~"), Alphabet)
    Keys = Keys.split("~")
    Keys.reverse()
    CipherText = clean_text(CipherText, Alphabet)
    file = open(rootFilesystem + "\Results\DecodeResults.txt", "w+")

    # Cycles through each key
    x = 0
    while x < len(Keys):

        # Initializes Variables
        CipherText = list(CipherText)  # splits ciphertext into letters
        Keys[x] = list(Keys[x])  # splits key into letters
        NumberKey = []
        NumberText = []

        # Assigns each letter in the key a number (Based on alphabet given)
        i = 0
        while i < len(Keys[x]):
            tmp = Keys[x][i]
            foo = Alphabet.index(tmp)
            NumberKey.append(foo)
            i = i + 1

        # Assigns each letter in the ciphertext a number (Based on alphabet given)
        i = 0
        while i < len(CipherText):
            tmp = CipherText[i]
            foo = Alphabet.index(tmp)
            NumberText.append(foo)
            i = i + 1

        # Initializes Variables
        Message = []

        # If the key is longer than the ciphertext...
        if len(NumberKey) >= len(NumberText):

            # Generates "Masterkey"
            i = 0
            while i < len(NumberText):
                tmp = NumberText[i]
                foo = NumberKey[i]
                bar = tmp - foo

                NumberKey.append(bar)

                i = i + 1

            # Lines up numbers with alphabet
            i = 0
            while i < len(NumberKey):
                if NumberKey[i] < 0:
                    NumberKey[i] = NumberKey[i] + 26
                else:
                    i = i + 1

            # Uses "Masterkey"
            i = 0
            while i < len(NumberText):
                tmp = NumberText[i]
                foo = NumberKey[i]
                bar = tmp - foo
                Message.append(bar)
                i = i + 1

            # Lines up numbers with alphabet
            i = 0
            while i < len(Message):
                if Message[i] < 0:
                    Message[i] = Message[i] + 26
                else:
                    i = i + 1

            # Converts numbers to letters
            i = 0
            while i < len(Message):
                tmp = Alphabet[Message[i]]
                Message[i] = tmp
                i = i + 1
            Message = "".join(Message)

        # If the key is shorter than the ciphertext...
        elif len(NumberKey) < len(NumberText):
            # Initializes Variable
            Difference = (len(NumberText) - len(NumberKey))

            # Generates "Masterkey"
            i = 0
            while i < Difference:
                tmp = NumberText[i]
                foo = NumberKey[i]
                bar = tmp - foo
                NumberKey.append(bar)

                i = i + 1

            # Lines up numbers with alphabet
            i = 0
            while i < len(NumberKey):
                if NumberKey[i] < 0:
                    NumberKey[i] = (NumberKey[i] + 26)
                    i = i + 1
                elif NumberKey[i] > 25:
                    NumberKey[i] = NumberKey[i] - 26
                else:
                    i = i + 1

            # Uses Masterkey
            i = 0
            while i < len(NumberKey):
                tmp = NumberKey[i]
                foo = NumberText[i]
                bar = foo - tmp

                Message.append(bar)

                i = i + 1

            # Lines up numbers with alphabet
            i = 0
            while i < len(Message):
                if Message[i] < 0:
                    Message[i] = (Message[i] + 26)
                    i = i + 1
                elif Message[i] > 25:
                    Message[i] = Message[i] - 26
                else:
                    i = i + 1

            # Converts numbers to letters
            i = 0
            while i < len(NumberKey):
                tmp = Alphabet[Message[i]]
                Message[i] = tmp
                i = i + 1

            # Converts message from a list of letters to a string
            Message = "".join(Message)

        # Initializes Variables
        NumberText = []
        CipherText = Message

        x = x + 1
        # Loops through next key if applicable

    #Exports Results
    file.write("\n\nAlphabet:" + ' '.join([str(elem) for elem in Alphabet[:]]) + "\nPassphrases: " + exportKeys.replace("~", " ") + "\nCipherText: " + CipherText)
    file.close()
    # Returns cleartext as a lowercase string
    return CipherText


############################################################


############################################################
# Hels Labyrinth Encoder
# *Generates Output File
# *Returns Clean String
# *Input = Raw Strings
def encode_hels(Alphabet, Keys, CipherText):

    # Initializes Variables
    exportKeys = Keys
    Alphabet = Alphabet.split()
    Keys = clean_text(Keys.replace(" ", "~"), Alphabet)
    Keys = Keys.split("~")
    CipherText = clean_text(CipherText, Alphabet)
    file = open(rootFilesystem + "\Results\EncodeResults.txt", "w+")

    # Debug Output
    #print("\n\nAlphabet: ", Alphabet, "\nKeys:", Keys, "\nCipherText: ", CipherText)

    # Loops through keys
    x = 0
    while x < len(Keys):
        # Initializes Variables
        CipherText = list(CipherText)
        Keys[x] = list(Keys[x])
        NumberKey = []
        NumberText = []

        # Assigns each letter in each key to numbers based on given alphabet
        i = 0
        while i < len(Keys[x]):
            tmp = Keys[x][i]
            foo = Alphabet.index(tmp)
            NumberKey.append(foo)
            i = i + 1

        # Assigns each letter in the cleartext to numbers based on given alphabet
        i = 0
        while i < len(CipherText):
            tmp = CipherText[i]
            foo = Alphabet.index(tmp)
            NumberText.append(foo)
            i = i + 1

        # Initializes Variables
        Message = []

        if len(NumberKey) >= len(NumberText):

            i = 0
            while i < len(NumberText):
                tmp = NumberText[i]
                foo = NumberKey[i]

                Message.append(tmp + foo)

                i = i + 1
            i = 0
            while i < len(Message):
                if Message[i] > 25:
                    Message[i] = Message[i] - 26
                    i = i + 1
                else:
                    i = i + 1

            i = 0
            while i < len(Message):
                tmp = Alphabet[Message[i]]
                Message[i] = tmp
                i = i + 1
            Message = "".join(Message)

        elif len(NumberKey) < len(NumberText):
            Difference = (len(NumberText) - len(NumberKey))

            i = 0
            while i < Difference:
                tmp = NumberText[i]
                NumberKey.append(tmp)

                i = i + 1

            i = 0
            while i < len(NumberKey):
                tmp = NumberText[i]
                foo = NumberKey[i]
                bar = foo + tmp
                Message.append(bar)
                i = i + 1

            i = 0
            while i < len(NumberKey):
                if Message[i] > 25:
                    Message[i] = (Message[i] - 26)
                    i = i + 1
                else:
                    i = i + 1

            i = 0
            while i < len(NumberKey):
                tmp = Alphabet[Message[i]]
                Message[i] = tmp
                i = i + 1

            Message = "".join(Message)

        NumberText = []
        CipherText = Message

        x = x + 1

    # Deubug Output
    #print("\n\nAlphabet: ", Alphabet, "\nKeys:", Keys, "\nCipherText: ", CipherText)


    file.write( "\n\nAlphabet:" + ' '.join([str(elem) for elem in Alphabet[:]]) + "\nPassphrases: " + exportKeys.replace("~", " ") + "\nCipherText: " + CipherText)
    file.close()
    return CipherText


############################################################
# Permutation Analysis
# *Returns string with number of permutations
def analyze_permutations(Keys):

    # Initializes Variables
    Combos = []
    Keys = Keys.lower()
    Alphabet = "abcdefghijklmnopqrstuvwxyz"
    Keys = clean_text(Keys.replace(" ", "~"), Alphabet)
    Keys = Keys.replace("~", " ")
    Keys = Keys.split()

    # Generates list of key combos
    x = 1
    while x <= len(Keys):
        for i in permutations(Keys, x):
            tmp = " ".join(list(i))
            Combos.append(tmp)
        x = x + 1

    return str(len(Combos)) + "Permutations"


############################################################
