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


# Encoding part


def encode(image, message, nbits):
    encoded_message = encode_message(message, nbits)

    # Data hiding
    # get rid of nbits least significant bits
    image = erase_n_lowest_bits(image, nbits)
    # put the data into those bits
    image = insert_data(image, encoded_message)
    return image


def encode_message(message, nbits):
    # Message encoding
    # make the message characters into indices
    encoded_characters = [encode_char(message[i]) for i in range(len(message))]
    # convert those indices to
    binary_encoded_characters = [number_into_binary_string(encoded_characters[i]) for i in range(len(encoded_characters))]
    # get all the data of indices into one string
    data = "".join(binary_encoded_characters)
    # split data into chunks in size of nbits
    arranged_data = split_data(data, nbits)
    # turn the arranged data into numbers
    arranged_data = [binary_string_into_number(arranged_data[i]) for i in range(len(arranged_data))]
    return arranged_data


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


def split_data(data, nbits):
    re = list()
    i = 0
    while i < len(data):
        buff = ""
        for j in range(nbits):
            buff += data[i]
            i += 1
        re.append(buff)
    return re


def insert_data(image, data):
    data_index = 0
    # just for optimization
    data_len = len(data)
    height = len(image)
    width = len(image[0])

    for i in range(height):
        for j in range(width):
            for k in range(3):
                if data_index < data_len:
                    image[i][j][k] = image[i][j][k] + data[data_index]
                    data_index += 1
                else:
                    return image


def encode_char(value):
    if characters.count(value) == 0:
        raise Exception("can't encode character, character not recognized")
    index = characters.index(value)
    return index


# Decoding part


def decode(image, nbits):
    return 0


def decode_char(value):
    if value >= len(characters):
        raise Exception("can't decode character, out of bounds")
    char = characters[value]
    return char


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


def main():
    # Message to encode
    message = "traps are gay"

    # Number of bits to use
    nbits = 2

    # Create path
    directory = "Pics"
    file_name = "test.png"
    path = os.path.join(directory, file_name)

    # Load image
    image = cv2.imread(path, 1)

    # Show before
    cv2.imshow("before", image)

    # Encode message inside the image
    encoded_image = encode(image, message, nbits)

    # Decode image and receive message
    recovered_message = decode(image, nbits)

    print("Recovered message: ", recovered_message)

    # Show result
    cv2.imshow("after", encoded_image)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()
