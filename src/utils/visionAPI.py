import os, io
# from google.cloud import vision
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'venv\ServiceAccountToken.json'

client = vision_v1.ImageAnnotatorClient()

print(client)
print(dir(client))