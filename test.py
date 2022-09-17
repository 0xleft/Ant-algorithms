# mostly use this file as testing function so i dont have to run the main script
import random

def maxFreq(arr):
    n= len(arr)
    count = 0
    selection = 0
    for item in arr:
        if arr.count(item) > count:
            count = arr.count(item)
            selection = item
         
    return selection

def shorten(arr):
    if len(arr) > 3: # delete phermones that are old
        return  arr[-3:]

def chooseMouve(arr, weights, output_count):
    return random.choices(arr, weights, k=output_count)

    
array = [1,2,3,4,5]

print(maxFreq(array), 'max freq')

print(shorten(array), 'shortened')

print(array[:], 'deep copy')

weights = [10,10,30,30,20]

outputs = 2000
choices = chooseMouve(array, weights, outputs)

for i in array:
    print(array.count(i)/outputs)
