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
in order to deploy the database you will follow these steps:
1. open the Database folder
2. run the command ```docker compose up```
3. confirm the image is running by using ```docker ps```, this will list all the currently running images, in this scenario, the image we are looking for is "postgres:16-alpine"


if you want to perform further checks to ensure the database was correctly set up with it's fields, follow these steps:
1. use  ```docker ps ``` and get the name of the image 
2. use ```docker exec -it <image name> psql -U admin -d proyecto_final```
3. on the postgres CLI use ```\d``` to list all the current tables, you should be able to see the "registros" table described on the init.sql file inside the folder 

>[!IMPORTANT]
>in case that you get an error while using a docker command similar to:```permission denied while trying to connect to the docker API at unix:///var/run/docker.sock``` you might not be added to the user group who is authorized to do so, in that case use ```sudo``` to move forward

---
## web (1) [ESP]
this is the user interface that was be created in order to access the data and allow users to submit data and view/request an email with a statistic breakdown of the collected data, it's the english version of the site
### Ports
* 5000

### Deployment
in order to enable the mail sending feature through google, follow the following steps: 
1. open the docker-compose file
2. locate the variables ```MAIL_USERNAME``` and ```MAIL_PASSWORD```
3. use the email address (ej:email@gmail.com) as the user, and the mail password is the mail password provided by google(not your user password)

>[!NOTE]
>is not required to have the mail feature enabled to get the page running 

in order to deploy the web page, you need to follow these steps:
1. go to the web folder
2. open the docker-compose file  and change the ```DB_HOST``` to your database internal IP under the ```web-app-es``` service 
3. use  docker ```compose up web-app-es``` to deploy the ESP version of the web page



---
## web (2) [ENG]
this is the user interface that was be created in order to access the data and allow users to submit data and view/request an email with a statistic breakdown of the collected data, it's the english version of the site

### Ports
* 5000

### Deployment
in order to deploy the web page, you need to follow these steps:
in order to deploy the web page, you need to follow these steps:
1. go to the web folder
2. open the docker-compose file  and change the ```DB_HOST``` to your database internal IP under the web-app-en service 
3. use  docker ```compose up web-app-en``` to deploy the ESP version of the web page
---
>[!NOTE]
>web (2) [ENG] and web (1) [ESP] are exchangable, ensure the proper service is being edited on the docker-compose file uppon deployment 
## nginx

this component acts as the load balancer of the project and ensures the users are distributed across machines evenly, it also provides a SSL certificate from certbot,since certbot needs to have a machine running to be able to provide the appropiate certificates

### Ports
* 443
* 80

### Deployment

in order to deploy nginx you need to follow these steps:

1. go to the nginx folder
2. open the nginx folder inside of it so you can edit the config files
3. on the file ```confdummie.d``` you will find the ```server_name``` attribute under the server section, change it to the domain you have and want to set up for the project; this will allow you to obtain the certificates needed.
4. change the ```server``` attributes under ```upstream backend_servers``` to the private IP of each machine hosting the webs, the order does not matter
5. go out of the nginx folder, ensure that you are on the right folder by using ```ls``` and confirm you see the nginx folder and the ```docker-compose``` file
6. run the command ```docker compose up nginx```
7. manually execute: 
```sudo docker compose run --rm --entrypoint "certbot" certbot certonly --webroot --webroot-path=/var/www/certbot --email <mail> --agree-tos --no-eff-email -d <domain>```
8. even though certbot can take a few seconds to create the certificates needed to execute the project, it is recommended to wait at least 1 minute in order to use the command ```docker compose down``` to shut down the container and keep the generated certificates
9. open the ```docker-compose``` file, and go to the ```volumes``` section
10. on the line ```- ./nginx/confdummie.d:/etc/nginx/conf.d:ro``` change the "confdummie.d" segment to "conf.d"; the line should look like ```- ./nginx/conf.d:/etc/nginx/conf.d:ro``` and save the changes
11. open the nginx folder 
12. open the ```conf.d```
13. apply the same changes on step 4 
14. on both server sections, change the ```server_name``` to the domain you want to use
15. on the last server section, you will find the attributes ```ssl_certificate``` and ```ssl_certificate_key``` change it's values so it points to a folder with your domain name it should look like this:
    * ```ssl_certificate /etc/letsencrypt/live/<your domain>/fullchain.pem;```
    * ```ssl_certificate_key /etc/letsencrypt/live/<your domain>/privkey.pem;```
16. use ```docker compose up``` 

