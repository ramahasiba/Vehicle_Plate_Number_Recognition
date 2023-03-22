#Parent image(initial layer), this iis from docker hub
FROM python:3.9-slim

#The working dir. that specify that any below instructions will be run in the /folder_name folder
WORKDIR /app 

#Single dot means the path the current directory, 
#Second dot means the path inside the image that I wanna copy my source code to (COPY . .)
COPY . .

# Copy the requirements file into the container
COPY requirements.txt .
 
#RUN instruction runs the command as the image being in build time 
RUN pip install e .
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8080"]
