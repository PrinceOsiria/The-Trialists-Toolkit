#######################################################################
# Documentation: The Trialist's Toolkit
#######################################################################
# The Trialist's Toolkit is a small program containing:
# Project 107 - Archiving - Archiving Software
# Project 108 - Cryptography - Cryptography Software
#####
#####Both of these projects have been merged and updated for the simplest
#####user experience possible, while also allowing for the completion of
#####complex tasks pertaining to mushroom.film
#####
# Coded by Tyler Pryjda
#######################################################################


#######################################################################
#####Imports
#######################################################################
# os allows for access to files and pathlib assists with subdirectory navigation
import os
from pathlib import Path
# tkinter - Allows the creation of a GUI
from tkinter import *
from tkinter import ttk
# Imports Project 108 - Module Edition
from Modules import p108_module as p108
# Imports CSV Machine - Module Edition
from Modules import CSV_Machine
# Imports Filesystem Machine - Module Edition
from Modules import Filesystem_Machine
# Subprocess opens output files using notepad.exe on windows machines and csv accesses local data on csv files
import subprocess, csv
from functools import partial
import requests
import tempfile

#######################################################################
#####Variables
#######################################################################
# Program Variables
# Selects Current Directory as Filesystem
rootFilesystem = str(os.path.dirname(os.path.abspath(__file__)))
os.chdir(rootFilesystem)
# p108 Variables
Alphabet = p108.create_alphabet("")

# Window Options
root = Tk()
root.title("The Trialist's Toolkit")
root.resizable(False, False)
# root.iconbitmap("path to image") - Icon File
root.geometry("400x500")

#######################################################################
#####Functions
#######################################################################  

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def DisplayPage(*args):
    page = selectedProgram.get()

    if page == "Project 108 - Cryptography":
        p107Frame.forget()
        p108Frame.pack(fill=BOTH, expand=True)
    elif page == "Project 107 - Archiving":
        p108Frame.forget()
        p107Frame.pack(fill=BOTH, expand=True)

def CleanCSV(*args):
    CSV_Machine.clean_csv(rawCSVSelection.get())

def GenerateFilesystem(*args):
    filename = cleanCSVSelection.get()
    year = filename[:4]
    pathtofiledir = rootFilesystem + "/Archives/Spreadsheets/Clean"
    pathtoarchive = rootFilesystem + "/Archives/Filesystem"
    print((year, pathtofiledir, filename, pathtoarchive))
    Filesystem_Machine.generate_filesystem(year, pathtofiledir, filename, pathtoarchive)

