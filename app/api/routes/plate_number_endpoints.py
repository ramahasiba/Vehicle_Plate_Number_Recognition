from fastapi import FastAPI, File, UploadFile, Form, Body, Request
from fastapi.templating import Jinja2Templates   
from fastapi.staticfiles import StaticFiles
from http import HTTPStatus 
from typing import Dict, List
import os
from google.cloud import vision
from utils import visionAPI as PNE #Plate Number Extraction 

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
 
client = vision.ImageAnnotatorClient()

#define a template object           
templates = Jinja2Templates(directory="templates")
  
app = FastAPI() 
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')  
def _search_view(request: Request):
    return templates.TemplateResponse("index.html", {  
    "request": request, 
})   


@app.post("/extract_plate_number")
async def _extract_plate_number(_image: UploadFile = File(...)):  
    #image must has the same name of the input in the form. 

    #contructing an image instance  
    extracted_number = PNE.extract_number(_image)  

    #get image bytes after drawing the border on the licens plate
    # image_as_bytes = PNE.draw_plate_border(extracted_number["number_plate_boundaries"], _image)
    print("Find here the objs: ", extracted_number)

    return{"plate_number": extracted_number["number_plate_text"],
           "plate_boundaries": extracted_number["number_plate_boundaries"], 
        #    "image_as_bytes": image_as_bytes,
           } 

