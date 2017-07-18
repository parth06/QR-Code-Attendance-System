# QR-Code-Attendance-System
The proposed solution offers a QR code for the attendees to scan it via a specific application. The QR code along with the attendee’s identity taken by the application will confirm his attendance. 

This system also takes care of preventing unauthorized attendance registration using multi-factor authentication. Thus, the designed solution also uses facial recognition technology to authenticated user in addition to QR Code. That is, it considers “Something you have” i.e. QR Code for event, and “Something you are” i.e. face recognition by capturing your face to confirm identity of attendee. 

The Application works in the described manner:
i.   User Registration is done via registration.html
ii.  User's QR Code is generated inside the Database.Thus,Distribution of QR Code takes place.
iii. The application detects the QR Code decodes it,fetches the data of the user from the database and generates the recognizer database        for each user at the time of decoding.
iv.  The design then runs the face recognizition algorithm to authenticate the user.
v.   After identifing the user it makes an entry into the database regarding time of entrance of attendee and then it removes the              recognizer database created specially for him/her.

## Installation ##

Requirements:
* Python 2.7
* Windows or Linux 
* OpenCV 
* numpy	(version 1.11.1)
* MySQL-python (version 1.2.5)
* Pillow (version 4.0.0)
* zbar (version 0.10)

