import math

# allowed characters are only abc, ABC, 012, ' ', '.'

# region Characters and constants
lower = [chr(ord('a')+i) for i in range(26)]
upper = [chr(ord('A')+i) for i in range(26)]
digits = [chr(ord('0')+i) for i in range(10)]
special = [' ', '.']
characters = lower + upper + digits + special  # especially length of 64 (log2(64) = 6 bits)

nbits = 2
pixel_range = 256
cbits = int(math.log2(len(characters)))
bits = int(math.log2(pixel_range))
# endregion

# General functions


def binary_string_into_number(number):
    """
    :param number: string representing a binary number 
    :return: numeric value of number
    """
    # result
    re = 0
    # 2-factor
    factor = 0
    number = int(number)

    while number > 0:
        re += (number % 2) * 2**factor
        number //= 10
        factor += 1
    return re


def number_into_binary_string(number):
    re = ['0']*cbits
    i = cbits-1
    while number > 0:
        re[i] = chr(ord('0') + (number % 2))
        number >>= 1
        i -= 1
    re = "".join(re)
    return re


def erase_n_bits(image, mode):
    and_string = ""
    # Generate string with nbits of 0 in the lsb/msb side depending on mode
    if mode == 'lsb':
        and_string = (bits - nbits) * '1' + nbits * '0'
    elif mode == 'msb':
        and_string = (bits - nbits) * '0' + nbits * '1'
    # Turn it into and integer so you can bitwise and it
    and_number = binary_string_into_number(and_string)
    # just for optimization
    height = len(image)
    width = len(image[0])

    for i in range(height):
        for j in range(width):
            # bitwise and all the channels with the and number
            image[i][j] = [color & and_number for color in image[i][j]]
    return image
