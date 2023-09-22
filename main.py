import cv2
import time
from win10toast import ToastNotifier
import threading


def main():
    dist_to_screen = int(input("how far do you want to be from the screen?"))

    toaster = ToastNotifier()
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


    cap = cv2.VideoCapture(0)

    total_width = 0
    num_faces = 0
    start_time = time.time()


    min_width_threshold = 100

    while True:
        time.sleep(0.5)
        _, img = cap.read()


        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            face_width_pixels = w
            
    
            if face_width_pixels >= min_width_threshold:

                total_width += face_width_pixels
                num_faces += 1


        cv2.imshow('img', img)


        elapsed_time = time.time() - start_time
        if elapsed_time >= 10:
            if num_faces > 0:
                # Calculate the average width
                average_width = total_width / num_faces
                dist = 13104.6/(average_width + 12.5049) - 7.97122
                print(dist)
                if dist < dist_to_screen:
                    toaster.show_toast("Screen distancing", "Get further from your screen", duration=2)
            else:
                print("No faces meeting the threshold detected in the last 10 seconds")

    
            total_width = 0
            num_faces = 0
            start_time = time.time()


        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    # Release the VideoCapture object
    cap.release()

if __name__ == "__main__":
    main()