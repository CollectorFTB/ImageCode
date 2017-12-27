import cv2
import os
import math

pixel_range = 256
bits = int(math.log2(pixel_range))


def check_changed_pixel(a,b):
    return [a[i] == b[i] for i in range(3)]


def encode_message(image, message, nbits):
    image = erase_nbits(image, nbits)
    return image


def erase_nbits(image, nbits):
    # Generate string with nbits of 0 in the lsb side
    and_string = (bits-nbits)*'1' + nbits*'0'
    # Turn it into and integer so you can bitwise and it
    and_number = binary_string_into_binary(and_string)
    # just for optimization
    height = len(image)
    width = len(image[0])

    for i in range(height):
        for j in range(width):
            # bitwise all the channels
            image[i][j] = [color & and_number for color in image[i][j]]
    return image


def binary_string_into_binary(number):
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
    re = encode_message(image, "traps are gay", 1)

    # Show result
    cv2.imshow("after", re)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()