def Generate_p108Bruter():
    p108Bruter_ciphertextFrame = Frame(p108Bruter)

    p108Bruter_ciphertextHeader = Label(p108Bruter_ciphertextFrame, text="Ciphertext:")
    p108Bruter_ciphertextHeader.pack(anchor=W, pady=10)

    p108Bruter_ciphertextEntry = Entry(p108Bruter_ciphertextFrame, width=45)
    p108Bruter_ciphertextEntry.pack(side=LEFT)

    p108Bruter_ciphertext = Label(p108Bruter, text="Please Enter Your Ciphertext & Press Confirm.")

    def p108Bruter_ciphertextConfirmation_clicked():
        p108Bruter_ciphertext.config(text=p108.clean_text(p108Bruter_ciphertextEntry.get().replace("~", ""), Alphabet))

    p108Bruter_ciphertextConfirmation = Button(p108Bruter_ciphertextFrame, width=15, text="Confirm Ciphertext", command=p108Bruter_ciphertextConfirmation_clicked)
    p108Bruter_ciphertextConfirmation.pack(side=RIGHT)

    p108Bruter_alphabetKeyFrame = Frame(p108Bruter)

    p108Bruter_alphabetKeyHeader = Label(p108Bruter_alphabetKeyFrame, text="Alphabet Key:")
    p108Bruter_alphabetKeyHeader.pack(anchor=W, pady=10)

    p108Bruter_alphabetKeyEntry = Entry(p108Bruter_alphabetKeyFrame, width=45)
    p108Bruter_alphabetKeyEntry.pack(side=LEFT)

    p108Bruter_alphabet = Label(p108Bruter, text=Alphabet)

    def p108Bruter_generateAlphabetButton_clicked():
        p108Bruter_alphabet.config(text=p108.create_alphabet(p108Bruter_alphabetKeyEntry.get().replace("~", "")))

    p108Bruter_generateAlphabetButton = Button(p108Bruter_alphabetKeyFrame, width=15, text="Generate Alphabet", command=p108Bruter_generateAlphabetButton_clicked)
    p108Bruter_generateAlphabetButton.pack(side=RIGHT)

    p108Bruter_passphraseFrame = Frame(p108Bruter)

    p108Bruter_passphraseHeader = Label(p108Bruter_passphraseFrame, text="Passphrases: (Separated With Spaces or ~)")
    p108Bruter_passphraseHeader.pack(anchor=W, pady=10)

    p108Bruter_passphraseEntry = Entry(p108Bruter_passphraseFrame, width=45)
    p108Bruter_passphraseEntry.pack(side=LEFT)

    p108Bruter_passphrases = Label(p108Bruter, text="Please Enter Your Passphrases & Press Confirm.")

    def pp108Bruter_passphraseConfirmation_clicked():
        p108Bruter_passphrases.config(text=p108.clean_text(p108Bruter_passphraseEntry.get().replace(" ", "~"), Alphabet))

    p108Bruter_passphraseConfirmation = Button(p108Bruter_passphraseFrame, width=15, text="Confirm Passphrases", command=pp108Bruter_passphraseConfirmation_clicked)
    p108Bruter_passphraseConfirmation.pack(side=RIGHT)

    p108Bruter_bruteButtonFrame = Frame(p108Bruter)

    def p108Bruter_bruteButton_clicked():
        p108.brute_hels(p108Bruter_alphabet["text"], p108Bruter_passphrases["text"], p108Bruter_ciphertext["text"])
        subprocess.Popen(["notepad", rootFilesystem + "/Results/BruteResults.txt"])

    p108Bruter_bruteButton = Button(p108Bruter_bruteButtonFrame, width=50, text="BRUTE", command=p108Bruter_bruteButton_clicked)
    p108Bruter_bruteButton.pack(pady=25)

    p108Bruter_ciphertextFrame.pack()
    p108Bruter_ciphertext.pack(pady=10)
    p108Bruter_alphabetKeyFrame.pack()
    p108Bruter_alphabet.pack(pady=10)
    p108Bruter_passphraseFrame.pack()
    p108Bruter_passphrases.pack(pady=10)
    p108Bruter_bruteButtonFrame.pack()

def Generate_p108Encoder():
    p108Encoder_ciphertextFrame = Frame(p108Encoder)

    p108Encoder_ciphertextHeader = Label(p108Encoder_ciphertextFrame, text="Cleartext:")
    p108Encoder_ciphertextHeader.pack(anchor=W, pady=10)

    p108Encoder_ciphertextEntry = Entry(p108Encoder_ciphertextFrame, width=45)
    p108Encoder_ciphertextEntry.pack(side=LEFT)

    p108Encoder_cleartext = Label(p108Encoder, text="Please Enter Your Cleartext & Press Confirm.")

    def p108Encoder_cleartextConfirmation_clicked():
        p108Encoder_cleartext.config(text=p108.clean_text(p108Encoder_ciphertextEntry.get().replace("~", " "), Alphabet))

    p108Encoder_ciphertextConfirmation = Button(p108Encoder_ciphertextFrame, width=15, text="Confirm Cleartext", command=p108Encoder_cleartextConfirmation_clicked)
    p108Encoder_ciphertextConfirmation.pack(side=RIGHT)

    p108Encoder_alphabetKeyFrame = Frame(p108Encoder)

    p108Encoder_alphabetKeyHeader = Label(p108Encoder_alphabetKeyFrame, text="Alphabet Key:")
    p108Encoder_alphabetKeyHeader.pack(anchor=W, pady=10)

    p108Encoder_alphabetKeyEntry = Entry(p108Encoder_alphabetKeyFrame, width=45)
    p108Encoder_alphabetKeyEntry.pack(side=LEFT)

    p108Encoder_alphabet = Label(p108Encoder, text=Alphabet)

    def p108Encoder_generateAlphabetButton_clicked():
        p108Encoder_alphabet.config(text=p108.create_alphabet(p108Encoder_alphabetKeyEntry.get().replace("~", " ")))

    p108Encoder_generateAlphabetButton = Button(p108Encoder_alphabetKeyFrame, width=15, text="Generate Alphabet", command=p108Encoder_generateAlphabetButton_clicked)
    p108Encoder_generateAlphabetButton.pack(side=RIGHT)

    p108Encoder_passphraseFrame = Frame(p108Encoder)

    p108Encoder_passphraseHeader = Label(p108Encoder_passphraseFrame, text="Passphrases: (Separated With Spaces or ~)")
    p108Encoder_passphraseHeader.pack(anchor=W, pady=10)

    p108Encoder_passphraseEntry = Entry(p108Encoder_passphraseFrame, width=45)
    p108Encoder_passphraseEntry.pack(side=LEFT)

    p108Encoder_passphrases = Label(p108Encoder, text="Please Enter Your Passphrases & Press Confirm.")

    def p108Encoder_passphraseConfirmation_clicked():
        p108Encoder_passphrases.config(text=p108.clean_text(p108Encoder_passphraseEntry.get().replace(" ", "~"), Alphabet))

    p108Encoder_passphraseConfirmation = Button(p108Encoder_passphraseFrame, width=15, text="Confirm Passphrases", command=p108Encoder_passphraseConfirmation_clicked)
    p108Encoder_passphraseConfirmation.pack(side=RIGHT)

    p108Encoder_encodeButtonFrame = Frame(p108Encoder)

    def p108Encoder_encodeButton_clicked():
        p108.encode_hels(p108Encoder_alphabet["text"], p108Encoder_passphrases["text"], p108Encoder_cleartext["text"])
        subprocess.Popen(["notepad", rootFilesystem + "/Results/EncodeResults.txt"])

    p108Encoder_encodeButton = Button(p108Encoder_encodeButtonFrame, width=50, text="ENCODE", command=p108Encoder_encodeButton_clicked)
    p108Encoder_encodeButton.pack(pady=25)

    p108Encoder_ciphertextFrame.pack()
    p108Encoder_cleartext.pack(pady=10)
    p108Encoder_alphabetKeyFrame.pack()
    p108Encoder_alphabet.pack(pady=10)
    p108Encoder_passphraseFrame.pack()
    p108Encoder_passphrases.pack(pady=10)
    p108Encoder_encodeButtonFrame.pack()

