from os import path, getenv

import boto3
from joblib import load
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

LOCAL_BASE_PATH = getenv('BASE_PATH')
REMOTE_TRAINED_PATH = getenv('REMOTE_TRAINED_PATH')
REMOTE_MODEL_PATH = getenv('REMOTE_MODEL_PATH')
BUCKET_STORAGE = getenv('BUCKET_STORAGE')
LOCAL_PATH_FEATURES = path.join(LOCAL_BASE_PATH,
                       'trained_model.parquet')
LOCAL_PATH_MODEL = path.join(LOCAL_BASE_PATH,
                       'model_risk.joblib')

@app.route('/_health')
def serverHealth():
    return jsonify('Server is happy :)')



@app.route('/predictionClient/<client_id>')
def client_id_search(client_id):
    s3 = boto3.resource('s3')
    s3.Object(BUCKET_STORAGE, REMOTE_TRAINED_PATH).download_file(LOCAL_PATH_FEATURES)
    s3.Object(BUCKET_STORAGE, REMOTE_MODEL_PATH).download_file(LOCAL_PATH_MODEL)
    df = pd.read_parquet(LOCAL_PATH_FEATURES)
    my_model = load('model_risk.joblib') 
    data = df[df.id==client_id].drop(columns=['id'])
    response = my_model.predict([data.iloc[-1]])
    return jsonify(int(response[0]))



if __name__ == '__main__':
    app.run(debug=True)