import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('pickles/model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    user_input = [x for x in request.form.values()][0]
    prediction = model(user_input)

    return render_template('index.html', prediction_text='Predicted NAICS code for "{}" is {}'.format(user_input.upper(),prediction))

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model(str(data.values()))

    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug=True)