from util import *
# Encoding part


def encode(image, message):
    encoded_message = encode_message(message)

    # Data hiding
    # get rid of nbits least significant bits
    image = erase_n_bits(image, 'lsb')
    # put the data into those bits
    image = insert_data(image, encoded_message)
    # store length of message in the end
    image = store_length(image, len(encoded_message))
    return image


def encode_message(message):
    # Message encoding
    # make the message characters into indices
    encoded_characters = [encode_char(message[i]) for i in range(len(message))]
    # convert those indices to
    binary_encoded_characters = [number_into_binary_string(encoded_characters[i]) for i in range(len(encoded_characters))]
    # get all the data of indices into one string
    data = "".join(binary_encoded_characters)
    # split data into chunks in size of nbits
    arranged_data = split_data(data)
    # turn the arranged data into numbers
    arranged_data = [binary_string_into_number(arranged_data[i]) for i in range(len(arranged_data))]
    return arranged_data


def split_data(data):
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


def store_length(image, length):
    # just for optimization\
    height = len(image)-1
    # check how many pixels the original message will take
    length = ((length - 1)//3 + 1)*3
    # encode the number of pixels
    encoded_length = encode_message(str(length))
    # insert the encoded length to the last 24 pixels
    for j in range(1, 9):
        for k in range(1, 4):
            if ((j-1) * 3 + (k-1)) < len(encoded_length):
                image[height][-j][-k] = encoded_length[-k - (j - 1) * 3]

    return image


def encode_char(value):
    if characters.count(value) == 0:
        raise Exception("can't encode character, character not recognized")
    index = characters.index(value)
    return index