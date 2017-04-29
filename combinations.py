from sys import argv
import codecs
import hashlib
import os
from Bucket import Bucket
import sys
from itertools import permutations


sys.setrecursionlimit(0x100000)

def visi_deriniai(str):
    betkaip=str.split(" ")
    perms = [' '.join(p) for p in permutations(betkaip)]
    return (perms)

with codecs.open("final.txt", "r", "utf-8") as readFile:
    hashesToGuess = ["e4820b45d2277f3844eac66c903e84be", "23170acc097c24edb98fc5488ab033fe", "665e5bcb0c20062fe8abaaf4628bb154"]
    for i, line in enumerate(readFile):
        goodWord = line[:-2].strip()
        
        print(str(i) + " "+goodWord + ";")
        asd = goodWord.split(" ")
        print (len(asd))
        if (len(asd) < 9):
            for i, derinys in enumerate(visi_deriniai(goodWord)):
                guessableHash = hashlib.md5(derinys.encode('utf-8')).hexdigest()
                if (guessableHash in hashesToGuess):
                    print("WE HAVE A WINNER!")
                    print(derinys)
                    with codecs.open("winner.txt", "w", "utf-8") as f:
                        f.write(derinys + "; " + guessableHash + "\n")
         
