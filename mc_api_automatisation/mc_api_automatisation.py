# Importer les bibliothèques nécessaires
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

MY_KEY = "moby_jhLrd98tuuqPZI3iioZZQkzVvAy"
# Définir les arguments par défaut pour le DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 4, 27),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
# Initialiser le DAG
dag = DAG(
    dag_id='masterclass_api_dag',
    default_args=default_args,
    description='Un exemple de DAG Airflow',
    tags=['masterclass', 'datascientest'],
    schedule_interval=timedelta(days=1),
)


def get_data(API_KEY):
        
    # Define the API URL and parameters
    url = 'https://api.mobygames.com/v1/games'
    params = {
        'format': 'normal',
        'api_key': API_KEY,
        'limit': 100
    }

    # Initialize an empty list to store the data
    data = []

    # Loop over the API results and append to the data list
    for offset in range(0, 1000, 100):
        params['offset'] = offset
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data += response.json()['games']
        time.sleep(1)
    now = datetime.now().isoformat()
    filename = f"{now}.json"
    file_path = f"/app/raw_files/{filename}"
    with open(file_path, 'w') as f:
        json.dump(data, f)


def transform_one_element(game:dict)-> dict:
    """Extract sub keys from the json file containing data about a game"""
    dict1 ={'description': game['description'], 
                'title':game['title'],
                'game_id':game['game_id'],
                'genre' : ','.join([ g['genre_category'] for g in game['genres'] ])}
        
    dict2 = { 'release_date'+p['platform_name'] : p['first_release_date']
            for p in game['platforms']
            }
    dict1.update(dict2)
    return dict1

def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text(separator=" ")
    return stripped_text              

def transform_data(sourcefile,filename):
    """
    transforming raw json files with unstructured data into a clean and ready to use dataframe
    """
    # Load the data from the JSON file
    with open(sourcefile, 'r') as f:
        data = json.load(f)
    transfo_data=[ transform_one_element(game) for game in data]
    df = pd.DataFrame(transfo_data)
    #removing html tags
    df["description"] = df["description"].apply(remove_html_tags)
    #removing platform with less than 15% Non NAN values for the release_date
    df = df.dropna(axis=1,thresh=int(df.shape[0]*0.15))
    #Saving the dataframe as csv file
    df.to_csv( filename, index=False)


# Define the task that calls the get_data function
collect_data_task = PythonOperator(
    task_id='get_data',
    python_callable=get_data,
    op_kwargs={'API_KEY': MY_KEY},
    dag=dag,
)


transform_data_task  = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    op_kwargs={'sourcefile': 'data.json',
    'filename' :'dataset_mobigames.csv'},
    dag=dag
)


# Set the order of the tasks in the DAG
collect_data_task >> transform_data_task


################################################################################################
##Idée à creuser :
##Scrapper ou trouver API comme metacritic ou steam pour avoir des notes

##Modele analyses de sentiments ou embedding et faire du ML 

#twitter API pour connaitre dernières tendances ?

#Se conenecter à une base de données/cloud ?
def load_data():
    # Load the transformed data from the CSV file
    with open('/path/to/transformed_data.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader) # skip header row
        transformed_data = [row for row in reader]
    
    # Save the transformed data to a database
    conn = psycopg2.connect(
        host='your_host',
        port='your_port',
        dbname='your_dbname',
        user='your_username',
        password='your_password'
    )
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS my_table (title text, year integer, genre text)')
    cur.executemany('INSERT INTO my_table (title, year, genre) VALUES (%s, %s, %s)', transformed_data)
    conn.commit()
    cur.close()
    conn.close()
##Envoyer des mails si échoue
def send_email_failure():
    # Send an e-mail notification if any task in the DAG fails
    subject = 'DAG execution failed'
    body = 'One or more tasks in the DAG failed to execute. Please check the logs for more information.'
    to = 'your_email@your_domain.com'
    email = EmailOperator(
        task_id='send_email_failure',
        to=to,
        subject=subject,
        html_content=body,
        dag=dag
    )
    return email.execute(context=dag.default_context)