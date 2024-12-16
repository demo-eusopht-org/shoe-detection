from PIL import Image
import time

def merge(templete_image, templete_txt, overlay_image_path):
    top_left_position = ""
    bottom_right_position = ""
    width = ""
    height = ""

    with open('./template/box/'+templete_txt, 'r') as file:
        data = str(file.read()).split(",")
        top_left_position = [int(data[0]), int(data[1])]
        bottom_right_position = [int(data[2]), int(data[3])]
        width = data[4]
        height = data[5]
        
    box = {
        "top_left": top_left_position,  # (x, y) coordinates of the top-left point of the box
        "bottom_right": bottom_right_position,  # (x, y) coordinates of the bottom-right point of the box
        "width": int(width),  # Width of the box
        "height": int(height)  # Height of the box
    }
        
    output_filename = str(int(time.time())) + "-merge-image.jpg"
    output_image_path = "./merge_images/" + output_filename
    # Open background image
    background_image = Image.open('./template/images/'+templete_image)

    # Open overlay image
    overlay_image = Image.open(overlay_image_path)

    # Resize overlay image to fit the box
    overlay_image = overlay_image.resize((box["width"], box["height"]))

    # Paste overlay image onto background image
    background_image.paste(overlay_image, (box["top_left"][0], box["top_left"][1]), overlay_image)

    # Save the resulting image
    background_image.save(output_image_path)
    
    print("output_filename",output_filename)
    
    return output_filename