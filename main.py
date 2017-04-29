from sys import argv
import codecs
import hashlib
import os
from Bucket import Bucket
import sys
from itertools import permutations
import time

print (sys.getrecursionlimit())

sys.setrecursionlimit(0x100000)
hashesToGuess = ["e4820b45d2277f3844eac66c903e84be", "23170acc097c24edb98fc5488ab033fe", "665e5bcb0c20062fe8abaaf4628bb154"]

def getArrangedLetters(str ):
   "Removes spaces, orders letters by alphabet"
   arrangedStr = str.replace(" ","")
   sortedStr = ''.join(sorted(str))
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
    
def searchForWords(bucketToEmpty1, buckets, index, totalLetters):
    """Bega per bucketList pradedant nuo indexo ir aplink ji iki index -1.
       Iki kol uzpildo anagrama, arba pribega index -1 Grazina True ir phrase arba False ir empty string  
    """
    totalBuckets = len(buckets)
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

        candidateWord = buckets[i].bucket
        (matched, bucketToEmpty, lettersLeft) = tryTheCandidate(bucketToEmpty, candidateWord, lettersLeft)
        if (matched):
             newPhrase = " ".join([newPhrase, buckets[i].word])
        #Jei lettersLeft <= 0, reiskias radom fraze anagrama
        if (lettersLeft <= 0):
            return (True, newPhrase)
        #jei i yra ant elemento -1, nuo kurio pradejom, reiskias praejom visa cikla, iseik ir grazink False:
        if (i == index - 1):
            #print(newPhrase)
            return (False, "")
        i += 1


def bigFatPhunction(bucketToEmpty1, buckets, index, totalLetters, goodPhrasesList, fileToWrite):

    i = index
    totalWords = len(buckets)
    (match, newPhrase) = searchForWords(bucketToEmpty1, buckets, i, totalLetters)
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
    #print(i)
    if(i != totalWords -1):
        bigFatPhunction(bucketToEmpty1, buckets, index + 1, totalLetters, goodPhrasesList, fileToWrite)
    return 

def visi_deriniai(str):
    betkaip=str.split(" ")
    perms = [' '.join(p) for p in permutations(betkaip)]
    return (perms)

def gaukZodziusSuIlgiuX(buckets, ilgis):
    geriBucketai = []
    for bucket in buckets:
        if (bucket.wordLength == ilgis):
            geriBucketai.append(bucket.word)
    return tuple(geriBucketai)

#populateUsableDictionary("words.txt", "wordlist", "matched_wordlist")

buckets = getGoodwordsBucketList("matched_wordlist2.txt")
bucketToEmpty, totalLetters = getSearchablePhraseBucketList("words.txt")

def subset_sum(numbers, target, rez, partial=[]):
    s = sum(partial)

    # check if the partial sum is equals to target
    if s == target: 
        print ("sum(%s)=%s" % (partial, target))

        rez.append(partial)
    if s >= target:
        return  # if we reach the number why bother to continue

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i+1:]
        subset_sum(remaining, target, rez, partial + [n]) 

def sum_to_n(n, size, limit=None):
    """Produce all lists of `size` positive integers in decreasing order
    that add up to `n`."""
    if size == 1:
        yield [n]
        return
    if limit is None:
        limit = n
    start = (n + size - 1) // size
    stop = min(limit, n - size + 1) + 1
    for i in range(start, stop):
        for tail in sum_to_n(n - i, size - 1, i):
            yield [i] + tail


# subset_sum([1,2,3,4,5,6,7,8,9,10,11 \
# ,9 ,8 ,7 \
# , 6, 6, 5, 5 \
# ,4, 4, 4 \
# ,3 ,3 ,3 ,3 ,3 \
# ,2, 2, 2, 2, 2 \
# ,1,1,1,1,1 \
# ],18, r1)


# def gaukVariantus(visoVariantu, esamasList):
#     """
#     Kaip su obuoliais. 3 obuolius galima padalinti i: 3 -> [[3], [2,1], [1,1,1]]
#     """
#     rez = []
#     if (visoVariantu == 1):
#         return [[1]]
#     gaukVariantus
#     newList = [[visoVariantu], [ , 1]]
#     esamasList.append(newList)

# print( gaukVariantus(1))
# print( gaukVariantus(2))
# print( gaukVariantus(3))
# print( gaukVariantus(4))
# print( gaukVariantus(5))
# print( gaukVariantus(6))





def isbandykVarianta(b1, b2, b3):
    #n1 = getArrangedLetters(newPhrase)
    #if (''.join(sorted(''.join([b1, b2, b3]))) == "ailnooprssttttuuwy"):
    newPhrase = str(' ').join([b1, b2, b3])
    #print(newPhrase)
    guessableHash = hashlib.md5(newPhrase.encode()).hexdigest()
    if (guessableHash in hashesToGuess):
        print("WE HAVE A WINNER!")
        
        print(newPhrase)
        with codecs.open("winner.txt", "w", "utf-8") as f:
            f.write(newPhrase + "; " + guessableHash + "\n")

for i1 in sum_to_n(18, 3):
    print(i1)

zodziaiSuRaidziuKiekiu = []
for i in range(1, 12):
    print(i)
    zodziaiSuRaidziuKiekiu.append(gaukZodziusSuIlgiuX(buckets, i))
for i1 in sum_to_n(18, 3):
    print(i1)
    for i2 in i1:
        if i2 > 11:
            break
    print("Spausdinam: {}".format(i1))
    p1 = [zodziaiSuRaidziuKiekiu[i1[0] -1], zodziaiSuRaidziuKiekiu[i1[1] -1], zodziaiSuRaidziuKiekiu[i1[2] -1]]


    i = 0
    isViso = len(p1[0])

    perms = permutations(p1)
    for i1, per in enumerate(perms):
        visoListu = len(per)
        i = 0
        for b1 in per[0]:
            start = time.clock()

            i+=1
            for b2 in per[1]:
                for b3 in per[2]:
                    isbandykVarianta(b1, b2, b3)
            end = time.clock()
            print("{}  {} is {}".format(i1, i, isViso))
            print ("%.2gs" % (end-start))


def visi_deriniai2(list1):
    perms = [' '.join(p) for p in permutations(betkaip)]
    return (perms)

#perms =  permutations([zodziaiSuIlgiu7, zodziaiSuIlgiu7_2, zodziaiSuIlgiu4 ])
# for i, p in enumerate(perms):
#     print(str(i))
#arrayOfBucketsSortedByLetterLength = getArrayOfBucketsSortedByLetterLength(buckets)

# goodPhrasesList = []
# with codecs.open("results.txt", "w", "utf-8") as fileToWrite:
#     bigFatPhunction(bucketToEmpty, buckets, 0, totalLetters, goodPhrasesList, fileToWrite)

