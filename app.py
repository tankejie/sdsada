from flask import Flask, request, jsonify, render_template
import numpy as np
#import pickle
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    Length = request.form.get('length')
    Diameter = request.form.get('diameter')
    Height = request.form.get('height')
        
    #output = round(prediction[0], 2)    
   
    ####################### FROM AUTOAI DEPLOYMENT API #######################
    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "ieLUV0Cb-QOgcFR_1tkB6KX6M9NU_Y-zAiP8yyVJRU2Q"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
     API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    #LoanDuration = input('Enter Loan Duration')
    #LoanAmount = input('Enter Loan Amount')
    #Age = input('Enter Age')

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [
                    "Sex",
                    "Length",
                    "Diameter",
                    "Height",
                    "Whole weight",
                    "Shucked weight",
                    "Viscera weight",
                    "Shell weight",
                    "Rings"],                 
        "values": [[

                    None,
                    Length,
                    Diameter,
                    Height,
                    None,
                    None,
                    None,
                    None,
                    None]]
        }]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/c258bae8-1c4e-4341-9462-9f2548c369e1/predictions?version=2022-07-07', json=payload_scoring,
                                     headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    ####################### END OF AUTOAI DEPLOYMENT API #######################

    return render_template('index.html', prediction_text='Loan Risk Prediction is $ {}'.format(response_scoring.json()))

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=8080)
    app.run()