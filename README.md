### :exclamation:ONLY USE GIT/GITHUB DESKTOP TO INTERACT WITH THIS REPO:exclamation:

## FLASK SERVER FOR POS SYSTEM

**If you get stuck Google: '*[Whatever you are trying to do] in flask*' and follow the tutorial**

### how to get started

1. ```$ git clone https://github.tamu.edu/jacobt1206/proj3_server.git```
2. ```$ cd proj3_server```
3. On a mac: ```python3 -m venv env``` || On a PC: ```py -3 -m venv env```
4. On a mac: ```. env/bin/activate``` || On a PC: ```env\Scripts\activate```
5. ```pip install -r requirements.txt```
6. ```flask run```
> At this point you can begin working in the main.py file. Remember to push and pull frequently.
7. ```Ctrl + C``` to kill the server
8. ```$ deactivate``` to deactive the virtual enviornment
9. Push to github

### how to begin work

1. ```$ cd proj3_server```
2. ```git pull origin main --rebase```
3. On a mac: ```. env/bin/activate``` || On a PC: ```env\Scripts\activate```
4. ```pip install -r requirements.txt```
5. ```flask run```
> At this point you can begin working in the main.py file. Remember to push and pull frequently.
6. ```Ctrl + C``` to kill the server
7. ```$ deactivate``` to deactive the virtual enviornment
8. Push to github


### how to test endpoints with Postman

The server is going to running on your laptop at `http://127.0.0.1:5000`. To test whether or not your endpoint is working, go to postman and make a `POST` or `GET` request to `http://127.0.0.1:5000/[your endpoint name]`. Add any form data you need to in Postman and then click send. the server will respond with a message, you can debug from there.

### IMPORTANT!

if you use pip to install a package, run the following command ```pip freeze > requirements.txt``` and then push the changes. This will update the requirements.txt. Once this is done notify the group of the change.

To install packages run the following command ```pip install -r requirements.txt```
