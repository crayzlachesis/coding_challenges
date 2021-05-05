# written by vmiller
# Input file format: one integer in each row

from timeit import default_timer as timer

file_string = input("Enter file_name: ")

with open(file_string) as file:
    temp_array = file.read().split("\n")

temp_array = temp_array[:-1]

array = []

for x in temp_array:
    array.append(int(x))

def hoppafacan(array):

    maxIndex = i = 0
    solutionList = []
    solved = False
    maxmaxHop = 0
    length = len(array)

    while i < length:
        maxHop = 0
        # Check whether current array element value is big enough to exit the array
        if array[i] >= length - i:
            solved = True
            solutionList.append(str(i) + ", out")
            break
        # Check the next element for the biggest possible hop combined wit the the current element
        for j in range(i+1, i+array[i]+1):
            if array[j]+(j-i) > maxHop:
                maxHop = array[j] + (j-i)
                maxIndex = j

        solutionList.append(str(i))
        if maxHop == 0:
            break

        if maxmaxHop < maxIndex-i:
            maxmaxHop = maxIndex-i

        i = maxIndex

    if solved:
        print(solutionList[1:100])
        print(len(solutionList))
        print(maxmaxHop)
    else:
        print("failure")


start = timer()
hoppafacan(array)
end = timer()
print(end-start)