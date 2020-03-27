#!/bin/bash

install_and_setup_docker=True
DOCKER_HUB_USR=imscientist

sudo apt update

echo "
#########################################
######## install Docker runtime #########
#########################################
"
# source:
# https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04

if [ ${install_and_setup_docker} = True ]; then
  sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
  sudo apt update
  sudo apt install docker-ce -y
fi

echo "
##################################
############ run app  ############
##################################
"
sudo docker run --name dash_app --restart always -d -p 80:80 ${DOCKER_HUB_USR}/plotly_app:1.0
