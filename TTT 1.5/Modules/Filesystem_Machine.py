#############################################################################################
#Documentation: Filesystem Machine - Module Edition
# Parses a spreadsheet a generates a filesystem from download links & timestamps
#Coded by Tyler Pryjda
#############################################################################################
#####Imports
#############################################################################################
import os, csv
import urllib.request as urllib
import tempfile, shutil
from pathlib import Path
import Modules.imgurdownloader as id

#############################################################################################
#####Functions
#############################################################################################
def download(url, year, date, pathtoarchive):

    # Cleans Variables
    url = "".join(url.replace("\"", ""))
    url = "".join(url.replace(" ", ""))

    # Determine the appropriate directory for the file
    destination = pathtoarchive + "\\" + year + "\\" + date + "\\"

    # Create the directory
    os.makedirs(os.path.dirname(destination), exist_ok=True)

    # Download file directly into the directory
    images = id.ImgurDownloader(url, destination)
    images.save_images()

def generate_filesystem(year, pathtofile, filename, pathtoarchive):

    # Set the current directory to that of the input csv file
    os.chdir(pathtofile)

    # Open and parse csv file
    with open(filename, 'r') as importcsv:
        csvreader = csv.reader(importcsv, delimiter=',')

        # For every row with a value that isn't the header and isn't empty
        for row in csvreader:
            if len(row) > 0 and row[0] != "Date":
                # download from url to downloaddir and then move into archive sorted by year/month/day

                row[0] = row[0].replace("/","\\")
                download(row[1], year, row[0], pathtoarchive)

#############################################################################################
#####Main
#############################################################################################
