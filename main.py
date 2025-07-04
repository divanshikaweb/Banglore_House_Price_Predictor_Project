import json
import pickle
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

model = pickle.load(open("banglore_home_prices_model.pickle", 'rb'))

with open("columns.json", "r") as f:
    data_columns = json.load(f)['data_columns']

# Extract location names
locations = data_columns[3:]  # first 3 are: total_sqft, bath, bhk

@app.route('/')
def index():
    return render_template('try.html', locations=locations)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        location = request.form.get('location')
        bhk = int(request.form.get('bhk'))
        bath = int(request.form.get('bathroom'))
        sqft = float(request.form.get('total_sqft'))
        
        if not all([location, bhk, bath, sqft]):
            return "Missing parameters", 400
            
        # Create input vector
        x = np.zeros(len(data_columns))
        x[0] = sqft
        x[1] = bath
        x[2] = bhk
        
        if location in data_columns:
            loc_index = data_columns.index(location)
            x[loc_index] = 1
        else:
            return "Invalid location", 400
            
        prediction = model.predict([x])[0] * 1e5
        return str(np.round(prediction, 2))
        
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
