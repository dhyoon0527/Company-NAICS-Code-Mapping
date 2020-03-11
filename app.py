import numpy as np
from flask import Flask, request, jsonify, render_template
import dill

app = Flask(__name__)
model = dill.loads(model)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    #nt_features = [int(x) for x in request.form.values()]
    #inal_features = [np.array(int_features)]

    prediction = model(request.form.values())

    return render_template('index.html', prediction_text='Predicted NAICS code is $ {}'.format(prediction))

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model(data.values())

    #output = prediction[0]
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug=True)