# The E-Commerce web application based on Django 
This is the web application which used for shopping online

Render URL : [Clothes Market](https://solo-assessment.onrender.com/) 

Superusername: Ryusenn

Superuserpassword: xhrh0725

## Installation
This application based on python, to start it, the first step is certaining the version of python, and deploy the virtual environment
```bash
    pyenv local 3.10.7 # this sets the local version of python to 3.10.7
    python3 -m venv .venv # this creates the virtual environment for you
    source .venv/bin/activate # this activates the virtual environment
    pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.
```


Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the Dependencies.

```bash
pip install -r requirements.txt 
```


## How to use
Through migrate to create the database.
```bash
python3 manage.py migrate
python3 manage.py makemigrations
```
Then, parse the data to database from csv document 
```bash
python3 manage.py parse_csv
```
The command of running server is 
```bash
python3 manage.py runserver
```
or if you running on the platform online
```bash
python3 manage.py runserver 0.0.0.0
```

## Testing

This application has multiple test method, the built-in test in Django is 
```bash
python3 manage.py test
```
It also has behave test
```bash
behave
```
