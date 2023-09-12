# Bojio Backend

## Prerequisites
* Install Python 3.10.x

## Installation
### Create virtual environment
In your terminal, navigate to project root directory and run the following commands.
1. `pip install virtualenv`
2. `python -m venv env`
3. `.\env\Scripts\activate` for Windows and `source env/bin/activate` for Mac

### Install Dependencies
Run `pip install -r requirements.txt`

## Run Project
### Activate virtual environment
`.\env\Scripts\activate` for Windows and `source env/bin/activate` for Mac

### Run using development config
`flask run --debug`

### Run using production config
`flask run`
