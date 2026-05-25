# telematicaFinal

## initial setup
upon cloning of the repository on a new Ec2 (or any provider for that matter) ubuntu machine, run '''dockerinstall.sh''' to install docker and be able to move further

to do so:
1. execute: '''chmod -x dockerinstall.sh'''
2. execute: '''sudo bash dockerinstall.sh''', as this will install docker and test it using the hello world image; ensure you are able to see the image results on console
3. move onto the project component's folder you want to run on the machine

## folders

the project has the following component's folders:

* Database: contains all the database setup related files
* nginx: contains all the nginx setup related files
* web: contains all the webpage setup related files

in order to move forward go to the dedicated section for each component.

> [!NOTE]
> is suggested to go over the deployment of each component as follows: Nginx => Database => Web(1) => Web(2); the order will not affect the deployment process, however, it will be the step by step process followed

## nginx
## Database
## web (1)
## web (2)
