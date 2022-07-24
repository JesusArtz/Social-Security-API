l = ((43,), (44,), (45,))

arr = ''

for i in l:
    
    print(i[0])
    
    arr = arr + f"{i[0]} "
    

print(arr.replace(' ', ',').rstrip(','))

