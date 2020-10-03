import cv2 as cv  # opencv-python	4.2.0.32
import os


class FaceRecognition:
    face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

    def __init__(self, file_name):
        self.image = cv.imread(file_name)
        image_gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        self.face = self.face_cascade.detectMultiScale(image_gray, 1.1, 20)
        # a face is a tuple of 4 values (x, y, w, h)

        self.total_detected = 0
        # number will be written at the end of file name to prevent overwriting in case of multiple
        # faces detected in the same picture

    def show_faces(self):
        """Draws a rectangle highlighting the detected face on a copy of the original image"""
        image_copy = self.image
        for (x, y, w, h) in self.face:
            cv.rectangle(image_copy, (x, y), (x+w, y+h), (255, 0, 0))
        cv.imshow("result", image_copy)
        cv.waitKey()  # keep window open until a key is pressed

    def save_portraits(self, file_name, path):
        """Extends the borders of the detected faces to create full portraits, crops them and saves them to individual
        files resized to 200x300 in the "bearbeitet" folder"""

        for (x, y, w, h) in self.face:
            image_copy = self.image
            self.total_detected += 1
            x1 = int(x - w*20/100)  # extend left border by 20%
            x2 = int(x + w + w*20/100)  # extend right border by 20%
            y1 = int(y - h*30/100)  # extend top border by 30%
            y2 = int(y + h + h*70/100)  # extend bottom border by 70%
            cropped_image = image_copy[y1:y2, x1:x2]  # numpy slicing, x and y are switched for some reason
            cropped_image = cv.resize(cropped_image, (200, 300), interpolation=cv.INTER_AREA)
            cv.imwrite(path + "/bearbeitet/" + file_name[:-4] + "_" + str(self.total_detected) + ".jpg", cropped_image)

            # debugging:
            # print "original coordinates: ", "x=", x, "y=", y, "w=", w, "h=", h
            # print "extended coordinates: ", "x1=", x1, "x2=", x2, "y1=", y1, "y2=", y2
            # cv.imshow("Cropped", cropped_image)
            # cv.waitKey()  # show next picture on key press


if __name__ == "__main__":
    folder_path = os.getcwd()
    if not os.path.exists("bearbeitet"):
        os.mkdir("bearbeitet")
    for file in os.listdir(folder_path):
        if ".jpg" in file or ".jpeg" in file or ".png" in file:
            faces = FaceRecognition(file)
            faces.save_portraits(file, folder_path)
            if faces.total_detected == 0:
                print "ERROR: No faces detected in " + file
            else:
                print str(faces.total_detected) + " face(s) found in " + file
    raw_input("Press Enter to continue...")
