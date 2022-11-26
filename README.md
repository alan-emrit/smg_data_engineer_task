# smg_data_engineer_task

Steps Done:

- Data Loaded To Big Query
- Creation Service Account with BigQuery User and Big Query Data Owner permissions 
- Creation json key to access service account
- Simple REST API implemented with Python Flask (alternatively can be done with FastAPI)
- The API run in localhost at port 5000
- run app.py 
- launch requests from another terminal window either with GET or POST (curl -X POST -d "<your string>" http://localhost:5000/sentences/)
- GET request run directly in the browser by providing a numerical id
- Alternatevely the requests can be launch with Postman
- The Open API specification was read with Swagger Editor
- The REST API remain very simple but can be further improved
