import cv2
from paddleocr import PaddleOCR

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Load English OCR model

def extract_clean_nutritional_information(image_path):
    """
    Extracts and cleans nutrients and their corresponding values from an image.

    Args:
        image_path (str): Path to the image file.

    Returns:
        dict: Dictionary with nutrients as keys and their corresponding values.
    """
    # Perform OCR on the image
    results = ocr.ocr(image_path, cls=True)

    # Initialize dictionary to store extracted data
    nutrients_data = {}
    lines = []

    # Extract text from OCR results
    for line in results[0]:
        text = line[1][0]  # Extract detected text
        lines.append(text)

    # Process lines to form nutrient-value pairs
    for i, line in enumerate(lines):
        if "Per" in line or "SERVE SIZE" in line or "%" in line or "Approximate" in line:
            continue  # Skip table headers or irrelevant rows

        # Ensure next line is numeric (value) and doesn't contain percentages
        if i + 1 < len(lines):
            value = lines[i + 1]
            if any(char.isdigit() for char in value) and "%" not in value:
                nutrients_data[line.strip()] = value.strip()

    # Remove duplicates and redundant values
    cleaned_data = {}
    for key, value in nutrients_data.items():
        if key not in cleaned_data:
            cleaned_data[key] = value

    return cleaned_data  # Return the cleaned dictionary


# Main Execution
if __name__ == "__main__":
    image_path = "food1.jpg"  # Replace with your image path
    extracted_data = extract_clean_nutritional_information(image_path)

    # Print the cleaned results in dictionary format
    print("Extracted Nutrients and Values:")
    print(extracted_data)  # Print as dictionary