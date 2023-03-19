import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import plate_number_extraction_endpoits 
 
app = FastAPI()

app.include_router(router=plate_number_extraction_endpoits.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

if __name__ == '__main__':
	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload = True)
 