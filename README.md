# CSC 450 - Team Project

## Team Members

* Terrence Hernandez
* Andrew Davison
* Will Rosoff
* Daniela Garcia-Garcia
* Joseph Giltinan
* Travis Fryar

## Setup and Starting Virtual Environment

> Install Python
  * https://www.python.org/downloads/
> Setup/Install Heroku Account/CLI
  * Account: https://signup.heroku.com/identity
  * CLI: https://devcenter.heroku.com/articles/heroku-cli
  * Continue following heroku's instructions if necessary
> Install Pycharm
  * https://www.jetbrains.com/pycharm/download/#section=windows
  * Community is Free, Professional has free trails and options.
  * Set up an interpreter: https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html

> Create a Virtual Environment (venv)

1) Open command line terminal and navigate to project's root directory
2) Depending on your platform:
    * On Windows enter:<br/>
      &ensp;py -m venv venv
    * On Mac enter:<br/>
      &ensp;python3 -m venv venv
3) Next:
    * On Windows enter:<br/>
      &ensp;venv\scripts\activate
    * On Mac:<br/>
      &ensp;. venv/bin/activate
      <br/><b>If a (venv) appears before the source in your terminal command line, success!</b>

> Install Packages from requirements.txt

* In the terminal command line, with the (venv) still active, enter:<br/>
  &ensp;pip install -r requirements.txt

## Starting/Running the Server

* Running <b>app.py</b> will activate the Flask server
* Follow the link provided by IDE, terminal/console, or copy and paste the line below into your browser.
* <br/>&ensp;127.0.0.1:5000

## Creating/Updating local DB

* In (venv) run command: flask db upgrade
* You may need to delete your current local db every now and again depending on new migration versions/directories
* To save any new schema changes to the db migration versions: flask db migrate

