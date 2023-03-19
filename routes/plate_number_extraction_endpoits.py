from fastapi import APIRouter, File, UploadFile, Form, Body, Request
from http import HTTPStatus 
from typing import Dict 
from src.utils import visionAPI as PNE #Plate Number Extraction 
from fastapi.templating import Jinja2Templates  
import cv2
 
def save_image(image_bytes, image_name):
    file_location = f"images/{image_name}"
    with open(file_location, "wb") as file_object:
        file_object.write(image_bytes)

#define a template object           
templates = Jinja2Templates(directory="templates")
  
router = APIRouter() 
 
@router.get('/')  
def _search_view(request: Request):
    return templates.TemplateResponse("index.html", {  
    "request": request, 
})   
  
@router.post("/extract_plate_number")
async def _extract_plate_number(my_image: UploadFile = File(...)) -> Dict:  
    #image must has the same name of the input in the form. 
    # file_ = my_image
    uploaded_image_bytes = await my_image.read()
    # save_image(file_)
    file_name = my_image.filename
    save_image(uploaded_image_bytes, file_name)
    # print(file_name)
    # file_path = str()
    # print(file_path) 
    image = cv2.imread("./images/" + file_name) 
    #contructing an image instance  
    extracted_number = PNE.extract_plate_number(image)  
    # print(extracted_number["image_with_border_on_plate"])
    #get image bytes after drawing the border on the licens plate
    # image_as_bytes = PNE.draw_plate_border(extracted_number["number_plate_boundaries"], _image)
    # # print("Find here the objs: ", extracted_number)
    # bytes_tt = extracted_number["image_with_border_on_plate"]
    save_image(extracted_number["image_with_border_on_plate"], ("bordered" + file_name))

    return { 
        "plate_number": extracted_number["plate_number"], 
        } 

