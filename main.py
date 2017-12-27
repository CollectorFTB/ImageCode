import cv2
import os
from encode import encode
from decode import decode


def main():
    # Message to encode
    message = str(input("Enter message to encode: "))

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

    # Save encoded image
    directory = "Pics"
    file_name = message.split(" ")[0] + ".png"
    path = os.path.join(directory, file_name)
    cv2.imwrite(path, image)

    # Show result
    cv2.imshow("after", encoded_image)

    # Decode image and receive message
    recovered_message = decode(encoded_image)

    print("Message should be the same as input: ", recovered_message)

    cv2.waitKey(0)

if __name__ == "__main__":
    main()
