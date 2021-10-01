import random
import math
import numpy as np


def generate_example(num):
    example_file = open('./example_files/example_{0}.txt'.format(num), 'w')
    #r_min, r_max = 0, 100
    
    x_min, x_max = 0, num*1000
    y_min, y_max = 0, num*1000
    
    x_list = random.sample(range(x_min, x_max),num)
    y_list = random.sample(range(y_min, y_max),num)
    
    for i in range(num):
        ID = str(i+1)
        line = ID+'\t'+str(x_list[i]/100)+'\t'+str(y_list[i]/100)+'\n'
        example_file.write(line)

    example_file.close


if __name__ == "__main__":
    for i in range(1):
        num = 7000
        generate_example(num)
