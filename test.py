import datetime


def selectionSort(arr):

    for i in range(len(arr) - 1):
        minIndex = i
        for j in range(i + 1,len(arr)):
            if arr[j] < arr[minIndex]:
                minIndex = j
        if i != minIndex:
            arr[i],arr[minIndex] = arr[minIndex],arr[i]
    return arr
a = [1,4,5,2,7,9,5,6,7,5,2,15]
print(selectionSort(a))

default=datetime.datetime.now()
print(default)


a = [1,2,3]
if 1 not in a:
    print("999")
else:
    print("8585")