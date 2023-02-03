import requests
import os

url = "https://drive.google.com/drive/folders/1PBk6QbsA7LISa74J5gRS0PCphb06LsCH?usp=share_link"
response = requests.get(url)
open("file.zip", "wb").write(response.content)
os.system("unzip file.zip")
os.system("python user_int.py")
