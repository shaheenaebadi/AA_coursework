'''
To install face_recognition, simply use 'pip install face_recognition' in a terminal
However, often you may meet an error about the 'dlib' library with cmake.
The easy solution is to visit https://github.com/z-mahmud22/Dlib_Windows_Python3.x and download the 
compiled wheels locally with the python version, and install it from local

if you want to show the found image with the known face, you need opencv and also uncomment the related code.

'''


#import cv2
import time
import face_recognition
import os

'''
def show_found_image(unknow_image):
    face_locations = face_recognition.face_locations(unknown_image)

    # Draw rectangles around faces
    for top, right, bottom, left in face_locations:
        cv2.rectangle(unknown_image, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow("Found Image", cv2.cvtColor(unknown_image, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
'''


start = time.time()
# Load the known face image and get the features of the face
known_image = face_recognition.load_image_file("dataset/task1_4/known_man.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

folder_path = "dataset/task1_4/imageset/"
filenames = [file.name for file in os.scandir(folder_path) if file.is_file()]

for filename in filenames:
    # Load the unknown face image
    unknown_image = face_recognition.load_image_file(folder_path+filename)

    # Find faces and encodings in the unknown image
    unknown_encodings = face_recognition.face_encodings(unknown_image)

    for unknown_encoding in unknown_encodings:
    # Compare the unknown face encoding with the known encoding
        matches = face_recognition.compare_faces([known_encoding], unknown_encoding)

        if matches[0]:  # If a match is found
            print("Match found! in " + filename)
            #show_found_image(unknown_image)
            break

print(time.time()-start)        



