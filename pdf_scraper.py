from trafilatura import fetch_url, extract, extract_metadata
import urllib, urllib.request
import json
from PIL import Image, PSDraw, ImageDraw, ImageFont
import os
import pytesseract
import requests
import time
import tempfile
from pdf2image import convert_from_path

#save list to file
#download pdfs from list, save in /pdf/
#convert pdf to imgs, save to /pdf_img/
#use tesseract to extract text from images in /pdf_img/
#save files to /pdf_ocr/

os.makedirs("./pdf/", exist_ok=True)
os.makedirs("./pdf_img/", exist_ok=True)
os.makedirs("./pdf_ocr/", exist_ok=True)


# fetches 250 articles codes and saves list into a file
with open("codelist.txt","w") as f:
    url = "https://arxiv.org/list/cs.CL/recent?skip=0&show=250"
    downloaded = fetch_url(url)
    result = extract(downloaded)
    for r in result.split("\n"):
        if ":" in r and "[" in r:
            indexStart = r.find(":")
            indexEnd = r.find("[pdf")
            if "(" in r:
                indexEnd = r.find("(")
                
            code = r[indexStart+1:indexEnd-1]
            print(code)
            f.write(code+"\n")

# retrieves pdf from articles, saves pdf in /pdf/ 
with open("codelist.txt") as f:
  file = f.read()
  for code in file.split("\n"):
        url = "https://arxiv.org/pdf/"+code;
        print(url)
        
        response = requests.get(url);
        
        with open('pdf/'+code+".pdf",'wb') as fr:
            fr.write(response.content)
        
        response.close()
        time.sleep(3)
#         break;

# convert pdf to images
i = 0
for subdir, dirs, files in os.walk("./pdf/"):
  for file in files:
    print (file)
    with tempfile.TemporaryDirectory() as path:
        images_from_path = convert_from_path(os.path.join(subdir,file), output_folder="./pdf_img")
        print(f"Converting {i} of {len(files)}")
        i+=1

#reads all files in /pdf_img/, appends all text to arxiv_clean.json
for subdir, dirs, files in os.walk("./pdf_img/"):
    for file in files:
        #print(file)
        with open(os.path.join("./pdf_ocr/",file),"w") as f:
          f.write(pytesseract.image_to_string(Image.open(os.path.join(subdir,file))))
