from django.shortcuts import render
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

# Create your views here.

def classify(request):
  if request.POST:
    amount = request.POST['Amount']
    user_id = request.POST['User_ID']
    ip = request.POST['IP_Address']
    product = request.POST['Product_Name']

    df = pd.read_csv(rf'C:\Users\Ilay2\django\fraud_detector\samsung_tech.csv')

    users = df.groupby('UserID')
    unique_ips = users['IP_Address'].nunique()
    amount_spent = users['Amount'].sum()

    # Add new entry to data frame

    df['Unique_Ips'] = df['UserID'].map(unique_ips)
    df['Total_Amount'] = df['UserID'].map(amount_spent)

    # Grab row out of the model with it's new rows:
    # unique ips
    # toatl amount
    
    X = df[['Unique_Ips', 'Total_Amount']]

    # Import model from local files
    # Run the model on new data point, XGBoost has a parameter that allows us to get a score, rather than true false
    # return the model result inside a context variable 


def trainer():
  df = pd.read_csv(rf'C:\Users\Ilay2\django\fraud_detector\samsung_tech.csv')

  # Group by specific users
  # Fetch number unique IP addresses thru agrregating rows with unique IPS
  # Sum their amount spent
  # Append columns to corresponding rows in the dataframe
 
  users = df.groupby('UserID')
  
  unique_ips = users['IP_Address'].nunique()
  amount_spent = users['Amount'].sum()

  df['Unique_Ips'] = df['UserID'].map(unique_ips)
  df['Total_Amount'] = df['UserID'].map(amount_spent)

  df['Fraud'] = df['Unique_Ips'] > 2
  
  X = df[['Unique_Ips', 'Total_Amount']]
  y = df['Fraud']

  x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2
  )

  model = XGBClassifier()
  model.fit(x_train, y_train)

  y_pred = model.predict(x_test)

  accuracy = accuracy_score(y_test, y_pred)
  print("Accuracy after training is: ", accuracy)
  
  model.save_model('fraud_classifier.json')

  
  # Read columns
 