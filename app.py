import numpy as np
from flask import Flask, request, jsonify, render_template
import dill

app = Flask(__name__)
model = dill.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    user_input = [x for x in request.form.values()][0]

    prediction = model(user_input)
    #prediction = [x for x in request.form.values()]

    return render_template('index.html', prediction_text='Predicted NAICS code for "{}" is {}'.format(user_input.upper(),prediction))

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model(data.values())

    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug=True)