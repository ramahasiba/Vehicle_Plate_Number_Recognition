import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import plate_number_extraction_endpoits 
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'ced.json'

app = FastAPI()

app.include_router(router=plate_number_extraction_endpoits.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload = True)




  
   


# import base64
# from fastapi import FastAPI, File, UploadFile, Form, Body, Request
# from http import HTTPStatus 
# from typing import Dict, List 
# from src.utils import visionAPI as PNE #Plate Number Extraction 
# from fastapi.staticfiles import StaticFiles  
  
# #To delete
# from fastapi import FastAPI
# from fastapi.templating import Jinja2Templates  
# import os
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'ced.json'

# #define a template object           
# templates = Jinja2Templates(directory="templates")
  
# app = FastAPI() 
# app.mount("/static", StaticFiles(directory="static"), name="static")


# @app.get('/')  
# def _search_view(request: Request):
#     return templates.TemplateResponse("index.html", {  
#     "request": request, 
# })   


# @app.post("/extract_plate_number")
# async def _extract_plate_number(my_image: UploadFile = File(...)) -> Dict:  
#     #image must has the same name of the input in the form. 
#     image_bytes = await my_image.read()
#     image_bytes = base64.b64decode(image_bytes) 

#     #contructing an image instance  
#     extracted_number = await PNE.extract_plate_number(my_image)  

#     #get image bytes after drawing the border on the licens plate
#     # image_as_bytes = PNE.draw_plate_border(extracted_number["number_plate_boundaries"], _image)
#     print("Find here the objs: ", extracted_number)

#     return{
#         "gg":"ff",
#         # "plate_number": extracted_number["plate_number"],
#         # "image_as_bytes": extracted_number["image_with_border_on_plate"],
#         } 




