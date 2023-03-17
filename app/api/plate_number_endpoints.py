from fastapi import FastAPI, File, UploadFile, Form, Body, Request
from http import HTTPStatus 
from typing import Dict, List 
from src.utils import visionAPI as PNE #Plate Number Extraction 
 

#To delete
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates  
from fastapi.staticfiles import StaticFiles
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'ServiceAccountToken.json'

#define a template object           
templates = Jinja2Templates(directory="templates")
  
app = FastAPI() 

app.mount("/static", StaticFiles(directory="static"), name="static")
#To delete

@app.get('/')  
def _search_view(request: Request):
    return templates.TemplateResponse("index.html", {  
    "request": request, 
})   


@app.post("/extract_plate_number")
async def _extract_plate_number(_image: UploadFile = File(...)) -> Dict:  
    #image must has the same name of the input in the form. 

    #contructing an image instance  
    extracted_number = PNE.extract_plate_number(_image)  

    #get image bytes after drawing the border on the licens plate
    # image_as_bytes = PNE.draw_plate_border(extracted_number["number_plate_boundaries"], _image)
    print("Find here the objs: ", extracted_number)

    return{
        "plate_number": extracted_number["plate_number"],
        "image_as_bytes": extracted_number["image_with_border_on_plate"],
        } 

