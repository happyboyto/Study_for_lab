import random
import math


def generate_example(num):
    example_file = open('example_{0}.txt'.format(num), 'w')
    r_min, r_max = 0, 100
    
    # x_min, x_max = 0, 1000
    # y_min, y_max = 0, 1000

    for i in range(num):
        ID = str(i+1)
        r = random.uniform(r_min,r_max)
        theta = random.uniform(0,2*math.pi)
        x = str(r*math.cos(theta))
        y = str(r*math.sin(theta))
        # x = str(random.uniform(x_min, x_max))
        # y = str(random.uniform(y_min, y_max))
        line = ID+'\t'+x+'\t'+y+'\n'
        example_file.write(line)

    example_file.close


if __name__ == "__main__":
    for i in range(1):
        num = 100
        generate_example(num)
