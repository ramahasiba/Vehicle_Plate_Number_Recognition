from fastapi import FastAPI
from fastapi.templating import Jinja2Templates  
from fastapi.staticfiles import StaticFiles


#define a template object           
templates = Jinja2Templates(directory="templates")
  
app = FastAPI() 

app.mount("/static", StaticFiles(directory="static"), name="static")

from plate_number_endpoints import *
 


