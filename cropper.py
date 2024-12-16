from google.cloud import vision
import cv2
import time
from helper import get_image_extension

def annotate_and_crop_best_score(filename):
    image_path = "./uploads/" + filename
    print("image_path",image_path)
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Performs object localization on the image file
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    # Filter objects to only keep those labeled as 'shoe'
    shoe_objects = [obj for obj in objects if obj.name.lower() in ['shoe', 'footwear']]

    # If no shoe is detected, return False
    if not shoe_objects:
        print("No shoes detected.")
        return {"status": 400, "message": "No shoes detected"}
    
    print("shoe_objects",shoe_objects)

    # Find object with highest confidence score
    best_object = min(shoe_objects, key=lambda obj: obj.score)
    
    print("best_object",best_object)

    img = cv2.imread(image_path)
    
    # Extract vertices of the best object
    vertices = [(vertex.x * img.shape[1], vertex.y * img.shape[0]) for vertex in best_object.bounding_poly.normalized_vertices]

    # Read image using OpenCV
    # Crop the region with the best score
    top_left = (int(vertices[0][0]), int(vertices[0][1]))
    bottom_right = (int(vertices[2][0]), int(vertices[2][1]))
    cropped_img = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    
    # Calculate width and height
    width = bottom_right[0] - top_left[0]
    height = bottom_right[1] - top_left[1]
    
    print('top_left',top_left)
    print('bottom_right',bottom_right)
    cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(img, "Shoe", (int(vertices[0][0]), int(vertices[0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)

    output_filename = str(int(time.time())) + "-cropped-image" + get_image_extension(filename)
    output_path = "./cropped_images/" + output_filename
    print("cropped-image output_path", output_path)
    # Save the cropped image
    cv2.imwrite(output_path, cropped_img)
     # Save the image with rectangle
    annotated_file_name = filename.split('.')[0] + "-annotated" + get_image_extension(filename)
    annotated_image_path = "./annotated_images/" + annotated_file_name
    annotated_txt_path = "./annotated_images/" + filename.split('.')[0] + "-annotated.txt"
    cv2.imwrite(annotated_image_path, img)
    content = str(top_left) + "," + str(bottom_right) + "," + str(width) + "," + str(height)
    with open(annotated_txt_path, 'w') as file:
        # Write content to the file
        file.write(content.replace("(","").replace(")","").replace(" ",""))
    return {"annotated_file":annotated_file_name, "cropped_file": output_filename}