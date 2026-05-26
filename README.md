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
> is suggested to go over the deployment of each component as follows: Database => Web(1) => Web(2) => Nginx ; the order will not affect the deployment process, however it will ensure everything is properly set up, it will be the step by step processfollowed

> [!WARNING]
> At the start of each section you will find a port list, ensure the machines running the component have these ports open to ensure the correct working, otherwhise, if it is not posible to do so, ensure to change the port wich each component is listening to on the docker compose section
--- 
## Database
The DB is currently running using postgres, the database uses the init.sql file to set up and run the database on the computer, allowing the machine to receive any database releated requests over the port 5432
### Ports
* 5432

### Deployment
in order to deploy the database we will follow these steps:
1. open the Database folder
2. run the command ```docker compose up -d``` in order to execute the container in detached mode
3. confirm the image is running by using ```docker ps```, this will list all the currently running images, in this scenario, the image we are looking for is "postgres:16-alpine"


if you want to perform further checks to ensure the database was correctly set up with it's fields, follow these steps:
1. use  ```docker ps ``` and get the name of the image 
2. use ```docker exec -it <image name> psql -U admin -d proyecto_final```
3. on the postgres CLI use ```\d``` to list all the current tables

in case that you get an error while using a docker command similar to:
 ```permission denied while trying to connect to the docker API at unix:///var/run/docker.sock```
 you might not be added to the user group who is authorized to do so, in that case use ```sudo``` to move forward
---
## web (1)

### Ports
* 

### Deployment

---
## web (2)
### Ports
* 

### Deployment

---
## nginx

### Ports
* 

### Deployment

