# plotly-web-app

### Setup 
- Create an environment and install the required dependencies:
    ```shell script
    conda create -n plotly-web-app python=3.8 -y
    conda activate plotly-web-app
    pip install -r requirements.txt
    pip install -e .
    ```

- Local test of the app:  
  Dash apps are web applications. 
  Dash uses Flask as the web framework. 
  The underlying Flask app is available at `app.server`
    ```shell script
    export FLASK_APP=app:server
    flask run
    ```
- Azure Web app deployment notes:
  In `web-app` -> `Configuration` -> `General settings` set the 
  startup command to `gunicorn -b 0.0.0.0 app:server` 

### App with preprocessed content
- Idea: Instead of splitting the data, calculating the 
roc-auc scores, generating and plotting the new figures, we can 
generate, dump and load all possible figures and roc-auc scores.

- Generate the content by executing:
    ```shell script
    python create_content.py
    ```
    This content is used in `app_2.py`:
    ```shell script
    export FLASK_APP=app_2:server
    flask run
    ```
  
- Azure Web app deployment notes:
  In `web-app` -> `Configuration` -> `General settings` set the 
  startup command to `gunicorn -b 0.0.0.0 app_2:server`  
