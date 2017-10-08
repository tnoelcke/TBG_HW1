import math

# reference: https://codesays.com/2014/solution-to-median-of-two-sorted-arrays-by-leetcode/

def findKthItem(A, B, k):

            if len(A) > len(B):
                A, B = B, A
            # stepsA = (endIndex + beginIndex_as_0) / 2
            stepsA = int((min(len(A), k) -1)/ 2)
            # stepsB =  k - (stepsA + 1) -1 for the 0-based index
            stepsB = int(k - stepsA - 2)
 
            # Only array B contains elements
            if len(A) == 0:
                return B[k-1]
            # Both A and B contain elements, and we need the smallest one
            elif k == 1:
                return min(A[0], B[0])
            # The median would be either A[stepsA] or B[stepsB], while A[stepsA] and
            # B[stepsB] have the same value.
            elif A[stepsA] == B[stepsB]:
                return A[stepsA]
            # The median must be in the right part of B or left part of A
            elif A[stepsA] > B[stepsB]:
                return findKthItem(A, B[stepsB+1:], k-stepsB-1)
            # The median must be in the right part of A or left part of B
            else:
                return findKthItem(A[stepsA+1:], B, k-stepsA-1)
 
        # There must be at least one element in these two arrays
            assert not(len(A) == 0 and len(B) == 0)
 
            if (len(A)+len(B))%2==1:
            # There are odd number of elements in total. The median the one in the middle
                return findKthItem(A, B, (len(A)+len(B))/2+1) * 1.0
            else:
            # There are even number of elements in total. The median the mean value of the
            # middle two elements.
                return ( findKthItem(A, B, (len(A)+len(B))/2+1) +
                     findKthItem(A, B, (len(A)+len(B))/2) ) / 2.0

alist = [1, 4, 7, 10, 13]
blist = [2, 5, 8, 11, 14]
clist = [3, 6, 9, 12, 15]
dlist = [4, 8, 10 ,12, 20]
list1 = [1,7]
list2 = [2,6]

superlist2 = [list1,list2]


superlist1 = [ alist, blist, clist]

def findKthForArrayLoop(superlist, kth):
    # superlist is a matrix of m files (or arrays) with n elements each
    print("\nkth is:", kth)
    print("list size is :" ,len(superlist[0]))
    # list for kth element of each file
    KthElementsForPair = []
    # loop through each m files
    a = []
    # adjKth is the midpoint of an array m of size n
    adjKth = math.floor( kth / len(superlist) )
    
    KthElementsForPair = []
    print("adjkth:",adjKth)

    # if kth is greater than the size of the array
    # 1) merge all elements in array m from [midpoint, size]
    #   (ie take the upper half of m arrays and merge them)
    # 2) call findKthElement on the merged array with k = kth mod size
    #  - an optional 3rd case where we have an array m of size 2 so we will not adjust k 
    if(kth > len(superlist[0])):
        print("kth is larger than n array size")
        listOfKthElements = []
        for l in superlist:
            for item in l[adjKth-1:len(l)]:
                listOfKthElements.append(item)
        
        listOfKthElements.sort()
        print("list of elemnts" ,listOfKthElements)
        # check if midpoint is 1 (aka array size is 2) 
        if(adjKth ==1):
            print("Kth elemnt if k> length:",findKthItem(listOfKthElements,a,kth))
        else:
            print("Kth elemnt if k> length:",findKthItem(listOfKthElements,a,kth % len(superlist[0])+1))

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
            for item in l[0:adjKth]:
                listOfKthElements.append(item)
        print(listOfKthElements)
        listOfKthElements.sort()
        print("list of elemnts",listOfKthElements)
        print("Kth element if k<len",findKthItem(listOfKthElements, a, kth))


#findKthForArray(superlist1,5)
findKthForArrayLoop(superlist1, 4)
findKthForArrayLoop(superlist1,14)
findKthForArrayLoop(superlist2, 3)
