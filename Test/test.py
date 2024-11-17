start = -25
step = 0.2
list = [-25]


def append(list, item):
    list.append(item)


while (start < 25):
    start += step
    list.append(round(start, 3))



    
print(list)