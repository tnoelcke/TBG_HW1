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
    def getVal(self,idx):
        NuIdx = idx * 4 #in case of pass by ref.
        return (int(hexlify(self.filePtr[NuIdx:NuIdx+4]),16))
    def len(self):
        return (self.maxIdx - self.minIdx)
    def closeFile(self):
        self.filePtr.close()

# desc: Helper for opening binary files
def openBinaryfile(fStr):
    fileName = fStr + ".dat"
    
    with open(fileName,"r+b") as f:
        filePtr = mmap.mmap(f.fileno(),0)
    return filePtr

# reference: https://codesays.com/2014/solution-to-median-of-two-sorted-arrays-by-leetcode/

def findKth(arrA, arrB, k):
    if len(arrA) > len(arrB):
        arrA, arrB = arrB, arrA
    # indexA = (endIndex + beginIndex_as_0) / 2
    indexA = int((min(len(arrA), k) -1) / 2)
    # indexB =  k - (indexA + 1) -1 for the 0-based index
    indexB = int(k - indexA - 2)

    # Only array arrB contains elements
    if len(arrA) == 0:
        return arrB[k - 1]
    # Both arrA and arrB contain elements, and we need the smallest one
    elif k == 1:
        return min(arrA[0], arrB[0])
    # The median would be either arrA[indexA] or arrB[indexB], while arrA[indexA] and
    # arrB[indexB] have the same value.
    elif arrA[indexA] == arrB[indexB]:
        return arrA[indexA]
    # The median must be in the right part of arrB or left part of arrA
    elif arrA[indexA] > arrB[indexB]:
        return findKth(arrA, arrB[indexB + 1:], k - indexB - 1)
    # The median must be in the right part of arrA or left part of arrB
    else:
        return findKth(arrA[indexA + 1:], arrB, k - indexA - 1)

    # There must be at least one element in these two arrays
    assert not(len(arrA) == 0 and len(arrB) == 0)

    if (len(arrA)+len(arrB))%2==1:
    # There are odd number of elements in total. The median the one in the middle
        return findKth(arrA, arrB, (len(arrA)+len(arrB)) / 2 + 1) * 1.0
    else:
    # There are even number of elements in total. The median the mean value of the
    # middle two elements.
        return ( findKth(arrA, arrB, (len(arrA) + len(arrB)) / 2 + 1) +
                findKth(arrA, arrB, (len(arrA) + len(arrB))/2) ) / 2.0

def findKthForArrayLoop(superlist, kth):
    # superlist is a matrix of m files (or arrays) with n elements each
    print("\nkth is:", kth)
    print("list size is :" ,superlist[0].len())
    # list for kth element of each file
    KthElementsForPair = []
    # loop through each m files
    a = []
    # adjKth is the midpoint of an array m of size n
    adjKth = math.floor( kth / len(superlist) )
    kthElement = 0
    KthElementsForPair = []
    print("adjkth:",adjKth)

    # if kth is greater than the size of the array
    # 1) merge all elements in array m from [midpoint, size]
    #   (ie take the upper half of m arrays and merge them)
    # 2) call findKthElement on the merged array with k = kth mod size
    #  - an optional 3rd case where we have an array m of size 2 so we will not adjust k 
    if(kth > superlist[0].len()):
        print("kth is larger than n array size")
        listOfKthElements = []
        for l in superlist:
            #for item in l[adjKth-1:len(l)]:
            for num in range(adjKth-1, l.len()):
                listOfKthElements.append(l.getVal(num))
        
        listOfKthElements.sort()
        print("list of elemnts" ,listOfKthElements)
        # check if midpoint is 1 (aka array size is 2) 
        if(adjKth ==1):
            kthElement = findKth(listOfKthElements,a,kth)
            print("Kth elemnt if k> length:",kthElement)
        else:
            kthElement = findKth(listOfKthElements,a,kth % (superlist[0].len())+1)
            print("Kth elemnt if k> length:",kthElement)

   # if kth is less than the size of the array
   # adjust midpoint to be the cieling rather than floor of kth / array size
    # 1) merge all elements in array m from [0, midpoint]
    #   (ie take the lower half of m arrays and merge them)
    # 2) call findKthElement on the merged array with k = kth 
    else:
        print("kth is smaller than n array size")
        listOfKthElements = []
        adjKth = math.ceil( kth / len(superlist) )
        print("adjKth",adjKth)
        for l in superlist:
            for num in range(0,adjKth):
                listOfKthElements.append(l.getVal(num))
        print(listOfKthElements)
        listOfKthElements.sort()
        print("list of elemnts",listOfKthElements)
        kthElement = findKth(listOfKthElements, a, kth)
        print("Kth element if k<len",kthElement)
    return kthElement

#findKthForArray(superlist1,5)
#findKthForArrayLoop(superlist1, 4)
#findKthForArrayLoop(superlist1,14)
#findKthForArrayLoop(superlist2, 3)

inputFile = open("input.txt","r")
inputStr = (inputFile.readline().split(','))

numFiles = int(inputStr[0])
numCols = int(inputStr[1])
posElement = int(inputStr[2])

superList = []#list of files
for i in range(1,numFiles+1):
    print(i)
    filePtr = openBinaryfile(str(i))
    superList.append(fileObj(filePtr,0,numCols))

kthValue = findKthForArrayLoop(superList, posElement)
outFile = open("output.txt","w+")
outFile.write(str(kthValue)))
outFile.close()
