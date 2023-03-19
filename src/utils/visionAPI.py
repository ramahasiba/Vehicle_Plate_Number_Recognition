# necessary libraries
import os, io
import numpy as np
import proto
import cv2
import math
import re 
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

 
# google credentials ==> json file 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'/ServiceAccountToken.json'

# Create a client object to interact with Google Cloud Vision API
client = vision_v1.ImageAnnotatorClient()

def extract_plate_number(image:np.ndarray)-> dict:
 """
    Extracts the license plate number from an image and returns it along with the image
    with a border around the plate.

    Parameters:
        image (np.ndarray): A numpy array containing the image.

    Returns:
        A dictionary with the following keys:
            - 'plate_number': The extracted license plate number as a string.
            - 'image_with_border_on_plate': A byte string representing the image. 
    """
  

    # Extract the bounding box coordinates of the license plate
    vertices = extract_plate_number_object(image)
   
    # Draw a rectangle around the license plate and encode the image as a byte string
    image_with_border_on_plate = cv2.rectangle(image, (vertices[0][0],vertices[0][1]),(vertices[2][0],vertices[2][1]),(0, 255, 0), 5)
    is_success1, im_buf_arr1 = cv2.imencode(".jpg", image_with_border_on_plate)
    image_byte_im = im_buf_arr1.tobytes()

    
    # Crop the license plate from the image and encode it as a byte string
    left = math.ceil(vertices[0][0])
    right = math.ceil(vertices[1][0])
    buttom = math.ceil(vertices[1][1])
    top = math.ceil(buttom + vertices[2][1] - vertices[1][1])   
    cropped_image = image[buttom:top , left:right]
    is_success2, im_buf_arr2 = cv2.imencode(".jpg", cropped_image)
    croped_byte_im = im_buf_arr2.tobytes() 

    # Extract text from the cropped image and replace any colons with dashes    
    extracted_text = extract_text_from_image(croped_byte_im)
    text = extracted_text['text_annotations'][0]['description'].replace(":", "-")
    

    # Use regular expressions to extract the license plate number from the text
    plate_number = re.findall(r'\d{1}-\d{4}-\d{2}|\d{1}-\d{4}-[A-Z]{1}|\d{2}-\d{3}-\d{2}|\d{3}-\d{2}-\d{3}', text)
 
    # Return the license plate number and the image with a border around the license plate
    return {"plate_number": plate_number, "image_with_border_on_plate": image_byte_im}
   
    



def extract_text_from_image(image_file:bytes)-> dict:
    
    """
    Extracts text from an image using Google Cloud Vision API.

    Args:
        image_file (bytes): A byte string containing the image to be processed.

    Returns:
        dict: A Python dictionary containing the extracted text and related information
    
    """

    extracted_as_dict = {}
    
    
    # Create a Vision API Image object with the image content
    image = types.Image(content= image_file)
    # 
    # Use the client object to send the image for text detection
    extracted_text = client.text_detection(image = image)  

    # Convert the extracted text to a Python dictionary
    extracted_as_dict = proto.Message.to_dict(extracted_text) 

    return extracted_as_dict




def extract_plate_number_object(image_array:np.ndarray)-> list:

    """
    Extracts the coordinates of the bounding box surrounding the license plate in the input image.

    Args:
        image_array (numpy ndarray): An input image in numpy ndarray format.

    Returns:
        list: A list of tuples where each tuple contains the x and y coordinates of the four corners of the bounding box
        surrounding the license plate detected in the input image.


    """
    
    plate_bounding = []

    # Get the height and width of the input image
    height, width = image_array.shape[:2]
    
    # Encode the input image to JPEG format using OpenCV
    is_success, im_buf_arr = cv2.imencode(".jpg", image_array)
    byte_im = im_buf_arr.tobytes()

    # Create a vision_v1.types.Image object from the byte string
    image = vision_v1.types.Image(content= byte_im)

    # Use Google Cloud Vision API's object_localization function to detect objects in the image
    objects = client.object_localization(image=image)

    # Convert the resulting objects object to a dictionary
    objects_as_dict = proto.Message.to_dict(objects)

    for object_ in objects_as_dict['localized_object_annotations']:

        # If the object is a license plate, extract the bounding box vertices
        if object_['name'] == 'License plate':
            for vertice in object_['bounding_poly']['normalized_vertices']:
    
                # Convert the normalized vertex coordinates to pixel coordinates
                vertice['x'] = vertice['x']* width
                vertice['y'] = vertice['y']* height

                # Append a tuple containing the x and y coordinates of each vertex to the plate_bounding list
                plate_bounding.append((vertice['x'], vertice['y']))

    return plate_bounding



def save_image(image_bytes: bytes, image_name: str) -> None:
     """
    Saves an image file to the 'images' directory with the specified name.

    Parameters:
        image_bytes (bytes): A byte string representing the image file.
        image_name (str): The name of the image file to be saved.

    Returns:
        None
    """

   # Construct the file path by joining the 'images' directory and the specified file name
    file_location = f"images/{image_name}"

    # Open the file in binary write mode and write the image byte string to it
    with open(file_location, "wb") as file_object:
        file_object.write(image_bytes)

    



