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
- Run with gunicorn:
  ```shell script
  gunicorn -b 0.0.0.0:5000 app:server
  ```