def Generate_p108Decoder():
    p108Decoder_ciphertextFrame = Frame(p108Decoder)

    p108Decoder_ciphertextHeader = Label(p108Decoder_ciphertextFrame, text="Ciphertext")
    p108Decoder_ciphertextHeader.pack(anchor=W, pady=10)

    p108Decoder_ciphertextEntry = Entry(p108Decoder_ciphertextFrame, width=45)
    p108Decoder_ciphertextEntry.pack(side=LEFT)

    p108Decoder_ciphertext = Label(p108Decoder, text="Please Enter Your Ciphertext & Press Confirm.")

    def p108Decoder_ciphertextConfirmation_clicked():
        p108Decoder_ciphertext.config(text=p108.clean_text(p108Decoder_ciphertextEntry.get().replace("~", " "), Alphabet))

    p108Decoder_ciphertextConfirmation = Button(p108Decoder_ciphertextFrame, width=15, text="Confirm Ciphertext", command=p108Decoder_ciphertextConfirmation_clicked)
    p108Decoder_ciphertextConfirmation.pack(side=RIGHT)

    p108Decoder_alphabetKeyFrame = Frame(p108Decoder)

    p108Decoder_alphabetKeyHeader = Label(p108Decoder_alphabetKeyFrame, text="Alphabet Key:")
    p108Decoder_alphabetKeyHeader.pack(anchor=W, pady=10)

    p108Decoder_alphabetKeyEntry = Entry(p108Decoder_alphabetKeyFrame, width=45)
    p108Decoder_alphabetKeyEntry.pack(side=LEFT)

    p108Decoder_alphabet = Label(p108Decoder, text=Alphabet)

    def p108Decoder_generateAlphabetButton_clicked():
        p108Decoder_alphabet.config(text=p108.create_alphabet(p108Decoder_alphabetKeyEntry.get().replace("~", " ")))

    p108Decoder_generateAlphabetButton = Button(p108Decoder_alphabetKeyFrame, width=15, text="Generate Alphabet", command=p108Decoder_generateAlphabetButton_clicked)
    p108Decoder_generateAlphabetButton.pack(side=RIGHT)

    p108Decoder_passphraseFrame = Frame(p108Decoder)

    p108Decoder_passphraseHeader = Label(p108Decoder_passphraseFrame, text="Passphrases: (Separated With Spaces or ~)")
    p108Decoder_passphraseHeader.pack(anchor=W, pady=10)

    p108Decoder_passphraseEntry = Entry(p108Decoder_passphraseFrame, width=45)
    p108Decoder_passphraseEntry.pack(side=LEFT)

    p108Decoder_passphrases = Label(p108Decoder, text="Please Enter Your Passphrases & Press Confirm.")

    def p108Decoder_passphraseConfirmation_clicked():
        p108Decoder_passphrases.config(text=p108.clean_text(p108Decoder_passphraseEntry.get().replace(" ", "~"), Alphabet))

    p108Decoder_passphraseConfirmation = Button(p108Decoder_passphraseFrame, width=15, text="Confirm Passphrases", command=p108Decoder_passphraseConfirmation_clicked)
    p108Decoder_passphraseConfirmation.pack(side=RIGHT)

    p108Decoder_encodeButtonFrame = Frame(p108Decoder)

    def p108Decoder_decodeButton_clicked():
        p108.decode_hels(p108Decoder_alphabet["text"], p108Decoder_passphrases["text"], p108Decoder_ciphertext["text"])
        subprocess.Popen(["notepad", rootFilesystem + "/Results/DecodeResults.txt"])

    p108Decoder_encodeButton = Button(p108Decoder_encodeButtonFrame, width=50, text="DECODE", command=p108Decoder_decodeButton_clicked)
    p108Decoder_encodeButton.pack(pady=25)

    p108Decoder_ciphertextFrame.pack()
    p108Decoder_ciphertext.pack(pady=10)
    p108Decoder_alphabetKeyFrame.pack()
    p108Decoder_alphabet.pack(pady=10)
    p108Decoder_passphraseFrame.pack()
    p108Decoder_passphrases.pack(pady=10)
    p108Decoder_encodeButtonFrame.pack()

