import openai

# Define your OpenAI API key
openai.api_key = ""  # Replace with your OpenAI API key

# Function to adjust nutritional values based on serving size
def adjust_nutritional_values(nutritional_data, reference_grams, serving_size):
    """
    Adjust nutritional data from the reference grams to the actual serving size.

    Args:
        nutritional_data (dict): Nutritional data per 'reference_grams'.
        reference_grams (float): The reference scale for the nutritional data (e.g., 100g, 50g).
        serving_size (float): The actual serving size in grams.

    Returns:
        dict: Nutritional data adjusted for the actual serving size.
    """
    serving_ratio = serving_size / reference_grams
    adjusted_data = {}
    
    for nutrient, value in nutritional_data.items():
        try:
            # Convert the nutrient value to a float, strip non-numeric characters where necessary
            numeric_value = float(''.join(c for c in value if c.isdigit() or c == '.'))
            adjusted_data[nutrient] = f"{numeric_value * serving_ratio:.2f}"
        except ValueError:
            adjusted_data[nutrient] = value  # Keep the original if conversion fails
    
    return adjusted_data

# Function to rate the healthiness of the product
def rate_healthiness(nutritional_data, serving_size, reference_grams):
    # Adjust the nutritional values based on the serving size and reference scale
    adjusted_data = adjust_nutritional_values(nutritional_data, reference_grams, serving_size)
    
    # Format the adjusted nutritional data into a string for the prompt
    formatted_data = ', '.join([f"{key}: {value}" for key, value in adjusted_data.items()])
    
    # Create the prompt to rate the healthiness
    prompt = f"The nutritional data for this product is as follows: {formatted_data}. The serving size is {serving_size} grams. Rate how healthy this product is from 1 to 5, where 1 means least healthy and 5 means healthiest."
    
    # Send the data to OpenAI API and get the health rating
    response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    
    # Extract and return the health rating
    health_rating = response.choices[0]['message']['content'].strip()
    return health_rating

# Function to get detailed analysis from OpenAI
def get_detailed_analysis(nutritional_data, serving_size, reference_grams):
    # Adjust the nutritional values based on the serving size and reference scale
    adjusted_data = adjust_nutritional_values(nutritional_data, reference_grams, serving_size)
    
    # Format the adjusted nutritional data into a string for the prompt
    formatted_data = ', '.join([f"{key}: {value}" for key, value in adjusted_data.items()])
    
    # Send a prompt for a detailed analysis to OpenAI
    prompt = f"Provide a brief analysis of the product's nutritional content: {formatted_data}. Mention harmful nutrients like trans fat."
    
    # Request detailed analysis
    response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    
    # Extract and return the detailed analysis
    detailed_analysis = response.choices[0]['message']['content'].strip()
    return detailed_analysis

# Example Nutritional Data (e.g., per 100g)
nutritional_data = {
    "Energy": "539kcal",
    "Protein": "6.8g",
    "Carbohydrates": "53.7g",
    "Total Sugars": "2.7g",
    "Added Sugars": "1.4g",
    "Total Fat": "33.0g",
    "Saturated Fat": "14.7g",
    "Trans Fat": "0.1g",
    "Sodium": "678mg"
}

# Reference grams (e.g., per 100g in the nutritional data)
reference_grams = 100  # Nutritional data given for per 100 grams

# Example serving size (user-specific)
serving_size = 20  # Example serving size in grams (this could be dynamic)

# Step 1: Get the health rating
health_rating = rate_healthiness(nutritional_data, serving_size, reference_grams)
print(f"Health Rating: {health_rating}")

# Step 2: Ask the user if they want detailed analysis
user_response = input("Do you want the detailed analysis of this product? (yes/no): ").strip().lower()
if user_response == 'yes':
    detailed_analysis = get_detailed_analysis(nutritional_data, serving_size, reference_grams)
    print(f"Detailed Analysis: {detailed_analysis}")
else:
    print("Ending the program.")