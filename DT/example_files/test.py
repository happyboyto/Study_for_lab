if __name__ == '__main__':
    file = open('./example_files/example_1900.txt','r')
    x_list = []
    y_list = []

    while True:
        line = file.readline()
        if line == '':
            break
        splited_line = line.split()
        x_list.append(splited_line[1])
        y_list.append(splited_line[2])
    
    print(len(x_list),len(y_list),len(set(x_list)),len(set(x_list)))