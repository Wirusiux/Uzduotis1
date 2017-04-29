from sys import argv
import codecs
import hashlib
import os
from Bucket import Bucket
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

def getGoodwordsBucketList(wordsFileName):
    with codecs.open(wordsFileName, "r", "utf-8") as dictFile:
        buckets = []

        for line in dictFile:
            goodWord = line[:-1]
            bucket = Bucket()
            bucket.word = goodWord
            bucket.sortedWord = getArrangedLetters(goodWord)
            bucket.wordLength = len(goodWord)
            bucket.bucket = makeBucketsLetters(goodWord)
            buckets.append(bucket)
    return (buckets)
        
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
            if(index == 0):
                print(newPhrase)
                return (False, "")

        candidateWord = bucketList[i]
        (matched, bucketToEmpty, lettersLeft) = tryTheCandidate(bucketToEmpty, candidateWord, lettersLeft)
        if (matched):
             newPhrase = " ".join([newPhrase, wordsList[i]])
        #Jei lettersLeft <= 0, reiskias radom fraze anagrama
        if (lettersLeft <= 0):
            return (True, newPhrase)
        #jei i yra ant elemento -1, nuo kurio pradejom, reiskias praejom visa cikla, iseik ir grazink False:
        if (i == index - 1):
            print(newPhrase)
            return (False, "")
        i += 1


def bigFatPhunction(bucketToEmpty1, goodBucketList, goodWordsList, index, totalLetters, goodPhrasesList, fileToWrite):
    hashesToGuess = ["e4820b45d2277f3844eac66c903e84be", "23170acc097c24edb98fc5488ab033fe", "665e5bcb0c20062fe8abaaf4628bb154"]
    i = index
    totalWords = len(goodWordsList)
    (match, newPhrase) = searchForWords(bucketToEmpty1, goodBucketList, goodWordsList, i, totalLetters)
    if (match):
        newPhrase = newPhrase[1:]
        goodPhrasesList.append(newPhrase)
        guessableHash = hashlib.md5(newPhrase.encode('utf-8')).hexdigest()
        print("Anagram found:{};   {}".format(newPhrase, guessableHash))
        fileToWrite.write(newPhrase + "\n")
        if (guessableHash in hashesToGuess):
            print("WE HAVE A WINNER!")
            
            print(newPhrase)
            with codecs.open("winner.txt", "w", "utf-8") as f:
                f.write(newPhrase + "; " + guessableHash + "\n")
            return
    print(i)
    if(i != totalWords -1):
        bigFatPhunction(bucketToEmpty1, goodBucketList, goodWordsList, index + 1, totalLetters, goodPhrasesList, fileToWrite)
    return 

def getArrayOfBucketsSortedByLetterLength(buckets):
    "pagal zodzio ilgi surikiuojam"
    for i in range(1,length):
        print(i)
        #randam visus zodzius, kuriu ilgis yra 1
        for bucket in buckets:
            if bucket.wordLength == i
    

#populateUsableDictionary("words.txt", "wordlist", "matched_wordlist")

buckets = getGoodwordsBucketList("matched_wordlist_suranka.txt")
bucketToEmpty, totalLetters = getSearchablePhraseBucketList("words.txt")

arrayOfBucketsSortedByLetterLength = getArrayOfBucketsSortedByLetterLength(buckets)

goodPhrasesList = []
with codecs.open("results.txt", "w", "utf-8") as fileToWrite:
    bigFatPhunction(bucketToEmpty, goodBucketList, goodWordsList, 0, totalLetters, goodPhrasesList, fileToWrite)

print("ok")

from itertools import permutations
def visi_deriniai (str):
    betkaip=str.split(" ")
    perms = [' '.join(p) for p in permutations(betkaip)]
    return (perms)


str="airs l n o ops t tut ty u w"
deriniu_listas=visi_deriniai(str)
print(deriniu_listas)

<<<<<<< HEAD

=======
print("ok")
>>>>>>> d97a9a02251ecd8d63d1906084efd857c9051507
