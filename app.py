from flask import Flask, render_template, request
import google.generativeai as genai  
import os
import requests

model = genai.GenerativeModel("gemini-1.5-flash")
api = os.getenv("GEMINI")
genai.configure(api_key=api) 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get the selected values from the form
    property_type = request.form.get('propertyType')
    location = request.form.get('location')
    rooms = request.form.get('rooms')

    # Perform calculation or any logic based on the dropdown selections
    # For example, calculating a hypothetical rental price based on inputs
    base_price = 1000
    property_type_factor = {'HDB': 1.0, 'Condo': 1.5, 'Landed': 2.0}.get(property_type, 1.0)
    location_factor = {'Bedok': 1.1, 'Tampines': 1.3, 'Jurong': 1.5}.get(location, 1.0)
    rooms_factor = {'1R': 0.8, '2R': 1.0, '3R': 1.2, '4R': 1.5}.get(rooms, 1.0)

    # Calculate the estimated rent
    estimated_rent = base_price * property_type_factor * location_factor * rooms_factor

    return render_template('predict_rent_result.html', rent=estimated_rent)

@app.route("/search_properties",methods=["POST"])
def search_properties():
    return(render_template("search_property_result.html"))

@app.route("/check_scam",methods=["POST"])
def check_scam():
    return(render_template("check_scam_result.html"))

@app.route("/check_scam_result",methods=["GET","POST"])
#Send URL to Gemini for scam detection
def check_scam_result():    
# Create a prompt to check if the URL is a scam"
    url =request.form.get("url") 
    prompt = f"Rate on a scale of 1-10 if this advertisement is likely a scam : {url}"
    r= model.generate_content(prompt)
    return(render_template("check_scam_result.html",r=r)) #synchronise front and back-end.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
