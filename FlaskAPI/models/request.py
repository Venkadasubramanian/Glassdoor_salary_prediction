
import requests
from data_input import data_input

URL = "http://127.0.0.1:5000/predict"
headers = {"content-Type" : "application/json"}
data = {'input':data_input}

r = requests.get(URL,headers=headers,json=data)

r.json()