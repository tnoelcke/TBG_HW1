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


#returns the index of the largest array in a list of lists based on the top
#position and bottom position.
def chooseLargestList(bottom, top):
	max = 0
	maxIndex = 0
	for i in range(0, len(top)):
		if top[i] - bottom[i] > max:
			max = top[i] - bottom [i]
			maxIndex = i
	return maxIndex

#sums all the elements in an array  
def arraySum(sumList):
	total = 0
	for i in range(0, len(sumList)):
		total = total + sumList[i]
	return total
#checks if we only have one element per array
def onlyOneElm(bottom, top):
	for i in range(0, len(bottom)):
		if(top[i] - bottom[i] > 1):
			return False
	return True

#Subtracts array1 from array2 and stores the result in array1
#assumes they are the same length
def arraySub(array1, array2):
	for i in range(0, len(array1)):
		array1[i] = array1[i] - (array1[i] - array2[i])

#adds array1 to array2 and stores the result in array1
def arrayAdd(array1, array2):
	for i in range(0, len(array1)):
		array1[i] = array1[i] + (array2[i] - array1[i])

#returns the index of value or the nearest element less than value
def binarySearchI(toSearch, value, low, high):
	#sets the first position to check
	#damn you python that doesn't do integer trucation automatically like c...
	if value < toSearch[low]:
		return low
	pos = int(math.ceil((high - low) / 2)) + low
	#if we found our value stop and return because we are done
	if value == toSearch[pos]:
	  return pos + 1
	#if we get down to one item and its smaller than value return pos.
	if high - low <= 1 and value > toSearch[pos]:
	  return pos + 1
	#if the last value we found is larger than value return the element
	#one index lower because we know it will be less than value.
	if high - low <= 1 and value < toSearch[pos]:
	  return pos
	if(value < toSearch[pos]):
	  return binarySearchI(toSearch, value, low, pos - 1)	
	else:
	  return binarySearchI(toSearch, value, pos + 1, high)
		
def findKth(superlist, k, bottom, top):
	#if you have only one array.
	if len(superlist) == 1:
		return superlist[0][k -1]
  #if there is only one element left per array then stop and fink k.
	if k == 1:
		min = superlist[0][len(superlist[0]) - 1]
		for i in range(0, len(superlist)):
			if top[i] - bottom[i] and superlist[i][bottom[i]] < min:
				min = superlist[i][bottom[i]]
				print(min)
		return min
	if onlyOneElm(bottom, top):
		results = []
		for i in range(0, len(superlist)):
			if top[i] - bottom [i] >= 0:
				results.append(superlist[i][bottom[i]])
		results.sort()
		print(k, results, bottom, top)
		return results[k - arraySum(bottom) - 1]
  
	#Find largest Array and choose the middle index
	largest = chooseLargestList(bottom, top)
	length = top[largest] - bottom[largest]-1
	middleIndex = int(length/2) + bottom[largest]
	middle = superlist[largest][middleIndex]
	middleAr = []
	print(largest, length, middleIndex, middle)
	temp = 0
	for i in range(0, len(superlist)):
		temp = binarySearchI(superlist[i], middle, 0, len(superlist[i]) - 1)
		if temp > 0:
			middleAr.append(temp)
		else:
			middleAr.append(0)
	index = arraySum(middleAr)
	if index == k:
		print(index, k, largest, middle, middleAr, bottom, top)
		return middle
	if index > k:
		print(k, index, middleAr,bottom, top, middle)
		arraySub(top, middleAr)
		return findKth(superlist, k, bottom, top)
	if index < k:
		print(k, index, middleAr,bottom, top, middle)
		arrayAdd(bottom, middleAr)
		return findKth(superlist, k , bottom, top)	
	

inputFile = open("input.txt","r")
inputStr = (inputFile.readline().split(','))

numFiles = int(inputStr[0])
numCols = int(inputStr[1])
posElement = int(inputStr[2])

top = []
bottom = []
fileList = []#list of files
superList = []
for i in range(1,numFiles+1):
	print(i)
	filePtr = openBinaryfile(str(i))
	fileList.append(fileObj(filePtr,0,numCols))
	bottom.append(0)
	top.append(numCols)

for i in range(0, len(fileList)):
	temp = []
	for j in range(0, fileList[i].len()):
		temp.append(fileList[i].getVal(j))
	superList.append(temp)
kthValue = findKth(superList, posElement, bottom, top)
outFile = open("output.txt","w+")
outFile.write(str(kthValue))
outFile.close()

	

