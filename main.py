import cv2
import os
from encode import encode
from decode import decode


def main():
    # Message to encode
    message = "traps are gay"

    # Create path
    directory = "Pics"
    file_name = "test.png"
    path = os.path.join(directory, file_name)

    # Load image
    image = cv2.imread(path, 1)

    # Show before
    cv2.imshow("before", image)

    # Encode message inside the image
    encoded_image = encode(image, message)

    # Show result
    cv2.imshow("after", encoded_image)

    # Decode image and receive message
    recovered_message = decode(image)

    print("Recovered message: ", recovered_message)

    cv2.waitKey(0)

if __name__ == "__main__":
    main()
