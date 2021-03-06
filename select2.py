#!/usr/bin/env python3
import mmap
import math
import copy
from binascii import hexlify

# reference: https://codesays.com/2014/solution-to-median-of-two-sorted-arrays-by-leetcode/

class fileObj:
    def __init__(self,ptr,minIdx,maxIdx):
        self.filePtr = ptr
        self.minIdx = minIdx
        self.maxIdx = maxIdx
        self.lastStoredMiddleIdx = 0
    def getVal(self,idx):
        nuIdx = self.minIdx + (idx * 4) #in case of pass by ref.
        return (int(hexlify(self.filePtr[nuIdx:nuIdx+4]),16))
    def getValAtStoredMid(self):
        nuMid = self.minIdx + (self.lastStoredMiddleIdx * 4)
        return (int(hexlify(self.filePtr[nuMid:nuMid+4]),16))
    def len(self):
        return (self.maxIdx - self.minIdx)
    def closeFile(self):
        self.filePtr.close()
    def compare(self,x):
        return (self.filePtr == x.filePtr)

# desc: Helper for opening binary files
def openBinaryfile(fStr):
    fileName = fStr + ".dat"
    
    with open(fileName,"r+b") as f:
        filePtr = mmap.mmap(f.fileno(),0)
    return filePtr


#reference http://www.geeksforgeeks.org/k-th-element-two-sorted-arrays/

#for M == 2
def findKthItem(A, B, k):
    while True:
        #BaseCases
        if A.len() == 0 or B.len() == 1:
            return B.getVal(k)
        if B.len() == 0 or A.len() == 1:
            return A.getVal(k)
        #end BaseCases

        #mids
        mid1 = max(math.floor(A.len() / 2),0)
        mid2 = max(math.floor(B.len() / 2),0)
        #end mids

        #sum indexes
        if (mid1 + mid2) < k:
            #resize file ranges
            if A.getVal(mid1) > B.getVal(mid2):
                B.minIdx += mid2+1 #or max
                k = max(k - mid2 -1,0)
            else:
                A.minIdx += mid1+1 #or max
                k = max(k - mid1 -1,0)
        else:
            #resize file ranges
            if A.getVal(mid1) > B.getVal(mid2):
                A.maxIdx -= mid1
            else:
                B.maxIdx -= mid2

def findLargest(superList):
    largest = superList[0]
    for subList in superList:
        if subList.len() > largest.len():
            largest = subList

    return largest

#modeled after findKthItem
def findKthForMFiles(superList,kth):
    adjKth = kth

    for subList in superList:#replace with lambda
        subList.maxIdx = adjKth


    while True:
        #find sum Indexes
        sumIndexes = 0
        for subList in superList:#replace with lambda
            sumIndexes += subList.len()
        #end find sum indexes

        #assign new mid indexes
        for subList in superList:#replace with lambda
            subList.lastStoredMiddleIdx = max(math.floor(subList.len() / 2),0)
        #end assign new mid indexes

        #BaseCase
        count = 0
        largeList = findLargest(superList)
        for subList in superList:#replace with lambda
            if subList.len() == 1 or subList.len() == 0:
                count += 1
        if count == len(superList) -1:
            print("count equals superlist")
            print(adjKth)
            return largeList.getVal(adjKth)#look over this again

        if sumIndexes == adjKth:
            print("equals adjkth")
            return largeList.getVal(adjKth)
        #end BaseCase


        print(sumIndexes)
        if sumIndexes < adjKth:
            for subList in superList:#replace with lambda
                if not subList.compare(largeList):
                    #resize file ranges
                    if largeList.getValAtStoredMid() > subList.getValAtStoredMid():
                        print("1")
                        subList.minIdx += subList.lastStoredMiddleIdx + 1
                        adjKth = max(adjKth - subList.lastStoredMiddleIdx - 1,0)
                    else:
                        #resize largest file
                        print("2")
                        oldLargest = None
                        for subList in superList:#replace with lambda
                            if subList.compare(largeList):
                                oldLargest = subList
                        largeList = subList
                        oldLargest.minIdx += oldLargest.lastStoredMiddleIdx + 1
                        adjKth = max(adjKth - oldLargest.lastStoredMiddleIdx - 1,0)
                        
        else:
            for subList in superList:#replace with lambda
                if not subList.compare(largeList):
                    print("l:",largeList.getValAtStoredMid())
                    print("s:",subList.getValAtStoredMid())

                    #resize file ranges
                    if largeList.getValAtStoredMid() > subList.getValAtStoredMid():
                        print("3")
                        subList.maxIdx -= subList.lastStoredMiddleIdx
                    else:
                        print("4")
                        #resize largest file
                        oldLargest = None
                        for subList in superList:#replace with lambda
                            if subList.compare(largeList):
                                oldLargest = subList
                        largeList = subList
                        oldLargest.maxIdx -= oldLargest.lastStoredMiddleIdx





            

def findKthForArrayLoop(superList, kth):
    
    adjKth = math.floor( kth / (2*len(superList)^2) )
    KthElementsForPair = []

    if len(superList) == 1: #O(1)
        return superList[0].getVal(kth)
    elif len(superList) == 2:#O(log n)
        return findKthItem(superList[0], superList[1], kth-1)
    else:
        return findKthForMFiles(superList,kth)



#findKthForArray(superlist1,5)
#findKthForArrayLoop(superlist1, 4)
#findKthForArrayLoop(superlist1,14)
#findKthForArrayLoop(superlist2, 3)

inputFile = open("input.txt","r")
inputStr = (inputFile.readline().split(','))

numFiles = int(inputStr[0])
numCols = int(inputStr[1])
posElement = int(inputStr[2])

fileSuperList = []#list of files
for i in range(1,numFiles+1):
    filePtr = openBinaryfile(str(i))
    fileSuperList.append(fileObj(filePtr,0,numCols))

kthValue = findKthForArrayLoop(fileSuperList, posElement)
print(kthValue)
# outFile = open("output.txt","w+")
# outFile.write(str(kthValue))
# outFile.close()
