import pandas as pd 
import streamlit as st 
import requests as req 
import joblib 
import numpy as np
import streamlit.components.v1 as components
X_test = pd.read_csv("X_test.csv")
list_explain = joblib.load("list_exp.joblib")
X_test['AGE'] = X_test['DAYS_BIRTH'] / -365
#option = st.selectbox( " veuillez choisir un client", list(X_test.index))
#st.write(str(option))
#url = "http://elmaha269.pythonanywhere.com/predict"
#data = {"index":option}
#reponse = req.post(url=url, json = data)
#st.write(reponse.text)
# streamlit run dashboard.py st.latex ou st.markdown


#from urllib.request import urlopen 
#import json
#X_test = pd.read_csv("X_test.csv")

#affichage du tableau de board
st.title('Dashboard Credit Scoring')
st.subheader("Prédictions de scoring client")
list_id = list(X_test.index)
id_client = st.text_input("Veuillez choisir un client",)
#option = st.selectbox("Veuillez choisir un client", list(X_test.index))
#st.write(str(option))

#Appel de l'API

if id_client == '':  #lorsque rien n'a été saisi
    st.write('Exemples id_client : 12, 8957, 3692, 89')

elif(int(id_client) in list_id):

    #APP_url = "http://elmaha269.pythonanywhere.com/predict" + id_client
    APP_url = "http://elmaha269.pythonanywhere.com/predict"
    st.title('Information du client')
    st.dataframe(X_test.loc[int(id_client)])

    with st.spinner("Chargement du score du client..."):
        APP_data = {"index":id_client}
        json_reponse = req.post(url = APP_url, json = APP_data).json()

        #APP_data = json.load(json_url.read())
        
        prediction= int(json_reponse['prediction'])
        probability = json_reponse['probability'] 
        def etat_client(pred):
            switch = {
                1: 'La prédiction du client par rapport au crédit est de ' "" + str(prediction)+ '(non accordé) :' +" " 'Client à risque  d\'une approximation de ' + str(round(probability*100))+'%' + " " 'de risque de défaut.',
                0: 'La prédiction du client par rapport au crédit est de ' "" + str(prediction)+ '(accordé) :' +" " 'Client peu de risque  d\'une approximation de ' + str(round(100 - probability*100))+'%' + " " 'de risque de défaut.'
            }
            return switch.get(pred)

    
        message = etat_client(prediction)

        st.markdown(message)
        components.html(list_explain[int(id_client)].as_html(),height = 500)
        i_n = np.where(X_test.index== int(id_client))[0][0]
        st.bar_chart(X_test.iloc[i_n:i_n+19][['AGE']])
        st.bar_chart(X_test.iloc[i_n:i_n+19][['DAYS_EMPLOYED']])
        st.bar_chart(X_test.iloc[i_n:i_n+19][['CC_AMT_BALANCE_MEAN']])
        
        
else: 
    st.write('Identifiant non reconnu')