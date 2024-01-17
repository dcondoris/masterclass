import requests

IP_ADDRESS= "63.34.168.100"

url = 'http://{IP_ADDRESS}:5001/invocations'
myobj ={
  "dataframe_records": [{
    "satisfaction_level":0.61,
    "last_evaluation":0.6,
    "number_projects":2.0,
    "average_monthly_hours":152.3,
    "time_spend_company":2.0,
    "work_accident":0.0,
    "promotion_last_5_years":0.0,
    "position":"technical",
    "salary":2
}]}

x = requests.post(url, json = myobj)

print(x.text)