def four_letters(names):
    num = 0
    split_names = names.split(' ')
    for i in range(0, len(split_names)):
        if len(split_names[i]) == 4:
            num = num + 1
    return num

names = "Tror Gvigris Deriana Nori"
print (four_letters(names))