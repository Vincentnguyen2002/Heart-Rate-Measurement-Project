from filefifo import Filefifo
user = input("choose the file 1 , 2 or 3: ")


data = Filefifo(10, name = "capture_250Hz_0{}.txt".format(user))

two_second_value = 2/(1/250)

#read the value
default_min = data.get()
default_max = data.get()


sample = 0

#find the min and max
for value in range(two_second_value):
    sample = data.get()
    if sample < default_min:
        default_min = sample
    elif sample > default_max:
        default_max = sample

for _ in range(2500):
    data_value = data.get()
    result = (data_value * 100) / default_max
    print(result)