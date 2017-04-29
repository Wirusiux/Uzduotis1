from sys import argv
import codecs
import hashlib
import os

import sys

print (sys.getrecursionlimit())

sys.setrecursionlimit(0x100000)

def getArrangedLetters(str ):
   "Removes spaces, orders letters by alphabet"
   arrangedStr = str.replace(" ","")
   sortedStr = ''.join(sorted(arrangedStr))
   return sortedStr

def getUniqueLetters(str):
    return ''.join(set(str))

def IsSubsetOfSet(sStr, BStr):
    bPos = 0
    if (len(sStr) > len(BStr)):
        return False
    for sPos, value in enumerate(sStr):
        while(sPos < len(sStr) and bPos < len(BStr) and BStr[bPos] != sStr[sPos]):
            bPos +=1
        if (bPos >= len(BStr) or sPos >= len(sStr) or BStr[bPos] != sStr[sPos]):
            return False
        bPos +=1
    return True



def populateUsableDictionary(wordsFileName, wordslist, matched_wordlist):
    "Writes usable words to matched_wordlist "
    wordsFile = open(wordsFileName, "r")
    wordsStr = wordsFile.read()
    print ("Phrase: " + wordsStr)

    arrangedLetters = getArrangedLetters(wordsStr)
    print("Arranged letters no space: " + arrangedLetters + " ; length: " + str(len(arrangedLetters)))

    print("Bucket to fill: ")
    bucketToEmpty = makeBucketsLetters(arrangedLetters)
    print(bucketToEmpty)

    goodWords = []
    with codecs.open(wordslist, "r", "utf-8") as dictFile:
        for line in dictFile:
            line2 = line[:-1]

            s1 = set(line2)
            s2 = set(arrangedLetters)
            s3 = s1 - s2
            if (len(s3) == 0):
                if (IsSubsetOfSet(getArrangedLetters(line2), arrangedLetters)):
                    #word is subset of phrase
                    #matchedFile.write(line)
                    #print(line2)
                    goodWords.append(line2)
    with codecs.open(matched_wordlist, "w", "utf-8") as matchedFile:
        sortedUniqueWords = sorted(set(goodWords))
        for word in sortedUniqueWords:
            matchedFile.write(word + "\n")
    print("Total word count: " + str(len(sortedUniqueWords)))



def makeBucketsLetters(word1):
    "Returns map of letters used in the word. For example 'abb' returns {'a':1; 'b':2}"
    letters = {}
    for letter in word1:
        if letter in letters:
            letters[letter] += 1
        else:
            letters[letter] = 1
    return letters

def bigFatPhunction1(bucketToEmpty1, goodBucketList, goodWordsList, index, totalLetters, goodPhrasesList, fileToWrite):
    bucketToEmpty = bucketToEmpty1.copy()
    lettersLeft = totalLetters
    phraseToGuess = ""
    for i in range(index, len(goodBucketList)):
        candidate = goodBucketList[i]
        newBucket = bucketToEmpty.copy()
        tempLettersLeft = lettersLeft
        isGoodWord = True
        for letter in candidate.keys():
            if (newBucket[letter] - candidate[letter] >= 0):
                newBucket[letter] = bucketToEmpty[letter] - candidate[letter]
                tempLettersLeft -= candidate[letter]
            else:
                isGoodWord = False
                break
        if (isGoodWord):
            lettersLeft = tempLettersLeft
            bucketToEmpty = newBucket
            phraseToGuess = " ".join([phraseToGuess, goodWordsList[i]])
        if lettersLeft <= 0:
            phraseToGuess = phraseToGuess[1:]
            guessableHash = hashlib.md5(phraseToGuess.encode('utf-8')).hexdigest()
            print("Phrase found:{};   {}".format(phraseToGuess, guessableHash))
            hashesToGuess = ["e4820b45d2277f3844eac66c903e84be", "23170acc097c24edb98fc5488ab033fe", "665e5bcb0c20062fe8abaaf4628bb154"]
            if (guessableHash in hashesToGuess):
                print("WE HAVE A WINNER!")
                print(phraseToGuess)
                fileToWrite.write(phraseToGuess + "; " + guessableHash + "\n")

            goodPhrasesList.append(phraseToGuess)
            bigFatPhunction(bucketToEmpty1, goodBucketList, goodWordsList, index + 1, totalLetters, goodPhrasesList, fileToWrite)
            break
    if (lettersLeft > 0):
        if(len(goodBucketList) > index):
            bigFatPhunction(bucketToEmpty1, goodBucketList, goodWordsList, index + 1, totalLetters, goodPhrasesList, fileToWrite)
        print("Exiting bigFatPhunction, lettersLeft: {}".format(lettersLeft))
    return 

