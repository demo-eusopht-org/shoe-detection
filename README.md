
# Shoe Detection and Replacement Using Flask

A Python Flask-based web application that detects shoes in an image and replaces them with a user-provided shoe image. This project combines computer vision with an intuitive user interface to create a seamless shoe replacement experience.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

---

## Introduction

This project is a Flask application designed to process images by detecting shoes and replacing them with a user-provided shoe image. It leverages machine learning techniques for object detection and computer vision libraries for image manipulation. The application is simple to use, providing an interactive web interface where users can upload images and preview results.

---

## Features

- **Shoe Detection**: Uses advanced object detection algorithms to identify shoes in an image.
- **Shoe Replacement**: Replaces detected shoes with a user-specified shoe image.
- **Web Interface**: Intuitive interface for image uploads and result previews.
- **Customizable**: Supports configuration of detection thresholds and output image size.

---

## Technologies Used

- **Python**: The programming language for backend logic.
- **Flask**: The web framework for building the application.
- **OpenCV**: For image processing and manipulation.
- **Google Cloud Vision**: For shoe detection model.
- **HTML/CSS/JavaScript**: For creating the web interface.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/shoe-detection-replacement.git
   cd demo-eusopht-org
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Also we have Pre-Trained Model For Shoe Detection **:
   Shoe Detection Pre-Trained model is created by using roboflow and yolov8. It's place in the `models/` directory.

5. **Run the Application**:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to `http://127.0.0.1:5000`.

---

## Usage

1. Navigate to the web interface in your browser.
2. Upload an image containing shoes.
3. Select an image from the following.
4. Click "Process" to view and download the updated image.

---

## Project Structure

```
shoe-detection/
├── app.py                  # Main Flask application
├── templates/              # HTML templates for the web interface
├── static/                 # Static files (CSS, JS, images)
├── models/                 # Pre-trained models for shoe detection
├── utils/                  # Helper scripts for image processing
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## Configuration

- **Detection Threshold**: Adjust the model confidence threshold in `app.py`.
- **Output Image Size**: Configure the resolution of processed images in the application settings.
- **Model Path**: Ensure the model file is correctly linked in `app.py`.

---

## Examples

Here are some example use cases:

### Annotated Image
![Annotated Image](annotated_images/)

### Background Removed Shoe
![Background Shoe](bg_removed_images/)

### Merge Image
![Merge Shoe](merge_images/)

---

## Troubleshooting

- **Flask Server Not Starting**: Ensure all dependencies are installed and the virtual environment is activated.
- **Model Not Found**: Verify that the model file exists in the `models/` directory.
- **Image Processing Issues**: Check if the uploaded images meet the required format (e.g., JPG/JPEG/PNG).

---