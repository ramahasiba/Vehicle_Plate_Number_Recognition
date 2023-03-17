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



# google credentials ==> json file 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'/ServiceAccountToken.json'

# Create a client object to interact with Google Cloud Vision API
client = vision_v1.ImageAnnotatorClient()

def extract_plate_number(image_file:UploadFile)-> dict: 

    vertices = extract_plate_number_object(image_file)

    opened_image = cv2.imread(image_file)
    height_, width_, channel = opened_image.shape
         

    left = math.ceil(vertices[0][0])
    right = math.ceil(vertices[1][0])
    top = math.floor(vertices[1][1])
    buttom = math.ceil(top+vertices[2][1]-vertices[1][1])   
     
    
    
    cropped_image = opened_image[top:buttom , left:right]
    
    image_with_border_on_plate = cv2.rectangle(opened_image, (vertices[0][0],vertices[0][1]),(vertices[2][0],vertices[2][1]),(0, 255, 0), 1)
    is_success1, im_buf_arr1 = cv2.imencode(".jpg", image_with_border_on_plate)
    byte_im1 = im_buf_arr1.tobytes()
  
    is_success2, im_buf_arr2 = cv2.imencode(".jpg", cropped_image)
    byte_im2 = im_buf_arr2.tobytes()

    extracted = extract_text_from_image(byte_im2)
    

    plate_number= extracted['text_annotations'][0]['description'].split('\n')[0].replace(':', '-')


    return {
        "plate_number": plate_number, 
        "image_with_border_on_plate": byte_im1
        }
   
    



def extract_text_from_image(image_file:bytes)-> dict:
    


    extracted_as_dict = {}
    
    
    # Create a Vision API Image object with the image content
    image = vision_v1.types.Image(content= image_file)
    
    # Use the client object to send the image for text detection
    extracted_text = client.text_detection(image = image)

    # Convert the extracted text to a Python dictionary
    extracted_as_dict= proto.Message.to_dict(extracted_text)

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






