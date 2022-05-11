# pip install fastapi uvicorn pandas lightgbm
# conda create -- myenv python=3.6
# conda activate myenv

#from fastapi import FastAPI
#from pydantic import BaseModel
from flask import Flask , jsonify 
#import pickle
import joblib as jb 
import pandas as pd 



app = FastAPI()
X_test = pd.read_csv('X_test.csv')
loaded_model = jb.load('best_model.joblib', 'r')
#with open('LGBmodele.pkl','rb') as file:
 # loaded_model = pickle.load(file)
#class Client(BaseModel):    # maper la réalité 
 # index : float   # ça peut être le nu du client  
# uvicorn app:app --reload
@app.route('/predict', methods =["POST"] )
def predict_var():
  data = request.get_json() 
  #data = client.dict()
  #print(data)
  id_client = int(data['index'])
  #id_client = 2
  prediction = loaded_model.predict(X_test.iloc[[id_client]])
  probability = loaded_model.predict_proba(X_test.iloc[[id_client]]).max()
  return jsonify({
    'prediction': str(prediction[0]),
    'probability': probability
    } )