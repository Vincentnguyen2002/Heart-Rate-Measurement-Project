from filefifo import Filefifo

user = input("choose the file 1 , 2 or 3: ")


data = Filefifo(10, name = "capture_250Hz_0{}.txt".format(user))

first_value = data.get()
second_value = data.get()
third_value = data.get()
fourth_value = data.get()

count = 0
index = 0

my_list = []

first_index = 0
second_index = 1

while True:
    
    first_value = second_value
    second_value = third_value
    third_value = fourth_value
    fourth_value = data.get()
    index += 1

    if first_value < second_value and second_value >= third_value and third_value > fourth_value:
        my_list.append(index)
        count += 1
        if count == 4:
            break


for _ in range(len(my_list)):
    #calculate the sample, seconds , freq
    sample = my_list[second_index] - my_list[first_index]
    seconds = sample/250
    freq = 1 / seconds
    
    #print out the samples, seconds , freq
    print("samples :",sample , "seconds:" , seconds , "freq :", freq)
    
    #condition to stop
    first_index += 1
    second_index += 1
    if first_index >= len(my_list)-1 and second_index >= len(my_list):
        break
    