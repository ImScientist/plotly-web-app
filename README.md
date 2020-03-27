# plotly web app

## Setup 
- Create an environment and install the required dependencies:
    ```shell script
    conda create -n plotly-web-app python=3.8 -y
    conda activate plotly-web-app
    pip install -r requirements.txt
    pip install -e .
    ```

- Local test of the app:   
  Dash uses Flask as the web framework. 
  The underlying Flask app is available at `app.server`
    ```shell script
    export FLASK_APP=app:server
    flask run
    ```
 
- Speed up the app   
  Idea: Instead of splitting the data, calculating the roc-auc scores, 
  generating and plotting the new figures, we can generate, dump and load all 
  possible figures and roc-auc scores.

  Generate the content by executing:
    ```shell script
    python create_content.py
    ```
    This content is used in `app_2.py`:
    ```shell script
    export FLASK_APP=app_2:server
    flask run
    ```

## Deployment

#### Azure Web app deployment notes (do not use this service)  
- In `web-app` -> `Configuration` -> `General settings` set the 
  startup command to `gunicorn -b 0.0.0.0 app_2:server` or to 
  `gunicorn -b 0.0.0.0 app:server` depending on what you want to run. 

#### Use google app engine (do not use this service)
  - Create a `app.yaml` that contains info about the runtime and 
  about the entrypoint. Then use the gcloud cli:
    ```shell script
    gcloud init
    # go into the right project
    gcloud app deploy ./app.yaml -Y
    ```

#### Use a docker image running on ubuntu VM
- Build the image:   
  In case you want to deploy the app somewhere else:
  ```shell script
  docker build -t plotly_app:1.0 . --build-arg runtime_path="."
  ```
  Launch a container to test the app:
  ```shell script
  docker run --rm --name dash_app -d -p 80:80 plotly_app:1.0
  ```
  If everything is fine, add the image to the dockerhub container registry:
  ```shell script
    docker login -u "$DOCKER_HUB_USR" \
                 -p "$DOCKER_HUB_PWD"
    
    docker tag plotly_app:1.0 "${DOCKER_HUB_USR}"/plotly_app:1.0
    
    docker push "${DOCKER_HUB_USR}"/plotly_app:1.0
  ```
- Setup a ubuntu machine to run the docker container:
  ```shell script
  chmod +x vm_docker_setup.sh
  ./vm_docker_setup.sh  
  ```

