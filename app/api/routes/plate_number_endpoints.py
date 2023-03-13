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


@app.post("/uploadfile")
async def create_file(_image: UploadFile = File(...)):  
    try:
        #image must has the same name of the input in the form.
        # cont = await _image.read() 
        #contructing an image instance  
        objects = PNE.extract_number(_image)  
        print("Find here the objs: ", objects)
    
        return{"Status": "Succeeded"}
    except:
        return{"Status": "Some error has occured"}