def tryTheCandidate(bucketToEmpty, candidateWord, lettersLeft):
    #nezinom ar kandidatas tinka, pasikuriam temp kintamuosius
    newBucket = bucketToEmpty.copy()
    tempLettersLeft = lettersLeft
    isGoodWord = True 
    #begam per kandidato raides ir tustimam "bucket", jei nepavyksta istustinti, abort:
    for letter in candidateWord.keys():
        if (newBucket[letter] - candidateWord[letter] >= 0):
            newBucket[letter] = newBucket[letter] - candidateWord[letter]
            tempLettersLeft -= candidateWord[letter]
        else:
            isGoodWord = False
            break
    if (isGoodWord):
        return (True, newBucket, tempLettersLeft)
    return (False, bucketToEmpty, lettersLeft)

    return  (newBucket, lettersLeft) 
    
def searchForWords(bucketToEmpty1, bucketList, wordsList, index, totalLetters):
    """Bega per bucketList pradedant nuo indexo ir aplink ji iki index -1.
       Iki kol uzpildo anagrama, arba pribega index -1 Grazina True ir phrase arba False ir empty string  
    """
    totalBuckets = len(bucketList)
    bucketToEmpty = bucketToEmpty1.copy()
    lettersLeft = totalLetters
    newPhrase = ""
    i = index
    while(True):
        #nueje iki galo, vel griztam nuo pradziu:
        if(i ==totalBuckets):
            i = 0

        candidateWord = bucketList[i]
        (matched, bucketToEmpty, lettersLeft) = tryTheCandidate(bucketToEmpty, candidateWord, lettersLeft)
        if (matched):
             newPhrase = " ".join([newPhrase, wordsList[i]])
        #Jei lettersLeft <= 0, reiskias radom fraze anagrama
        if (lettersLeft <= 0):
            return (True, newPhrase)
        #jei i yra ant elemento -1, nuo kurio pradejom, reiskias praejom visa cikla, iseik ir grazink False:
        if (i == index - 1):
            return (False, "")
        i += 1


def bigFatPhunction(bucketToEmpty1, goodBucketList, goodWordsList, index, totalLetters, goodPhrasesList, fileToWrite):
    hashesToGuess = ["e4820b45d2277f3844eac66c903e84be", "23170acc097c24edb98fc5488ab033fe", "665e5bcb0c20062fe8abaaf4628bb154"]
    i = index
    totalWords = len(goodWordsList)
    (match, newPhrase) = searchForWords(bucketToEmpty1, goodBucketList, goodWordsList, i, totalLetters)
    if (match):
        goodPhrasesList.append(newPhrase)
        guessableHash = hashlib.md5(newPhrase.encode('utf-8')).hexdigest()
        print("Anagram found:{};   {}".format(newPhrase, guessableHash))
        if (guessableHash in hashesToGuess):
            print("WE HAVE A WINNER!")
            print(phraseToGuess)
            fileToWrite.write(phraseToGuess + "; " + guessableHash + "\n")
        
        if(i != totalWords- 1 ):
            bigFatPhunction(bucketToEmpty1, goodBucketList, goodWordsList, index + 1, totalLetters, goodPhrasesList, fileToWrite)
    return 



def getGoodwordsBucketList(wordsFileName):
    with codecs.open(wordsFileName, "r", "utf-8") as dictFile:
        goodBucketList = []
        goodWordsList = []
        for line in dictFile:
            goodWord = line[:-1]
            goodBucketList.append(makeBucketsLetters(goodWord))
            goodWordsList.append(goodWord)
    return (goodBucketList, goodWordsList)
        
def getSearchablePhraseBucketList(filename):
    wordsFile = open(filename, "r")
    wordsStr = wordsFile.read()
    print ("Phrase: " + wordsStr)

    arrangedLetters = getArrangedLetters(wordsStr)
    print("Arranged letters no space: " + arrangedLetters + " ; length: " + str(len(arrangedLetters)))

    print("Bucket to fill: ")
    bucketToEmpty = makeBucketsLetters(arrangedLetters)
    print(bucketToEmpty)

    arrangedUniqueLetters = getArrangedLetters(getUniqueLetters(wordsStr))
    print("Arranged and unique letters: " + arrangedUniqueLetters + " ; length: " + str(len(arrangedUniqueLetters)))
    return (bucketToEmpty, len(arrangedLetters))


#populateUsableDictionary("words.txt", "wordlist", "matched_wordlist")

goodBucketList, goodWordsList = getGoodwordsBucketList("matched_wordlist2.txt")
bucketToEmpty, totalLetters = getSearchablePhraseBucketList("words.txt")


goodPhrasesList = []
with codecs.open("results.txt", "w", "utf-8") as fileToWrite:
    bigFatPhunction(bucketToEmpty, goodBucketList, goodWordsList, 0, totalLetters, goodPhrasesList, fileToWrite)




print("ok")