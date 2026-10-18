<a id="readme-top"></a>

# Py Camera Vision

**Py Camera Vision** is a Python application for webcam face recognition.

The application detects faces in a video stream, 
compares their features with those stored in SQLite, and displays the first and last name of the recognized person. 
Unknown faces are marked as `Unknown`. New users can be registered via the PyQt6 interface: their first and last name, and facial feature vector, are stored in the database.

<img width="1536" height="1024" alt="Detect Human App Over Scenic Landscape" src="https://github.com/user-attachments/assets/378de72a-d46b-43b9-9a38-c8cbe4bcd39a" />

## Technologies

- Python
- PyQt6
- OpenCV
- NumPy
- SQLite3

## Structure

Py_camera_vision\
└── src\
    ├── database\
    │    ├── create_bd.py\
    │    ├── find_user.py\
    │    ├── update_db.py\
    │    └── users.db\
    ├── models\
    │    ├── face_detection_yunet_2023mar.onnx\
    │    ├── face_recognition_sface_2021dec.onnx\
    │    └── hand_landmarker.task\
    ├── ui\
    │    └── MainWindow.py\
    ├── vision\
    │    ├── face_detector.py\
    │    ├── finger_count.py\
    │    └── finger_ok.py\
    └── main.py

## Install & start

1. Cloning and installing addictions
    ``` bash
    git clone https://github.com/igorehkere/py_camera_vision.git
    cd py_camera_vision
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    ```

2. Creating database (only on the first time)
    ```bash
    cd src/database
    python3 create_bd.py
    ```

3. Starting application
    ```bash
    cd src
    python3 main.py
    ```

## License

MIT

## Author

Igorehkere

<p align='right'><a href='#readme-top'>Back to top</a></p>
