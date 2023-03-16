from fastapi import FastAPI, File, UploadFile, Form, Body, Request
from fastapi.templating import Jinja2Templates   
from fastapi.staticfiles import StaticFiles
from http import HTTPStatus 
from typing import Dict, List
import os
from google.cloud import vision
# from utils import visionAPI as PNE #Plate Number Extraction 

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

# client = vision.ImageAnnotatorClient()

#define a template object           
templates = Jinja2Templates(directory="templates")

_app = FastAPI() 
_app.mount("/static", StaticFiles(directory="static"), name="static")

@_app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@_app.post("/uploadfile")
async def uploadFile():
    return {"status": "ok"}




