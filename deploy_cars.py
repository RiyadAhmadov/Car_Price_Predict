import uvicorn
from fastapi import FastAPI, Query
import pickle
import pandas as pd
import warnings
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# Create a FastAPI app instance
app = FastAPI()


# Load the pickled model using a relative file path
with open('model_car.pkl', "rb") as model_file:
    model = pickle.load(model_file)


html_content = """
<!DOCTYPE html>
<html>
<style>
    #buy-button {
        font-size: 20px;
        padding: 10px 20px;
        margin: 5px;
        background-color: #28a745; /* Green color for Buy button */
        color: #fff; /* Text color for Buy button */
        border: none; /* Remove button border */
        cursor: pointer;
    }

    #cancel-button {
        font-size: 20px;
        padding: 10px 20px;
        margin: 5px;
        background-color: #dc3545; /* Red color for Cancel button */
        color: #fff; /* Text color for Cancel button */
        border: none; /* Remove button border */
        cursor: pointer;
    }
    
    #next-button {
        font-size: 20px;
        padding: 10px 20px;
        margin: 5px;
        background-color: #007bff; /* Red color for Cancel button */
        color: #fff; /* Text color for Cancel button */
        border: none; /* Remove button border */
        cursor: pointer;
    }


    body {
        background-image: url(https://s1.cdn.autoevolution.com/images/gallery/MERCEDES-BENZ-E-63-AMG--W212--4712_26.jpg);
        background-size: cover;
        text-align: center; /* Center-align text within the body */
        background-size: cover;
        text-align: center; /* Center-align text within the body */
        height: 100%; /* Set height to 100% for the background to cover the entire viewport */
    }

    }
    
    form {
        text-align: left;
    }
    
    select {
    font-size: 16px; 
    width: 102.4%; 
    box-sizing: border-box; 
    padding: 8px; 
    }
    h1 {
        font-size: 28px; /* Change the font size for the heading */
        color: #333; /* Change the text color for the heading */
        font-family: "Verdana", sans-serif;
    }

    label {
        font-size: 18px; /* Change the font size for labels */
        color: #555; /* Change the text color for labels */
    }

    input {
        font-size: 16px; /* Change the font size for input fields */
        padding: 5px; /* Add padding to input fields */
        margin: 5px 0; /* Add margin to input fields */
        width: 100%; /* Make input fields 100% width of their container */
        font-family: "Verdana", sans-serif;
    }

    input[type="submit"] {
        background-color: #007BFF; /* Change the background color for the submit button */
        color: #fff; /* Change the text color for the submit button */
        font-size: 18px; /* Change the font size for the submit button */
        padding: 10px 20px; /* Add padding to the submit button */
        cursor: pointer;
        font-family: "Verdana", sans-serif;
    }

    input[type="submit"]:hover {
        background-color: #0056b3; /* Change the background color on hover */
    }


    .header {
        background-color: rgba(255, 255, 255, 0.5);
        padding: 2px;
        border: 10px solid rgba(255, 255, 255, 0.5);
    }

    .form-container {
        background-color: rgba(255, 255, 255, 0.7);
        padding: 20px;
        margin: 20px auto; /* Add margin to create space */
        width: 50%;
        border-radius: 10px;
    }
    .header h1 
    {
        color: black; /* Set text color to white */
        font-size: 30px;
        font-family: "Verdana", sans-serif;
    }

    h2 {
        font-size: 20px; /* Change the font size for the result heading */
        color: #333; /* Change the text color for the result heading */
        font-family: "Verdana", sans-serif;
    }

    p {
        font-size: 18px; /* Change the font size for the result text */
        color: #333; /* Change the text color for the result text */
        font-family: "Verdana", sans-serif;
    }
</style>
<head>
    <title>Airport Customer Satisfaction Prediction</title>
</head>
<body>
    <div class="header">
        <img src="https://s.tmimgcdn.com/scr/400x250/172200/red-automotive-logo-template_172217-2-original.png" alt="Car Sales Site Logo" style="width: 400px; height: 280px; margin-top: -70px; margin-bottom: -70px">
        <h1>Car Sales Prediction</h1>
    </div>
    <div class="form-container">
    <h1>Car Price Prediction</h1>
      <form id="prediction-form">
      
        <label for="Title">What is Title?</label>
        <input type="text" id="Title" name="Title" required><br>
         
        <label for="Year">In which year was the car manufactured?</label>
        <select id="Year" name="Year" required></select><br>

        <label for="UsedOrNew">Is the car used or new?</label>
            <select id="UsedOrNew" name="UsedOrNew" required>
                <option value="DEMO">DEMA</option>
                <option value="USED">USED</option>
                <option value="NEW">NEW</option>
            </select><br>

        <label for="Transmission">What type of transmission does the car have (e.g., automatic, manual)?</label>
            <select id="Transmission" name="Transmission" required>
                <option value="Automatic">Automatic</option>
                <option value="Manual">Manual</option>
            </select><br>

        <label for="Engine">Describe the engine of the car.</label>
        <input type="float" id="Engine" name="Engine" required><br>

        <label for="DriveType">What is the drive type of the car (e.g., front-wheel drive, rear-wheel drive)?</label>
            <select id="DriveType" name="DriveType" required>
                <option value="AWD">AWD</option>
                <option value="Front">Front</option>
                <option value="Rear">Rear</option>
                <option value="Other">Other</option>
                <option value="4WD">4WD</option>
            </select><br>

        <label for="FuelType">What type of fuel does the car use?</label>
        <select id="FuelType" name="FuelType" required>
            <option value="Diesel">Diesel</option>
            <option value="Premium">Premium</option>
            <option value="Unleaded">Unleaded</option>
            <option value="Hybrid">Hybrid</option>
            <option value="Other">Other</option>
            <option value="Electric">Electric</option>
            <option value="LPG">LPG</option>
            <option value="Leaded">Leaded</option>
        </select><br>

        <label for="FuelConsumption">What is the fuel consumption of the car?</label>
        <input type="text" id="FuelConsumption" name="FuelConsumption" required><br>

        <label for="Kilometres">How many kilometers has the car been driven?</label>
        <input type="number" id="Kilometres" name="Kilometres" required><br>

        <label for="ColourExtInt">What is the internal/external color of the car?</label>
        <input type="text" id="ColourExtInt" name="ColourExtInt" required><br>

        <label for="Location">Where is the car located?</label>
        <select id="Location" name="Location" required>
            <option value="NT">NT</option>
            <option value="TAS">TAS</option>
            <option value="WA">WA</option>
            <option value="NSW">NSW</option>
            <option value="VIC">VIC</option>
            <option value="ACT">ACT</option>
            <option value="QLD">QLD</option>
            <option value="SA">SA</option>
            <option value="AU-VIC">AU-VIC</option>
        </select><br>

        <label for="CylindersinEngine">How many cylinders are there in the engine?</label>
        <input type="float" id="CylindersinEngine" name="CylindersinEngine" required><br>

        <label for="BodyType">What is the body type of the car?</label>
        <select id="BodyType" name="BodyType" required>
            <option value="SUV">SUV</option>
            <option value="Hatchback">Hatchback</option>
            <option value="Coupe">Coupe</option>
            <option value="Commercial">Commercial</option>
            <option value="Wagon">Wagon</option>
            <option value="Ute / Tray">Ute/Tray</option>
            <option value="Sedan">Sedan</option>
            <option value="People Mover">People Mover</option>
            <option value="Convertible">Convertible</option>
            <option value="Other">Other</option>
        </select><br>

        <label for="Doors">How many doors does the car have?</label>
        <input type="number" id="Doors" name="Doors" required><br>

        <label for="Seats">How many seats does the car have?</label>
        <input type="number" id="Seats" name="Seats" required><br>

        <input type="submit" value="Predict Car Price">
    </form>
    <h2>Prediction Result:</h2>
    <p id="prediction_result"></p>
        <div id="result-container" style="display: none;">
            <p id="prediction_result"></p>
            <button id="buy-button">Buy</button>
            <button id="cancel-button">Cancel</button>
            <button id="next-button">Again</button>
            <p id="purchase-result"></p>
        </div>
    </div>
<script>
    const form = document.getElementById('prediction-form');
    const yearSelect = document.getElementById('Year');
    const predictionResult = document.getElementById('prediction_result');
    const resultContainer = document.getElementById('result-container');
    const buyButton = document.getElementById('buy-button');
    const cancelButton = document.getElementById('cancel-button');
    const nextButton = document.getElementById('next-button');
    const purchaseResult = document.getElementById('purchase-result');

    const years = [2022, 2011, 2004, 2017, 2000, 2013, 2014, 2009, 2018, 2015, 2016, 2012, 2023,
                2005, 2019, 2021, 2007, 2010, 2003, 2008, 2006, 2020, 1999, 2002, 1995, 1997,
                1993, 2001, 1998, 1985, 1992, 1986, 1996, 1994, 1989, 1990, 1981, 1991, 1959,
                1970, 1984, 1975, 1979, 1978, 1940];

    years.forEach(year => {
        const option = new Option(year, year);
        yearSelect.add(option);
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(form);

        // Convert string values to numbers for 'Engine' and 'FuelConsumption'
        formData.set('Engine', parseFloat(formData.get('Engine')));
        formData.set('FuelConsumption', parseFloat(formData.get('FuelConsumption')));

        // Replace the fetch URL with your actual server endpoint
        const response = await fetch('/predict/?' + new URLSearchParams(formData).toString());
        const data = await response.json();

        predictionResult.textContent = data['prediction'];

        // Show the result container
        resultContainer.style.display = 'block';
    });

    buyButton.addEventListener('click', () => {
        purchaseResult.textContent = 'Thank you for your purchase!';
    });

    cancelButton.addEventListener('click', () => {
        purchaseResult.textContent = 'Bad choice! Better luck next time.';
    });

    nextButton.addEventListener('click', () => {
        location.reload();
    });
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def serve_html():
    return HTMLResponse(content=html_content)


# Define the endpoint to make predictions
@app.get("/predict/")
async def predict(
    Year: int = Query(..., description="Year"),
    Title: str = Query(..., description="Title"),
    UsedOrNew: str = Query(..., description="Used or New"),
    Transmission: str = Query(..., description="Transmission"),
    Engine: float = Query(..., description="Engine"),
    DriveType: str = Query(..., description="Drive Type"),
    FuelType: str = Query(..., description="Fuel Type"),
    FuelConsumption: str = Query(..., description="Fuel Consumption"),
    Kilometres: int = Query(..., description="Kilometres"),
    ColourExtInt: str = Query(..., description="Colour External/Internal"),
    Location: str = Query(..., description="Location"),
    CylindersinEngine: float = Query(..., description="Cylinders in Engine"),
    BodyType: str = Query(..., description="Body Type"),
    Doors: int = Query(..., description="Doors"),
    Seats: int = Query(..., description="Seats")
):
    # Create a DataFrame from the input data
    data = pd.DataFrame({
        'Year': [Year],
        'Title': [Title],
        'UsedOrNew': [UsedOrNew],
        'Transmission': [Transmission],
        'Engine': [Engine],
        'DriveType': [DriveType],
        'FuelType': [FuelType],
        'FuelConsumption': [FuelConsumption],
        'Kilometres': [Kilometres],
        'ColourExtInt': [ColourExtInt],
        'Location': [Location],
        'CylindersinEngine': [CylindersinEngine],
        'BodyType': [BodyType],
        'Doors': [Doors],
        'Seats': [Seats]
    })


    print(data)

    # Edit new columns    
    data['Engine'] = data['Engine'].astype(float)
    
    data['CylindersinEngine'] = data['CylindersinEngine'].astype(float)
    
    data['Doors'] = data['Doors'].astype(int)
    data['Seats'] = data['Seats'].astype(int)
    
    data['FuelConsumption'] = data['FuelConsumption'].astype(float)
    
    # Location
    data['Location'] = data['Location'].str.split(', ').str[1]
    my_dict = {'NT': 8,
    'TAS': 7,
    'WA': 6,
    'NSW': 5,
    'VIC': 4,
    'ACT': 3,
    'QLD': 2,
    'SA': 1,
    'AU-VIC': 0}
    data['Location'] = data['Location'].map(my_dict)
    data['Location'] =  data['Location'].astype(float)

    # Body type
    my_dict_body = {'Commercial': 0,
    'Convertible': 1,
    'Coupe': 2,
    'Hatchback': 3,
    'Other': 4,
    'People Mover': 5,
    'SUV': 6,
    'Sedan': 7,
    'Ute / Tray': 8,
    'Wagon': 9}
    data['BodyType'] = data['BodyType'].map(my_dict_body)
    #----------------------------------------------------
    
    # Fuel Type 
    my_dict_fuel = {'Diesel': 1,
    'Electric': 2,
    'Hybrid': 3,
    'LPG': 4,
    'Leaded': 5,
    'Other': 6,
    'Premium': 7,
    'Unleaded': 8}
    data['FuelType'] = data['FuelType'].map(my_dict_fuel)
    #----------------------------------------------------

    # Drive Type 
    my_dict_dtype = {'4WD': 0, 'AWD': 1, 'Front': 2, 'Other': 3, 'Rear': 4}
    data['DriveType'] = data['DriveType'].map(my_dict_dtype)
    #----------------------------------------------------
    
    # Transmission 
    my_dict_trans = {'Automatic': 1, 'Manual': 2}
    data['Transmission'] = data['Transmission'].map(my_dict_trans)
    #----------------------------------------------------

    # UsedOrNew 
    my_dict_used = {'DEMO': 0, 'NEW': 1, 'USED': 2}
    data['UsedOrNew'] = data['UsedOrNew'].map(my_dict_used)
    #----------------------------------------------------

    # Year 
    my_dict_year = {1940: 0,
  1959: 1,
  1970: 2,
  1975: 3,
  1978: 4,
  1979: 5,
  1981: 6,
  1984: 7,
  1985: 8,
  1986: 9,
  1989: 10,
  1990: 11,
  1991: 12,
  1992: 13,
  1993: 14,
  1994: 15,
  1995: 16,
  1996: 17,
  1997: 18,
  1998: 19,
  1999: 20,
  2000: 21,
  2001: 22,
  2002: 23,
  2003: 24,
  2004: 25,
  2005: 26,
  2006: 27,
  2007: 28,
  2008: 29,
  2009: 30,
  2010: 31,
  2011: 32,
  2012: 33,
  2013: 34,
  2014: 35,
  2015: 36,
  2016: 37,
  2017: 38,
  2018: 39,
  2019: 40,
  2020: 41,
  2021: 42,
  2022: 43,
  2023: 44}
    data['Year'] = data['Year'].map(my_dict_year)
    #----------------------------------------------------
    print(data)

    # Make predictions using the pre-trained model
    Price = model.predict(data[['Year', 'UsedOrNew', 'Transmission',
       'Engine', 'DriveType', 'FuelType', 'FuelConsumption', 'Kilometres',
       'Location', 'CylindersinEngine', 'BodyType', 'Doors', 'Seats']])
    Price1 = str(round(Price[0],2)) + 'USD'
    Price_man = str(round(float(Price[0])*(float(1.7)),2)) + 'MAN'

    # You can use these parameters as input for your model and return the prediction result
    prediction_result = f"Price is for searching car : {Price1} -- (AZ): {Price_man}"
    return {"prediction": prediction_result}


# Run the FastAPI app using Uvicorn
if __name__ == '__main__':
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=5002,
        log_level="debug",
    )
