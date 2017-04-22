import zbar
from PIL import Image
import cv2
import MySQLdb
import numpy as np
import os
import datetime
import time

db = MySQLdb.connect("localhost", "root", "", "qr_information")
# prepare a cursor object using cursor() method
cursor = db.cursor()
capture = cv2.VideoCapture(0)


def present(fn):

    sql = "SELECT * FROM registration WHERE `Sr_No.` = '%s'" % (fn)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        sn = row[0]
        """fname = row[1]
        lname = row[2]
        cno = row[4]
        gender = row[5]

        # Now print fetched result
        print "Sr No. = %d\nFirst Name = %s\nLast Name = %s\nGender = %s\nContact No. = %s" % (sn,fname, lname, cno,gender)"""
    return sn

def face_rec(sn):

    #dataset creator
    faceDetect = cv2.CascadeClassifier("recognizer\\haarcascade_frontalface_default.xml")
    id = sn

    # read image from database
    sql = "SELECT * FROM registration WHERE `Sr_No.` = '%s'" % (id)
    cursor.execute(sql)
    results = cursor.fetchall()

    for row in results:
        data = row[6]
        with open("photo1.jpg", 'wb') as f:
            f.write(data)

    img = cv2.imread('photo1.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.imwrite("dataSet/User." + str(id) + ".0.jpg", gray[y:y + h, x:x + w])
        #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.waitKey(100)

    #cv2.imshow("Face", img)
    cv2.waitKey(1)
    #trainer

    recognizer = cv2.createLBPHFaceRecognizer()
    path = 'dataSet'

    def getImagesWithID(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        #print(imagePaths)
        faces = []  # list
        IDs = []
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            # l=grayscale
            # open img then convert into numpy array bcz openncv works with numpy array
            faceNp = np.array(faceImg, 'uint8')  # unsigned int 8
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
            #cv2.imshow("Training", faceNp)
            cv2.waitKey(100)
        return np.array(IDs), faces

    Ids, Faces = getImagesWithID(path)
    recognizer.train(Faces, Ids)
    recognizer.save('recognizer/trainingData.yml')
    #cv2.destroyAllWindows()

    #detector
    #cam=cv2.VideoCapture(0)
    rec = cv2.createLBPHFaceRecognizer(threshold=125)
    rec.load("recognizer\\trainingData.yml")
    loop = True
    while loop:

        ret, img = capture.read()
        # status value and captured img
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)

        cv2.imshow("Current", img)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            id, conf = rec.predict(gray[y:y + h, x:x + w])
            if id == sn:
                name = "Present "
                print (conf)
                for (x, y, w, h) in faces:
                    cv2.imwrite("sample.jpg", gray[y:y + h, x:x + w])
                    cv2.waitKey(100)
                loop=False
            else:
                name="unknown "
                print (conf)
            if loop == False:
                print id
                print name
                t = str(datetime.datetime.now())
                print t
                #'%s'" % (id)
                with open("sample.jpg", 'rb') as f:
                    pic = f.read()
                #thedata = open('sample.jpg', 'rb').read()
                query ="INSERT INTO attendance (srno,number,time) VALUES (1,%d,'%s')"%(id,t)
                c=db.cursor();
                n=c.execute(query)
                print n
            cv2.putText(img, name, (x, y + h), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4)
            cv2.imshow("Current", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        try:
            os.remove("dataSet/User." + str(id) + ".0.jpg")
            os.remove("recognizer/trainingData.yml")
            os.remove('photo1.jpg')
        except OSError:
            pass
    #cam.release()
    cv2.destroyAllWindows()


def main():
    # Begin capturing video. You can modify what video source to use with VideoCapture's argument. It's currently set
    # to be your webcam.
    #capture = cv2.VideoCapture(0)
    flag=True
    qr_decoded=''
    while flag:
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        ret, frame = capture.read()

        # Displays the current frame
        cv2.imshow('Current', frame)

        # Converts image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = Image.fromarray(gray)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

        # Scans the zbar image.
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)
        cv2.imshow('Current', frame)
        # Prints data from image.
        for decoded in zbar_image:
            flag = False
            qr_decoded=decoded.data
            #print(qr_decoded)
            no = present(qr_decoded)
            cv2.waitKey(20)
            face_rec(no)
            capture.release()
            db.commit()
            db.close()

if __name__ == "__main__":
    main()
