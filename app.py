# pip install fastapi uvicorn pandas lightgbm
# conda create -- myenv python=3.6
# conda activate myenv

from fastapi import FastAPI
from pydantic import BaseModel
#import pickle
import joblib as jb 
import pandas as pd 
from sklearn.linear_model import LogisticRegression


app = FastAPI()
X_test = pd.read_csv('X_test.csv')
loaded_model = jb.load('best_model.joblib', 'r')
#with open('LGBmodele.pkl','rb') as file:
 # loaded_model = pickle.load(file)
class Client(BaseModel):    # maper la réalité 
  index : float   # ça peut être le nu du client  
# uvicorn app:app --reload
@app.post('/predict')
async def predict_var(client : Client):
  #data = client.dict()
  #print(data)
  #id_client = int(data['index'])
  id_client = 2
  prediction = loaded_model.predict(X_test.iloc[[id_client]])
  probability = loaded_model.predict_proba(X_test.iloc[[id_client]]).max()
  return {
    'prediction': str(prediction[0]),
    'probability': probability
    }  