# input_1 = input("input array1\n").split(' ')
# len_1, input_1 = int(input_1[0]), input_1[1:]
# input_2 = input("input array2\n").split(' ')
# len_2, input_2 = int(input_2[0]), input_2[1:]
# input_k = int(input("input key\n"))
input_1 = [1, 1, 2]
len_1 = 3
input_2 = [1, 2, 3]
len_2 = 3
input_k = 2

change_input1 = 0
index_input1 = change_input1
change_input2 = 0
index_input2 = change_input2
number = 0
cou = 0

for number in range(input_k):
    # print(number)
    if number == 0:
        cou = int(input_1[index_input1]) + int(input_2[index_input2])
        # print(input_1[index_input1],input_2[index_input2])
        index_input1 += 1
        if index_input1 > len_1 -1:
            change_input1 += 1
            index_input1 = change_input1
        index_input2 += 1
        if index_input2 > len_2 -1:
            change_input2 += 1
            index_input2 = change_input2
        continue

    if input_1[index_input1] > input_2[index_input2]:
        cou += int(input_1[index_input1-1]) + int(input_2[index_input2])
        # print(input_1[index_input1],input_2[index_input2])
        index_input2 += 1
        if index_input2 > len_2 -1:
            change_input2 += 1
            index_input2 = change_input2
        continue
    else:
        cou += int(input_2[index_input2-1]) + int(input_1[index_input1])
        # print(input_1[index_input1],input_2[index_input2])
        index_input1 += 1
        if index_input1 > len_1 -1:
            change_input1 += 1
            index_input1 = change_input1
        continue

print(cou)
# print(len_1, input_1,len_2,input_2,input_k)
