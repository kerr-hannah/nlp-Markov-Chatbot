"""
This file takes the Cornell Movie Dialog Corpus as it is downloaded and formats
the data from the several files into one file of dialog lines.

Based off code by Matthew Inkawhich posted in a tutorial using this same corpus
(Only the code for pre-processing the data is used as the rest of the tutorial 
covers a different project)

Inkawhich, Matthew. “Chatbot Tutorial.” PyTorch, 2017, pytorch.org/tutorials/beginner/chatbot\_tutorial.html.
"""
import os
import codecs

corpus_name = "cornell movie-dialogs corpus"
corpus = os.path.join("cornell_movie_dialogs_corpus", corpus_name)

def printLines(file, n=10):
    with open(file, 'rb') as datafile:
        lines = datafile.readlines()
    for line in lines[:n]:
        print(line)

#printLines(os.path.join(corpus, "movie_lines.txt"))

# Splits each line of the file into a dictionary of fields
def loadLines(fileName, fields):
    lines = {}
    with open(fileName, 'r', encoding='iso-8859-1') as f:
        for line in f:
            values = line.split(" +++$+++ ")
            # Extract fields
            lineObj = {}
            for i, field in enumerate(fields):
                lineObj[field] = values[i]
            lines[lineObj['lineID']] = lineObj
    return lines

# Extracts pairs of sentences from conversations
def extractSentences(lines):
    sentences = []
    for line in lines:
        # Iterate over all the lines
        text = lines[line]["text"].strip()
        if text:
            sentences.append(text)
    return sentences

def main():

    # Define path to new file
    datafile = os.path.join(corpus, "formatted_movie_lines.txt")

    delimiter = '\t'
    # Unescape the delimiter
    delimiter = str(codecs.decode(delimiter, "unicode_escape"))

    # Initialize lines dict, conversations list, and field ids
    lines = {}
    MOVIE_LINES_FIELDS = ["lineID", "characterID", "movieID", "character", "text"]

    # Load lines
    print("\nProcessing corpus...")
    lines = loadLines(os.path.join(corpus, "movie_lines.txt"), MOVIE_LINES_FIELDS)
    # Write new text file
    print("\nWriting newly formatted file...")
    allLines = extractSentences(lines)
    file =  open(datafile, 'w', encoding='utf-8')
    for i in range(len(allLines)):
        file.write(allLines[i] + '\n')
    #Print a sample of lines

    print("\nSample lines from file:")
    printLines('formatted_movie_lines.txt')
main()
