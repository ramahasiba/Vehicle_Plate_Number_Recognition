from fastapi import APIRouter, File, UploadFile, Form, Body, Request
from http import HTTPStatus 
from typing import Dict 
from src.utils import visionAPI as PNE #Plate Number Extraction 
from fastapi.templating import Jinja2Templates  
import cv2
 

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
    uploaded_image_bytes = await my_image.read()
 
    file_name = my_image.filename
    PNE.save_image(uploaded_image_bytes, file_name)
    
    #load the image
    image = cv2.imread("./images/" + file_name) 
    #contructing an image instance  
    extracted_number = PNE.extract_plate_number(image)   

    PNE.save_image(extracted_number["image_with_border_on_plate"], ("bordered" + file_name))
 
    return { 
        "plate_number": extracted_number["plate_number"], 
        } 

