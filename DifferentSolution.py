import math

#returns the index of the largest array in a list of lists based on the top
#position and bottom position.
def chooseLargestList(top, bottom):
  max =[0, 0]
  for i in range(0, len(top)):
    if top[i] - bottom[i] > max[0]:
      max[0] = top[i] - bottom[i]
      max[1] = i
  return max[1]

#sums all the elements in an array  
def arraySum(sumList):
  total = 0
  for i in range(0, len(sumList)):
    total = total + sumList[i]
  return total
  
#Subtracts array1 from array2 and stores the result in array1
#assumes they are the same length
def arraySub(array1, array2):
  for i in range(0, len(array1)):
    array1[i] = array1[i] - array2[i]

#adds array1 to array2 and stores the result in array1
def arrayAdd(array1, array2):
  for i in range(0, len(array1)):
    array1[i] = array1[i] + array2[i]

#returns the index of value or the nearest element less than value
def binarySearchI(toSearch, value, low, high):
	#sets the first position to check
	#damn you python that doesn't do integer trucation automatically like c...
	pos = int(math.ceil((high - low) / 2)) + low
	#if we found our value stop and return because we are done
	if value == toSearch[pos]:
		return pos
	#if we get down to one item and its smaller than value return pos.
	if high - low <= 1 and value > toSearch[pos]:
		return pos
	#if the last value we found is larger than value return the element
	#one index lower because we know it will be less than value.
	if high - low <= 1 and value < toSearch[pos]:
		return pos - 1 
	if(value < toSearch[pos]):
		return binarySearchI(toSearch, value, low, pos - 1)	
	else:
		return binarySearchI(toSearch, value, pos + 1, high)


#finds the kth item in a list of list.
def findKth(superList, k, bottom, top):
  #finds the largest array and picks the middle element
  if k == 1:
    min = superArray[0][bottom[0]]
    for i in range(0, len(superList) - 1):
      if superArray[i][bottom[i]] < min:
        min = superArray[i][bottom[i]]
    return min
  largest = int(chooseLargestList(top, bottom))
  length = top[largest] - bottom[largest]
  middleIndex = int(length/2)
  middle = superList[largest][middleIndex]
  print(largest, middleIndex, length, top, bottom)
  #holds on to the index of the other arrays middle index
  middleArray = []
  index = 0
  #find the middleth element in each array so we can find what index middle is at
  for i in range(0, len(superList)):
    index = binarySearchI(superList[i], middle, 0, len(superList[i]) - 1) 
    middleArray.append(index + 1)
  #sum the array so we can find what index middle is at.
  index = arraySum(middleArray)
  #if our index == k then stop because we are done.
  if index == k:
    return index
  #if index is larger than k take the bottom half of the lists.
  if index > k:
    arraySub(top, middleArray)
    return findKth(superList, k, bottom, top)
  #otherwise take ther larger half of the array.
  else: 
    if index < k:
      k = k - index
      arrayAdd(bottom, middleArray)
      return findKth(superList, k, bottom, top)
      

array1 = [1, 5, 10, 15, 20]
array2 = [2, 3, 13, 16, 21]
array3 = [4, 7, 11, 12 , 23]
array4 = [6, 8, 9, 14, 25]
superArray = [array1, array2, array3, array4]
bottom = [0, 0, 0, 0]
top = [len(array1), len(array2), len(array3), len(array4)]


print(findKth(superArray, 25, bottom, top))