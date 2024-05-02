"""
7#6$5#12
157
"""
def func1(x,y):
    # #
    return 4*x+3*y+2

def func2(x,y):
    # $
    return 2*x+y+3

input_list = input().split("$")
# print(input_list)
con = 0
new_list = []
for i in input_list:
    if i.find("#") == -1:
        new_list.append(int(i))
        continue
    else:
        x_y = i.split("#")
        x, y = int(x_y[0]), int(x_y[1])
        number = func1(x, y)
        new_list.append(number)
# print(new_list)
redu = 0
index_new_list = 0
y = 0
for i in new_list:
    if index_new_list == 0:
        redu = int(i)
    else:
        y = int(i)
        # print(redu, y)
        redu = func2(redu, y)

    index_new_list += 1

print(redu)


