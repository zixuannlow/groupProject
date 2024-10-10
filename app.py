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
    hdb = 0
    condo = 0
    landed = 0

    property_type = request.form.get('propertyType') 
    if property_type == "HDB": 
        hdb= 1
    elif property_type == "Condo": 
        condo = 1
    elif property_type == "Landed": 
        landed = 1
     
    #to be amended
    region = request.form.get('location')
     
    encodeRegion = 0
    if region == "North": 
        encodeRegion= 1
    elif property_type == "West": 
        encodeRegion = 2
    elif property_type == "East": 
        encodeRegion = 3
    elif property_type == "South": 
        encodeRegion = 4
      
    rooms = request.form.get('rooms')
    numOfRooms = int(rooms[:1])
  
    rent = 1628.84 + 55.96*(encodeRegion) + 1251.01*(numOfRooms) - 56.69*(condo) - 84.34*(hdb) + 141.03*(landed)  
    rentString = "%.2f" % rent
    resultArr = [region, rooms ,property_type,rentString]
    return render_template('predict_rent_result.html', r=resultArr)

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
            prompt = "Analyze if this advertisement is about renting/selling of property. If yes, rate its legitimacy on a scale from 1 to 10."
            
            # Convert the image to the required format for the generative model
            # Use the `Image` object directly instead of BytesIO
            response = model.generate_content([image, prompt])  # Adjust this as necessary

            result = response.text if response else "Unable to analyze the image at this time."
        except Exception as e:
            result = f"An error occurred: {str(e)}"

    return render_template("check_scam_result.html", r=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
