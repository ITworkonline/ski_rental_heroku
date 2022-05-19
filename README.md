# CSCI5828_Group_Project
![example event parameter](https://github.com/ITworkonline/ski_rental_heroku/actions/workflows/python-app.yml/badge.svg?event=push)

## Project Name
Ski Rental Heroku

## Access link
https://flask-deploy-ski.herokuapp.com/

## Team Member
 Jie Wang <br>
 Yvonne Liu <br>
 Yifan Chen <br>
 Sitong Lu <br>
 
 
## Project Description
A webpage that provides Ski rental service and can be used by both customers and managers.

By signning into this webpage, you can click on the Customer Mode to browse the ski equipment sorted by brand (which is also available for rental) and rent it, or click on the Manager Mode to view and edit the rental status of all existing equipment，or even add new equipment into the list.

To enter the Manager Mode, please use the following *login password: 12345*

## File map
* app
  * templates(html)

  * __init__.py

  * models.py

  * form.py

  * route.py
 
  * email.py

* config.py

* requirements.txt

* run.py  

## Run command
``` python
python run.py
```
To start consumer and producer (require to install RabbitMQ)
``` python
python producer.py
python consumer.py
```

## More Info: design decisions, software architecture
https://github.com/ITworkonline/ski_rental_heroku/wiki