def goto_url(link):
    os.system("start /"/" " + link)

#######################################################################
#####Main
#######################################################################
#####Project 108 - Cryptography#####
# Frame Options
p108Frame = Frame(root, relief=SUNKEN, bd=1)

# p108Bruter
p108Bruter = Frame(root, relief=SUNKEN, bd=1)
Generate_p108Bruter()

# p108Encoder
p108Encoder = Frame(root, relief=SUNKEN, bd=1)
Generate_p108Encoder()

# p108Decoder
p108Decoder = Frame(root, relief=SUNKEN, bd=1)
Generate_p108Decoder()

# Notebook Options (P108 Functions)
p108Functions = ttk.Notebook(p108Frame)
p108Functions.add(p108Bruter, text="Hels Bruter")
p108Functions.add(p108Encoder, text="Hels Encoder")
p108Functions.add(p108Decoder, text="Hels Decoder")
p108Functions.pack(fill=BOTH, expand=True, pady=5)





#####Project 107 - Archiving#####
# Frame Options
p107Frame = Frame(root, relief=SUNKEN, bd=1)

# Archiving Tools
#Downloads the most recent version of rawCSVLinks.csv
update = "https://docs.google.com/spreadsheets/d/1AXzSbVALQ6QbEvqrzbj70vLLN84wa_v7ebhtCqEqUS0/export?format=csv&id=1AXzSbVALQ6QbEvqrzbj70vLLN84wa_v7ebhtCqEqUS0&gid=1877437768"
file = r"/Archives/Spreadsheets/rawCSVLinks.csv"
with requests.get(update) as r:
    with open(rootFilesystem + file, "wb") as f:
        for data in r.iter_content():
            f.write(data)
        f.close()

#Downloads latest raw spreadsheets
os.makedirs(rootFilesystem + "/Archives/Spreadsheets/Raw//", exist_ok=True)
file = r"/Archives/Spreadsheets/rawCSVLinks.csv"
with open(rootFilesystem + file) as f:
    data = csv.reader(f, delimiter=',', quotechar='|')
    for row in data:
        filename = row[0]
        updatelink = row[1]
        with requests.get(updatelink) as r:
            with open(rootFilesystem + "/Archives/Spreadsheets/Raw//" + filename, "wb") as y:
                for data in r.iter_content():
                    y.write(data)
                y.close()
f.close()

