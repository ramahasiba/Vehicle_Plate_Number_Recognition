from fastapi import APIRouter, File, UploadFile, Form, Body, Request
from http import HTTPStatus 
from typing import Dict 
from src.utils import visionAPI as PNE #Plate Number Extraction 
from fastapi.templating import Jinja2Templates  
 
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

    #contructing an image instance  
    extracted_number =await PNE.extract_plate_number(my_image)  

    #get image bytes after drawing the border on the licens plate
    # image_as_bytes = PNE.draw_plate_border(extracted_number["number_plate_boundaries"], _image)
    print("Find here the objs: ", extracted_number)

    return{
        "plate_number": extracted_number["plate_number"],
        "image_as_bytes": extracted_number["image_with_border_on_plate"],
        } 

