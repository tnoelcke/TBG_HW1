import math 

def vankins(superList):
  maxScore = 0
  VMile = []
  n = len(superList)
  #Need n + 1 x n+1 size array as we will be
  #looking at elements bigger than n x n
  for i in range(0, n + 1):
    VMile.append([])
    for j in range(0, n + 1):
      VMile[i].append(0)
  for j in range(n, 0, -1):
    VMile[i-1][j -1] = 0
    for i in range(n, 0, -1):
      VMile[i-1][j-1] = superList[i-1][j-1] + max(VMile[i][j-1], VMile[i -1][j])
      maxScore = max(maxScore, VMile[i-1][j-1])
  print(VMile)
  return maxScore



file = open("input.txt","r")
arraySize = file.readline()
arr =[i.strip('\n').split(',') for i in file]
file.close()
arr = [list(map(int,i)) for i in arr]
result = vankins(arr)
output = open("output.txt", "w")
output.write(str(result))
print(output)
output.close()
