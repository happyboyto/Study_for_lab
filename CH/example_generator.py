import random


def generate_example(num):
    example_file = open('example_{0}.txt'.format(num), 'w')
    x_min, x_max = 0, 1000
    y_min, y_max = 0, 1000

    for i in range(num):
        ID = str(i+1)
        x = str(random.randint(x_min, x_max))
        y = str(random.randint(y_min, y_max))
        line = ID+'\t'+x+'\t'+y+'\n'
        example_file.write(line)

    example_file.close


if __name__ == "__main__":
    generate_example(50)
