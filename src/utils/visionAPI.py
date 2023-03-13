# necessary libraries
import os, io
import proto
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

# google credentials ==> json file 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'/ServiceAccountToken.json'


def extract_number(image_path:str):
    """
    Extracts the text and bounding box of a number plate in an image using Google Cloud Vision API's text detection feature.

    Args:
        image_path (str): The file path of the image to process.

    Returns:
        dict: A dictionary containing the following keys:
            - 'number_plate_text': A string representing the extracted text of the number plate.
            - 'number_plate_boundaries': A list of dictionaries representing the four vertices of the 
                bounding box of the number plate. Each dictionary has two keys: 'x' and 'y', representing the x and y coordinates of the vertex, respectively.
    """
    
    # Initialize an empty dictionary to hold the response
    response = {}
    
    # Create a client object to interact with Google Cloud Vision API
    client = vision_v1.ImageAnnotatorClient()
    
    # Open the image file and read its contents as bytes
    opened_image = open(image_path, 'rb')
    content = opened_image.read()

    # Create a Vision API Image object with the image content
    image = vision_v1.types.Image(content= content)
    
    # Use the client object to send the image for text detection
    extracted_text = client.text_detection(image = image)

    # Convert the extracted text to a Python dictionary
    extracted_as_dict= proto.Message.to_dict(extracted_text)

    # Extract the text of the first text annotation (which is assumed to be the number plate)
    response['number_plate_text'] = extracted_as_dict["text_annotations"][0]["description"]
    
    # Extract the vertices of the bounding box of the first text annotation (which is assumed to be the number plate)
    response['number_plate_boundaries'] = extracted_as_dict["text_annotations"][0]["bounding_poly"]["vertices"]
    
    # Return the response dictionary
    return(response)


