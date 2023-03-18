# necessary libraries
import os, io
import numpy as np
import proto
import cv2
import math
from io import BytesIO
from PIL import Image
from fastapi import UploadFile
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import re

 
# google credentials ==> json file 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'ced.json'
 
# Create a client object to interact with Google Cloud Vision API
client = vision_v1.ImageAnnotatorClient()

async def extract_plate_number(image_file:UploadFile)-> dict: 
    contents = image_file.read()
    print(contents)
    nparr = np.fromstring(contents, np.uint8) 
    print(nparr)
    print("Its type: ", type(nparr))
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  
    
    # Extract the bounding box coordinates of the license plate
    vertices = extract_plate_number_object(nparr)

    # Draw a rectangle around the license plate and encode the image as a byte string
    image_with_border_on_plate = cv2.rectangle(img, (vertices[0][0],vertices[0][1]),(vertices[2][0],vertices[2][1]),(0, 255, 0), 1)
    is_success1, im_buf_arr1 = cv2.imencode(".jpg", image_with_border_on_plate)
    image_byte_im = im_buf_arr1.tobytes()

    # Crop the license plate from the image and encode it as a byte string
    left = math.ceil(vertices[0][0])
    right = math.ceil(vertices[1][0])
    buttom = math.ceil(vertices[1][1])
    top = math.ceil(buttom + vertices[2][1] - vertices[1][1])
    cropped_image = img[buttom:top , left:right]
    is_success2, im_buf_arr2 = cv2.imencode(".jpg", cropped_image)
    croped_byte_im = im_buf_arr2.tobytes()

    # Extract text from the cropped image and replace any colons with dashes
    extracted_text = extract_text_from_image(croped_byte_im)
    text = extracted_text['text_annotations'][0]['description'].replace(":", "-")

    # Use regular expressions to extract the license plate number from the text
    plate_number = re.findall(r'\d{1}-\d{4}-\d{2}|\d{1}-\d{4}-[A-Z]{1}|\d{2}-\d{3}-\d{2}|\d{3}-\d{2}-\d{3}', text)

    # Return the license plate number and the image with a border around the license plate
    return {
    "plate_number": plate_number, 
    "image_with_border_on_plate": image_byte_im
    }
    



def extract_text_from_image(image_file:bytes)-> dict:
    


    extracted_as_dict = {}
    
    
    # Create a Vision API Image object with the image content
    image = vision_v1.types.Image(content= image_file)
    
    # Use the client object to send the image for text detection
    extracted_text = client.text_detection(image = image)

    # Convert the extracted text to a Python dictionary
    extracted_as_dict = proto.Message.to_dict(extracted_text)

    return extracted_as_dict




def extract_plate_number_object(image_file:UploadFile)-> list:

    
    plate_bounding = []


    opened_image = cv2.imread(image_file)
    height, width = opened_image.shape[:2]

    content = image_file.read()

   
    image = vision_v1.types.Image(content= content)
    
    objects = client.object_localization(image=image)

    objects_as_dict = proto.Message.to_dict(objects)
    
    for object_ in objects_as_dict['localized_object_annotations']:

        if object_['name'] == 'License plate':
            for vertice in object_['bounding_poly']['normalized_vertices']:

                vertice['x']=round(vertice['x']* width)
                vertice['y']=round(vertice['y']* height)

                plate_bounding.append((vertice['x'], vertice['y']))

         
    return plate_bounding






