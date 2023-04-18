import sys

new_size = 500
mysFile = open("./cositas.png","rb")
info = mysFile.read()
length_inf = info.__len__()
mul = 0
new_size -=1 ##cosiderando que D quita un byte
while(new_size * (mul+1) < length_inf):
    print(info[new_size * mul : new_size * (mul + 1) - 1])
    mul += 1