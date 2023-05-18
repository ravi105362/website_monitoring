# Status tracking service

Monitor your website with their downtimes on the fly

## Steps to run

1. Create a virtual env - python3 -m venv venv
2. Install the dependencies - pip install -r requirements.txt
3. Change the folder path in settings.py for security related files
4. Create the Aiven kafka service and Aiven Postgres service instance
5. run the command - python3 src/main.py
6. To run all the tests - pytest

## Service structure

It starts with a Kafka Producer checking the status of the given websites and
sending them over to the broker. Consumer collects it from the broker and
processes it to store in the the postgres DB.

Database is structed in the following tables -

1. websites - Stores the list of websites
2. status - Stores the status of the websites with the timestamp at which
   that status was found.
