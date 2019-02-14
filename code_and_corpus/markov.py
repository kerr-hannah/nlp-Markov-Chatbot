import nltk
import pprint
import random

class Markov(object):
    '''
    Class for a Markov model object. This object creates or reads in a dictionary representing
    state transitions and uses that dictionary to generate strings of random text
    '''
    def __init__(self, order=2, dictFile="", maxWordInSentence=20):
        self.table = {}
        self.inputLineCount = 0
        self.inputWordCount = 0
        self.setOrder(order)
        self.setMaxWordInSentence(maxWordInSentence)
        if dictFile:    #if a dictionary was given load the dict to the object
            self.loadDictionary(dictFile)

    def setOrder(self, order=2):
        self.order = order

    def loadDictionary(self, dictFile):
        '''
        Funtion to load dictionary from a given file
        '''
        with open(dictFile, 'r') as dict:
            self.table = eval(dict.read())

    def readFile(self, filename, fileEncoding="utf-8"):
        '''
        Function to open and read the text file that the Markov model will be based on
        '''
        with open(filename, "r", encoding=fileEncoding) as file:
            strLine = " ".join(file)
            self.processLine(strLine)

    def processLine(self,line):
        '''
        Function to process each line of the text file. Tokenizes and creates the table of state transitions
        and their frequencies
        '''
        sent_text = nltk.sent_tokenize(line) #list of sentences
        for sentence in sent_text:
            self.inputLineCount = self.inputLineCount  + 1
            tokens = nltk.word_tokenize(sentence)
            keyList = [ ]
            self.table.setdefault( '<s>', {})  			#Add start of sentence key
            addItem = tuple(tokens[0:self.order])
            if addItem not in self.table['<s>']:
                self.table['<s>'][addItem] = 1
            else:
                self.table['<s>'][addItem] += 1

            for item in tokens:  #loop through each word in the sentence,check list length is long enough, if not then add the item to the list
                if len(keyList) < self.order :
                    keyList.append(item)
                    continue
				#If item is not already in table create an entry, if item is already in table increment the frequency count
                self.table.setdefault(tuple(keyList), {})
                if item not in self.table[tuple(keyList)]:
                    self.table[tuple(keyList)][item] = 1
                else:
                    self.table[tuple(keyList)][item] += 1

				#Remove the first word and push last word on to it
                keyList.pop(0)
                keyList.append(item)
                self.inputWordCount = self.inputWordCount + 1

    def setMaxWordInSentence(self, maxWordInSentence):
        self.maxWordInSentence = maxWordInSentence

    def genText(self, seed):
        '''
        Function to use the Markov chain model to generate a string of random textself
        Length of the generated string will be up to maxWordInSentence
        '''
        begin = self.table['<s>']
        start = [tup for tup in begin if seed in tup ]
        if len(start) >= 1:     #if there is a state transition for the start seed, select a random choice
            key = list(random.choice(start))
        else:
            key = list(random.choice(list(self.table['<s>']))) #since no transitons for seed provided, select a random start state transition
        genStr = " ".join(key)
        for word in range(self.maxWordInSentence): #dynamically loop until maxWordInSentence or a terminal state
            newKey = self.table.setdefault(tuple(key), "")
            if(newKey == ""):
                break
            newVal = random.choice(list(newKey))
            genStr = genStr + " " + str(newVal)

            key.pop(0)
            key.append(newVal)
        return genStr

    def getLineCount(self):
        return self.inputLineCount

    def getWordCount(self):
        return self.inputWordCount

    def outputDict(self, filename):
        '''
        Function to write the generated dictionary representing the matrix of state transitons to a file
        '''
        markovDictFile = open(filename, 'w')
        pprint.pprint(self.table, markovDictFile)
