from util import *
# Decoding part


def decode(image):
    # get only encoded data
    image = erase_n_bits(image, 'msb')
    # get the length of the encoded message
    length = decode_length(image)
    # get all the pixels containing data about the message
    return length, " lol fake message ignore"


def decode_length(image):
    # grab the last n bits of each encoded length-pixel
    encoded_length = get_n_last_bits(image)
    # join nbits into chunks of cbits, and for each chunk, turn it into decimal
    decoded_length = join_and_decode_bits(encoded_length)
    # translate decoded numbers into characters
    length = translate_decoded_length(decoded_length)
    return length


def decode_char(value):
    if value >= len(characters):
        raise Exception("can't decode character, out of bounds")
    char = characters[value]
    return char


def get_n_last_bits(image):
    height = len(image) - 1
    encoded_length = [0] * 24
    for j in range(1, 9):
        for k in range(1, 4):
            encoded_length[-k - (j - 1) * 3] = number_into_binary_string(image[height][-j][-k])[-nbits:]
    return encoded_length


def join_and_decode_bits(encoded_length):
    decoded_length = [0] * 8
    encoded_binary_character = ""
    for i in range(0, 24, cbits // nbits):
        for j in range(cbits // nbits):
            encoded_binary_character += encoded_length[i + j]
        decoded_length[i // (cbits // nbits)] = binary_string_into_number(encoded_binary_character)
        encoded_binary_character = ""
    return decoded_length


def translate_decoded_length(decoded_length):
    for i, character in enumerate(decoded_length[:]):
        decoded_length[i] = decode_char(character)

    length = ""
    for i in range(len(decoded_length)):
        try:
            int(decoded_length[i])
            length += decoded_length[i]
        except ValueError:
            pass
    return int(length)