from ultralytics import YOLO
import os
import base64

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def count_files_in_folder(folder_path):
    """
    Count the number of files in a folder.
    
    :param folder_path: The path to the folder.
    :return: The number of files in the folder.
    """
    # Check if the folder exists
    if not os.path.exists(folder_path):
        return 0
    
    # Count the number of files
    file_count = sum([len(files) for _, _, files in os.walk(folder_path)])
    return str(file_count)


def detect_objects_on_image(buf):
    """
    Function receives an image,
    passes it through YOLOv8 neural network
    and returns an array of detected objects
    and their bounding boxes
    :param buf: Input image file stream
    :return: Array of bounding boxes in format 
    [[x1,y1,x2,y2,object_type,probability],..]
    """
    model = YOLO("best.pt")
    results = model.predict(buf)
    result = results[0]
    output = []
    for box in result.boxes:
        x1, y1, x2, y2 = [
          round(x) for x in box.xyxy[0].tolist()
        ]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)
        output.append([
          x1, y1, x2, y2, result.names[class_id], prob
        ])
    # print(output)
    return output

def remove_image_extension(image_name):
    # Split the file name and extension
    base_name, extension = os.path.splitext(image_name)
    # Return the base name (without the extension)
    return base_name

def get_image_extension(image_name):
    # Split the file name and extension
    base_name, extension = os.path.splitext(image_name)
    # Return the base name (without the extension)
    return extension

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        # Read the image file as binary data
        binary_data = img_file.read()
        
        # Encode the binary data as base64
        base64_data = base64.b64encode(binary_data)
        
        # Decode bytes to string (Python 3)
        base64_str = base64_data.decode("utf-8")
        
        return base64_str
  