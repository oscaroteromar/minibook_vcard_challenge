# Minibook vCard challenge

## Overview
This repository contains the code for a program that extracts all the data from the contacts stored in the address book service Minibook.

## Code
All the code is written on Python in just one file named _vcard_contact_challenge.py_ which contains two classes and the main module.
- The first class is called _Login_. It executes the log in operation in the address book and retrieve the html for the contacts page. 
- The second class is named _ParseHTML_. It allows to fetch the information from the given html and store all the contacts data in a list of dictionaries. Then, this list is converted into vCard.

The libraries that have been used are: requests, bs4 and vobject.

## Input and output
The user is asked for the username and the password as an input at the begining of the execution. Three outputs can be obtained:
- If the given user data is right and there are contacts stored, the contacts will be displayed in string and vCard format.
- If the user data is right but the are no contacts, a feedback message will be printed.
- If the input user data is wrong, an error will appear and the program will end.

## Requirements
Apart from the code file, a _requirements.txt_ file has been included in this repository. These can be installed, preferably in a virtual environment, by using the next command
```
sudo pip3 install -r requirements.txt
```

## Run
In order to run the program the following command can be executed 
```
python3 vcard_contact_challenge.py
```
