################################################################################
#Documentation: CSV Machine
# CSV Machine is a small module for converting csv "raw" csv files into "clean" csv files
#Coded by Tyler Pryjda
################################################################################
#####Imports
################################################################################
import os
import csv
from pathlib import Path
################################################################################
#####Variables
################################################################################
#Input for this program is very specific. It requires a string, which is the name of a file being processed. The file should begin with a 4 digit year, and end in raw.csv. The 1st column of the file should only be dates
year = ""
# Selects Current Directory as Filesystem
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rootFilesystem = str(Path(__file__).parent.parent)
################################################################################
#####Functions
################################################################################
def clean_csv(rawcsv):
    exportfields = ["Date", "Images"]
    importrows = []
    exportrows = []

    year = rawcsv[:4]

    os.chdir(rootFilesystem + "\Archives\Spreadsheets\Raw")

    rawfilename = year + "raw.csv"
    cleanfilename = year + "clean.csv"
 
    with open(year + "raw.csv", 'r') as importcsv:
        csvreader = csv.reader(importcsv, delimiter=',')

        for row in csvreader:
            importrows.append(row[0:])

    for rows in importrows: #for every line
        for items in rows[1:]: #for every cell on every line
            if len(items) > 5:
                if items[:17].lower() == "https://imgur.com":
                    exportrows.append([rows[0], items])

    os.chdir(rootFilesystem + "\Archives\Spreadsheets\Clean")

    with open(year +"clean.csv", "w") as exportcsv:
        csvwriter = csv.writer(exportcsv)
        csvwriter.writerow(exportfields)
        csvwriter.writerows(exportrows)
################################################################################