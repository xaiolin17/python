input_number = int(input())

def func1(change_str):
    num = 0
    for i in range(len(change_str)):
        change_num = int(change_str[i])
        if change_num == 1:
            num += 2**i

    print(num)

str_number = ''
while 1:
    number = input_number//2
    # print("input_number//2", input_number//2)
    # print("input_number%2", input_number%2)
    str_number += str(input_number%2)
    if number == 0:
        break
    else:
        input_number = number

list_str = list(str_number)
print("list_str",list_str)
index_0 = 0
change_str = list_str
print("change_str",change_str)
for i in range(len(change_str)):
    if i ==0:
        continue
    if change_str[i-1] == '1' and change_str[i] == '0':
        change_str[i], change_str[i-1] = change_str[i-1], change_str[i]
        index_0 += 1
        break
if index_0 == 0:
    change_str.append('1')
    change_str[-2] = '0'

print("result", change_str)

func1(change_str)


