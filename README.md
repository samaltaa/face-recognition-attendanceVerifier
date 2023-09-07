# Facial Recognition Attendance System

The Facial Recognition Attendance System is a Python-based project that utilizes various libraries such as OpenCV, dlib, matplotlib, and the face_recognition Python library to create a robust and efficient system for automatically marking student attendance using facial recognition technology.

## Features

- Capture the face in the video frame using the Haar Cascade algorithm.
- Compare the captured face with the faces encoded and saved in the database using the face_recognition library.
- Record the date and time when a student is marked present.

## Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/samaltaa/facial-recognition-attendance.git
   ```

2. Navigate to the project directory:

   ```bash
   cd facial-recognition-attendanceVerifier
   ```
   

3. Install the required dependencies using pip:

   ```bash
   pip install opencv-python dlib matplotlib face_recognition
   ```

4. Download the Haar Cascade XML file for face detection from [here](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml) and place it in the `data` directory of the project.

## Use cases 

1. Add the images of students to the `students` directory. Make sure each image file is named with the format `name>.jpg` (e.g., `john_doe.jpg`).

2. Run the `encode_faces.py` script to encode the faces and create the face database:

   ```bash
   python EncodeGenerator.py
   ```

3. Run the `main.py` script to start the attendance system:

   ```bash
   python main.py
   ```

4. The system will capture video from the default camera and compare faces with the encoded faces in the database. When a match is found, the student's presence will be recorded along with the date and time in the `attendance.csv` file.

5. Press `q` to exit the attendance system.

## Configuration

You can customize the following parameters in the `attendance_system.py` script:

- `TOLERANCE`: A lower tolerance value increases strictness of face recognition.
- `FRAME_THICKNESS`: Thickness of rectangle drawn around detected faces.
- `FONT_THICKNESS`: Thickness of the font used to display student names.
- `FONT_SCALE`: Scale factor for the font size.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

This project makes use of the following libraries:

- OpenCV: https://opencv.org/
- dlib: http://dlib.net/
- face_recognition: https://github.com/ageitgey/face_recognition

Special thanks to the contributors and maintainers of these libraries. ❤️ 

## Disclaimer

This project is intended for educational and informational purposes only. The creators and contributors of this project are not responsible for any unauthorized or improper use of the system.



