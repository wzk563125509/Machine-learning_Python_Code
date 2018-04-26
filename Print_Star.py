def print_star(le):
    if(le%2>0):
        mid = le - int(le/2)
        hang = 1
        temp = 1
        while(hang <= le):
            print(' '*(mid-temp)+'*'*(temp*2-1)+' '*(mid-temp))
            if hang < mid:
                temp += 1
            else :
                temp -= 1
            hang += 1

    else:
        mid = le - int(le/2)
        hang = 1
        temp = 1
        while(hang <= le):
            print(' '*(mid-temp)+'*'*(temp*2)+' '*(mid-temp))
            if hang < mid:
                temp += 1
            elif hang > mid:
                temp -= 1
            hang += 1
