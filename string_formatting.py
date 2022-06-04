import math

def print_formatted(number):
    if number < 3 :
        width = number
    else:
        try:
            width = math.ceil(math.log2(number))
        except e:
            raise e
    for i in range(1, number+1):
        print("{0:>{width}} {0:>{width}o} {0:>{width}X} {0:>{width}b}".format(i, width=width))
