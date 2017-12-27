import cv2
import os
import math

pixel_range = 256
lower = [chr(ord('a')+i) for i in range(26)]
upper = [chr(ord('A')+i) for i in range(26)]
digits = [chr(ord('0')+i) for i in range(10)]
special = [' ', '.']
characters = lower + upper + digits + special  # especially length of 64 (log2(64) = 6)
cbits = int(math.log2(len(characters)))
bits = int(math.log2(pixel_range))


def encode_message(image, message, nbits):
    # get rid of nbits least significant bits
    image = erase_n_lowest_bits(image, nbits)
    # make the message characters into indices
    encoded_characters = [encode_char(message[i]) for i in range(len(message))]
    # convert those indices to
    binary_encoded_characters = [number_into_binary_string(encoded_characters[i]) for i in range(len(encoded_characters))]
    # get all the data of indices into one string
    data = "".join(binary_encoded_characters)
    print(data)
    return image


def erase_n_lowest_bits(image, nbits):
    # Generate string with nbits of 0 in the lsb side
    and_string = (bits-nbits)*'1' + nbits*'0'
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


def encode_char(value):
    if characters.count(value) == 0:
        raise Exception("can't encode character, character not recognized")
    index = characters.index(value)
    return index


def decode_char(value):
    if value >= len(characters):
        raise Exception("can't decode character, out of bounds")
    char = characters[value]
    return char


def main():
    # Create path
    directory = "Pics"
    file_name = "test.png"
    path = os.path.join(directory, file_name)

    # Load image
    image = cv2.imread(path, 1)

    # Show before
    cv2.imshow("before", image)

    # Encode message inside the image
    re = encode_message(image, "traps are gay", 2)

    # Show result
    cv2.imshow("after", re)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()
