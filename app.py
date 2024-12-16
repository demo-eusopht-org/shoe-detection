from flask import Flask, flash, request, redirect, url_for, Response, send_file
from werkzeug.utils import secure_filename
from waitress import serve
import json
import os
from helper import allowed_file, count_files_in_folder
from cropper import annotate_and_crop_best_score
from bg_remover import remove_background
import time
import json
from merge_image import merge

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service_account.json"
os.environ["REPLICATE_API_TOKEN"] = "r8_1cP1Y48k6Z0yqKernQ37YjXpBmQE7fr05Skgc"
os.environ["BG_REMOVER_API_KEY"] = "qtM67gBP22uhGCg9gFxphFb9"

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# upload page
@app.route("/")
def root():
    with open("index.html") as file:
        return file.read()
    
    
@app.route("/detect", methods=["POST"])
def detect():
    if 'file' not in request.files:
        errorResponse = Response(
        response=json.dumps({
            "message": "Something went wrong, Please try again"
            }),
            status=500,
            mimetype='application/json'
        )
        return errorResponse
            
    file = request.files['file']
    extension = request.form['extension']
    template = request.form['template']
    
    print("Request file:", file)
    print("Request extension:", extension)
    print("Request template:", template)
    filename = ""
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '' or extension == '':
        errorResponse = Response(
            response=json.dumps({
                "message": "Something went wrong, Please try again"
                }),
            status=500,
            mimetype='application/json'
        )
        return errorResponse
    
    if file and allowed_file(secure_filename(file.filename) + "." + extension):
        filename = count_files_in_folder(UPLOAD_FOLDER) + "-" + str(int(time.time())) + "-" + secure_filename(file.filename) + "." + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
        # print("filename",filename)
        cropped_image = annotate_and_crop_best_score(filename)
        if(cropped_image == False):
            errorResponse = Response(
                response=json.dumps({
                    "message": "Something went wrong"
                    }),
                status=500,
                mimetype='application/json'
            )
            return errorResponse
        elif('status' in cropped_image and cropped_image['status'] == 400):
            errorResponse = Response(
                response=json.dumps({
                    "message": cropped_image['message']
                    }),
                status=500,
                mimetype='application/json'
            )
            return errorResponse
        bg_removed_image = remove_background(cropped_image["cropped_file"])
        if(bg_removed_image == False):
            errorResponse = Response(
                response=json.dumps({
                    "message": "Something went wrong"
                    }),
                status=500,
                mimetype='application/json'
            )
            return errorResponse
        # print("bg_removed_image",bg_removed_image)
        merged_image = merge(template + '.jpg', template + '.txt', './bg_removed_images/'+bg_removed_image)
        response = Response(
            response=json.dumps({
                "uploaded_image": filename,
                "annotated_image": cropped_image["annotated_file"],
                "cropped_image": cropped_image["cropped_file"],
                "bg_removed_image": bg_removed_image,
                "merged_image": merged_image
                }),
            status=200,
            mimetype='application/json'
        )
        return response
        # return redirect(url_for('root', filename=bg_removed_image))
    else:
        errorResponse = Response(
                response=json.dumps({
                    "message": "Invalid file extention, please use png, jpg or jpeg"
                    }),
                status=500,
                mimetype='application/json'
            )
        return errorResponse


@app.route("/uploaded/<filename>")
def get_uploaded_image(filename):
    directory = "./uploads/"
    # Construct the path to the requested image file
    image_path = directory + filename
    # Use send_file to serve the image file
    return send_file(image_path, mimetype='image/png')


@app.route("/annotated/<filename>")
def get_annotated_image(filename):
    directory = "./annotated_images/"
    # Construct the path to the requested image file
    image_path = directory + filename
    # Use send_file to serve the image file
    return send_file(image_path, mimetype='image/jpg')


@app.route("/cropped/<filename>")
def get_cropped_image(filename):
    directory = "./cropped_images/"
    # Construct the path to the requested image file
    image_path = directory + filename
    # Use send_file to serve the image file
    return send_file(image_path, mimetype='image/jpg')


@app.route("/bg_removed/<filename>")
def get_bg_removed_image(filename):
    directory = "./bg_removed_images/"
    # Construct the path to the requested image file
    image_path = directory + filename
    # Use send_file to serve the image file
    return send_file(image_path, mimetype='image/png')


@app.route("/merged/<filename>")
def get_merged_image(filename):
    directory = "./merge_images/"
    # Construct the path to the requested image file
    image_path = directory + filename
    # Use send_file to serve the image file
    return send_file(image_path, mimetype='image/jpg')


@app.route("/template/<filename>")
def get_template_image(filename):
    directory = "./template/images/"
    # Construct the path to the requested image file
    image_path = directory + filename
    # Use send_file to serve the image file
    return send_file(image_path, mimetype='image/jpg')

@app.route("/get_templetes")
def get_templates():
    directory = "./template/images"
    file_names = []
    for file_name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file_name)):
            file_names.append(file_name)
    
    response = Response(
        response=json.dumps({
            "file_names": file_names
            }),
        status=200,
        mimetype='application/json'
    )
    return response


serve(app, host='0.0.0.0', port=5000)
