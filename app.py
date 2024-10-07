from flask import Flask, render_template, request
import google.generativeai as genai  
import os
from PIL import Image
import io

app = Flask(__name__)

model = genai.GenerativeModel("gemini-1.5-flash")
api = os.getenv("GEMINI")
genai.configure(api_key=api) 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get the selected values from the form
    property_type = request.form.get('propertyType')
    location = request.form.get('location')
    rooms = request.form.get('rooms')

    # Calculate the estimated rent based on selections
    base_price = 1000
    property_type_factor = {'HDB': 1.0, 'Condo': 1.5, 'Landed': 2.0}.get(property_type, 1.0)
    location_factor = {'Bedok': 1.1, 'Tampines': 1.3, 'Jurong': 1.5}.get(location, 1.0)
    rooms_factor = {'1R': 0.8, '2R': 1.0, '3R': 1.2, '4R': 1.5}.get(rooms, 1.0)

    estimated_rent = base_price * property_type_factor * location_factor * rooms_factor

    return render_template('predict_rent_result.html', rent=estimated_rent)

@app.route("/search_properties", methods=["POST"])
def search_properties():
    return render_template("search_property_result.html")
 
@app.route("/check_scam_result", methods=["POST"])
def check_scam_result():
    if 'image' not in request.files:
        return "No file part", 400

    file = request.files['image']

    if file.filename == '':
        return "No selected file", 400

    if file:
        try:
            # Open the image file using PIL (Python Imaging Library)
            image = Image.open(file.stream)

            # Generate a prompt for the model analysis
            prompt = "Analyze this image of a property advertisement and rate its legitimacy on a scale from 1 to 10."
            
            # Convert the image to the required format for the generative model
            # Use the `Image` object directly instead of BytesIO
            response = model.generate_content([image, prompt])  # Adjust this as necessary

            result = response.text if response else "Unable to analyze the image at this time."
        except Exception as e:
            result = f"An error occurred: {str(e)}"

    return render_template("check_scam_result.html", r=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