CSVMachine = Frame(root, relief=SUNKEN, bd=1)
CSVCleaner = Frame(CSVMachine, relief=RIDGE, bd=1)
CSVCleanerHeader = Label(CSVCleaner, text="CSV Cleaner", relief=GROOVE)
CSVCleanerHeader.pack(fill=X)
CSVCleanerSubtitle = Label(CSVCleaner, text="Select A File to Clean it:", anchor=NW)
CSVCleanerSubtitle.pack(side=LEFT)
rawCSVList = os.listdir(rootFilesystem + "/Archives/Spreadsheets/Raw")
rawCSVSelection = StringVar()
rawCSVMenu = OptionMenu(CSVCleaner, rawCSVSelection, *rawCSVList or ["N/A"])
rawCSVMenu.pack(side=RIGHT)
CSVCleaner.pack(fill=X)
FilesystemGenerator = Frame(CSVMachine, relief=RIDGE, bd=1)
FilesystemMachineHeader = Label(FilesystemGenerator, text="Filesystem Generator", relief=GROOVE)
FilesystemMachineHeader.pack(fill=X)
FilesystemMachineSubtitle = Label(FilesystemGenerator, text="Select A File Generate a Filesystem from it:", anchor=NW)
FilesystemMachineSubtitle.pack(side=LEFT)
cleanCSVList = os.listdir(rootFilesystem + "/Archives/Spreadsheets/Clean")
cleanCSVSelection = StringVar()
cleanCSVMenu = OptionMenu(FilesystemGenerator, cleanCSVSelection, *cleanCSVList or ["N/A"])
cleanCSVMenu.pack(side=RIGHT)
FilesystemGenerator.pack(fill=X)

# Timeline
p107links = ScrollableFrame(root)

#Downloads most recent version of p107links.csv
update = "https://docs.google.com/spreadsheets/d/1pbeSknaHltSXTcGcxGWI0xVWU2nBRP7EONp7yg1kFEY/export?format=csv&id=1pbeSknaHltSXTcGcxGWI0xVWU2nBRP7EONp7yg1kFEY&gid=763577821"
file = "/Archives/Spreadsheets/p107Links.csv"
with requests.get(update) as r:
    with open(rootFilesystem + file, "wb") as f:
        for data in r.iter_content():
            f.write(data)
        f.close()

#Generates Timeline
with open(rootFilesystem + "/Archives/Spreadsheets/p107Links.csv") as p107LinksCSV:
    data = csv.reader(p107LinksCSV, delimiter=',', quotechar='|')
    years = []
    months = []

    for row in data:
        list = row[0].split(",")

        alpha = list[1]
        bravo = list[2]

        date = list[0].split("/")
        links = [alpha, bravo]

        #print(links)

        for items in date:
            if len(items) == 4: #if year
                if items not in years: #if new year
                    tmp = Frame(p107links.scrollable_frame, name="yearframe"+date[0])#UPDATE TO ALLOW SCROLLING
                    tmp.pack()
                    years.append(items)
            elif len(items) == 2:#if month
                if items not in months:

                    xyz = Frame(tmp)

                    Label(xyz, text="Year: " + date[0] + "/t|/t" + "Month: " + items + "/t|/t", name=str(date), anchor=NW).pack(side=LEFT)
                    Button(xyz, text="Bravo", name="alpha"+date[0], command= partial(goto_url,links[1])).pack(side=RIGHT)
                    Button(xyz, text="Alpha", name="bravo"+date[0], command= partial(goto_url,links[0])).pack(side=RIGHT)

                    months.append(items)

        xyz.pack()


# Notebook Options (p107 Functions)
p107Functions = ttk.Notebook(p107Frame)

p107Functions.add(p107links, text="Project 107 Access Point Charlie")
p107Functions.add(CSVMachine, text="Archiving Tools")

p107Functions.pack(fill=BOTH, expand=True, pady=5)





#####Program Header#####
# Title Options
HeaderFrame = Frame(root, bd=1, relief=RIDGE)
HeaderFrame.pack(fill=X)
rootHeader = Label(HeaderFrame, text="Welcome to The Trialist's Toolkit!", font=('Arial', 10, 'bold'))
rootHeader.pack()

# Menu Options
MenuFrame = Frame(root, bd=1, relief=RIDGE)
selectedProgram = StringVar()
programSelectText = Label(MenuFrame, text="Please Select a Program:")
programSelectMenu = OptionMenu(MenuFrame, selectedProgram, "Project 108 - Cryptography", "Project 107 - Archiving")
programSelectText.pack(side=LEFT)
programSelectMenu.pack(side=RIGHT)
MenuFrame.pack(fill=X)

# Tracers
selectedProgram.trace("w", DisplayPage)
rawCSVSelection.trace("w", CleanCSV)
cleanCSVSelection.trace("w", GenerateFilesystem)

# Sets Default Selected Program
selectedProgram.set("Project 107 - Archiving")

# Opens Root Window
root.mainloop()
