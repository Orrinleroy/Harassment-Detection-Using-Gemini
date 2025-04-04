from config import genai
import base64

def encode_image(image_path):

    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def analyze_image(image_path):

    image_data = encode_image(image_path)
    model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")

    response = model.generate_content([
        "Analyze this image. Does it contain harassment, violence, or suspicious activity?",
        image_data
    ])
    
    return response.text  # Returns Gemini’s response

# Example usage
if __name__ == "__main__":
    test_image = "static/test_image.jpg"
    result = analyze_image(test_image)
    print("Gemini Response:", result)
