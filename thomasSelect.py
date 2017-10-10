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

#returns the index of value or such that the index is the next lowest
#item in the array.
def binarySearchI(toSearch, value, low, high):
	#If the value is less than the lowest element return.
	if value < toSearch.getVal(low):
		return low
	#sets the first position to check
	pos = int(math.ceil((high - low) / 2)) + low
	#if we found our value stop and return because we are done.
	if value == toSearch.getVal(pos):
	  return pos + 1
	#if we get down to one item and its smaller than value return pos.
	if high - low <= 1 and value > toSearch.getVal(pos):
	  return pos + 1
	#if the last value we found is larger than value return the element
	#one index lower because we know it will be less than value.
	if high - low <= 1 and value < toSearch.getVal(pos):
	  return pos
	#Takes recursive step
	if value < toSearch.getVal(pos):
	  return binarySearchI(toSearch, value, low, pos - 1)
	else:
	  return binarySearchI(toSearch, value, pos + 1, high)
		
def findKth(superlist, k, bottom, top):
	#if you have only one array chose k and return.
	if len(superlist) == 1:
		return superlist[0].getVal(k - 1)
  #if k is the smallest remaining element in the array
	if (k - arraySum(bottom))  == 1:
		min = superlist[0].getVal(len(superlist[0]) - 1)
		#find the smallest element and return.
		for i in range(0, len(superlist)):
			if top[i] - bottom[i] and superlist[i].getVal(bottom[i]) < min:
				min = superlist[i].getVal(bottom[i])
		return min
	#if each column only has one element remaining find the kth element in the columns 
	if onlyOneElm(bottom, top):
		results = []
		#Loop through and grab the remaining elements
		for i in range(0, len(superlist)):
			#make sure that i is still a valid element
			if top[i] - bottom [i] >= 0:
				results.append(superlist[i].getVal(bottom[i]))
		#sort the list and return the kth element
		results.sort()
		return results[k - arraySum(bottom) - 1]
	
	#Find largest Array and choose the middle index
	largest = chooseLargestList(bottom, top)
	length = top[largest] - bottom[largest]-1
	middleIndex = int(length/2) + bottom[largest]
	middle = superlist[largest].getVal(middleIndex)
	middleAr = []
	temp = 0
	#loop through the list of lists and find the index where middle = listValue
	#or the value of the index of the nearest lower element
	for i in range(0, len(superlist)):
		temp = binarySearchI(superlist[i], middle, bottom[i], top[i] - 1) 
		if temp > 0:
			middleAr.append(temp)
		else:
			middleAr.append(0)
	index = arraySum(middleAr)
	#if the sum of our middle indexs == k you found the kth element and return
	if index == k:
		return middle
	#if index is greater than k take the the lower side of the lists
	if index > k:
		arraySub(top, middleAr) #eliminates higher elements
		return findKth(superlist, k, bottom, top)
	#if index is greater than k tkae the high side of the lists
	if index < k:
		arrayAdd(bottom, middleAr) #Eliminates lower elements.
		return findKth(superlist, k , bottom, top)
	

#Get the input from the text file
inputFile = open("input.txt","r")
inputStr = (inputFile.readline().split(','))

#parse input
numFiles = int(inputStr[0])
numCols = int(inputStr[1])
posElement = int(inputStr[2])

#set up for call to kth element.
top = [] # tracks the higher array indexes
bottom = [] #tracks the lower array indexes
superList = [] #Holds the file pointers
#load up the file pointers into our array
for i in range(1,numFiles+1):
	filePtr = openBinaryfile(str(i))
	superList.append(fileObj(filePtr,0,numCols))
	bottom.append(0)
	top.append(numCols)

#get the kth value and output it.
kthValue = findKth(superList, posElement, bottom, top)
print("kth: ", kthValue)
outFile = open("output.txt","w+")
outFile.write(str(kthValue))
outFile.close()

	

