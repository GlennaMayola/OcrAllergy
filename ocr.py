import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np

IMAGE_PATH = 'gmd.jpg'

reader = easyocr.Reader(['en'])
result = reader.readtext(IMAGE_PATH)
result

def extract_ingredients_list(ocr_output):
    ingredient_list = []
    for entry in ocr_output:
        text = entry[1]  # Extract the text
        # Split by both commas and semicolons to separate ingredients properly
        split_text = text.replace(';', ',').split(',')
        for part in split_text:
            # Clean each part and remove unwanted characters
            cleaned_text = ''.join(filter(lambda x: x.isalnum() or x.isspace(), part)).strip()
            if cleaned_text:  # Add non-empty entries to the list
                ingredient_list.append(cleaned_text)
    return ingredient_list

# Call the function
ocr_output = result
ingredients_list = extract_ingredients_list(ocr_output)
print(ingredients_list)