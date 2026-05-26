# telematicaFinal

## initial setup

in order to set up this project it is needed to have at least 4 machines or instances on aws or any other servive available runing ubuntu server.

upon cloning of the repository on a computer or AWS instance (or any provider for that matter), run ```dockerinstall.sh``` to install docker and be able to move further

to do so:
1. execute: ```chmod -x dockerinstall.sh```
2. execute: ```sudo bash dockerinstall.sh```,This will install docker and test it using the hello world image. ensure you are able to see the image results on console
3. move onto the project component's folder you want to run on the machine

## folders

the project has the following component's folders:

* Database: contains all the database setup related files
* nginx: contains all the nginx setup related files
* web: contains all the webpage setup related files

in order to move forward go to the dedicated section for each component.

> [!NOTE]
> is suggested to go over the deployment of each component as follows: Database => Web(1) => Web(2) => Nginx ; the order will not affect the deployment process, however, it will be the step by step process followed

## Database



## web (1)

## web (2)

## nginx
in order to run the load balancer this project is currently using Nginx 


### used ports:
* 1000: due to the usage of docker, the image will be listening through the port 1000; if needed, the settings on docker compose can be changed to set the port connected to the "physical" or virtual port

