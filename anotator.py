from google.cloud import vision
import cv2

def annotate_shoes(image_path, output_path):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Performs object localization on the image file
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    # Read image using OpenCV
    img = cv2.imread(image_path)

    # Identify and annotate shoes
    for obj in objects:
        if obj.name.lower() in ['shoe', 'footwear']:
            # Extract vertices
            vertices = [(vertex.x * img.shape[1], vertex.y * img.shape[0]) for vertex in obj.bounding_poly.normalized_vertices]
            
            # Draw a bounding box around the shoe
            cv2.rectangle(img, (int(vertices[0][0]), int(vertices[0][1])), (int(vertices[2][0]), int(vertices[2][1])), (0, 0, 255), 5)
            cv2.putText(img, "Shoe", (int(vertices[0][0]), int(vertices[0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)

    # Save the annotated image
    cv2.imwrite(output_path, img)