from flask import Flask, request
import codecs
import os
from google.cloud import bigquery

app = Flask(__name__)

#GLOBAL BIG QUERY VARIABLES
SERVICE_ACCOUNT_JSON = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
project = "animated-cinema-369614"
Dataset_id = "SMG_Task"
Table_id = "sentence_table"

#FUNCTION TO QUERY ONE SENTENCE FROM BIG QUERY AND RETRIEVE CRYPTED SENTENCE
def extract_rot13_encoded_sentence(project, Dataset_id, Table_id,sentence_id):
    query = ("""
		SELECT  id, text FROM {0}.{1}.{2} 
		WHERE id={3};
		""").format(project, Dataset_id, Table_id, sentence_id)
    df = client.query(query).to_dataframe()
    df['cyphered_text']=df.apply(lambda row: codecs.encode(str(row['text']), 'rot13'), axis=1)
    #df = df.drop('text', axis=1)
    return df.iloc[0].to_json()

#FUNCTION TO RETRIEVE LAST INDEX IN THE TABLE
def get_last_index(project, Dataset_id, Table_id):
    query = ("""
		SELECT  MAX(id) as max_id FROM {0}.{1}.{2};
		""").format(project, Dataset_id, Table_id)
    df = client.query(query).to_dataframe().at[0,'max_id']
    return df
  
#FUNCTION TO POST A NEW SENTENCE IN BIG QUERY WITH LAST ID
def post_new_sentence(project, Dataset_id, Table_id, test_sentence):
    last_id=get_last_index(project, Dataset_id, Table_id)
    table = client.get_table("{}.{}.{}".format(project, Dataset_id, Table_id))
    new_id=last_id+1
    rows_to_insert = [{u"id": int(new_id), u"text": str(test_sentence)}]
    errors = client.insert_rows_json(table, rows_to_insert)
    if errors == []:
        print("success")

#GET API ENDPOINT
@app.route("/sentences/<int:sentenceId>", methods=['GET'])
def get_sentence(sentenceId):
    last_id = get_last_index(project, Dataset_id, Table_id)
    if sentenceId <= last_id:
        return extract_rot13_encoded_sentence(project, Dataset_id, Table_id,sentenceId), 200
    elif sentenceId > last_id:
        return "Invalid ID supplied", 400
    else:
        return "Sentence not found", 404

#POST API ENDPOINT
@app.route('/sentences/', methods=['POST'])
def post_sentence():
    new_sentence=request.get_data()
    post_new_sentence(project, Dataset_id, Table_id, new_sentence)
    last_id=get_last_index(project, Dataset_id, Table_id)
    return ("id: {0} with sentence: {1} successfully uploaded").format(last_id,new_sentence), 200

app.run()

#POST EXAMPLE: curl -X POST -d "Write your sentence here" http://localhost:5000/sentences/
#GET EXAMPLE: curl  http://localhost:5000/sentences/1
