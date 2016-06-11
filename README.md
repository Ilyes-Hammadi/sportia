Sportia
=============

Sportia is a web application maded with the Flask framework and SQLAlchemy

###Install Virtualbox###
https://www.virtualbox.org/wiki/Downloads


###Install Vagrant###
https://www.vagrantup.com/downloads

Verify that Vagrant is installed and working by typing in the terminal:

	$ vagrant -v   # will print out the Vagrant version number

Clone the Repository
Once you are sure that VirtualBox and Vagrant are installed correctly execute the following:

	$ git clone https://github.com/Ilyes-Hammadi/sportia
	$ cd sportia



###Verify that these files and folders exist in the newly cloned repository:###<br>
    
    ├── data.json                   #json file that contains dummy data
    ├── data.py                     #insert data into the database
    ├── fb_client_secrets.json      #json file that contains your app and client facebook id
    ├── google_client_secrets.json  #json file that contains your app and client google plus id
    ├── manage.py                   #used to run the app
    ├── models.py                   #contains the database models
    ├── static                      #folder that contains all the css js and images
    │   ├── css
    │   ├── img
    │   └── js
    ├── templates                   #folder that contains all the html
    │   ├── base.html
    │   ├── categories
    │   ├── sport
    │   └── user
    ├── views.py                    #contains the app views and settings
    ├── Vagrantfile                 #template that launches the Vagrant environment
    ├── pg_config.sh                #shell script provisioner called by Vagrantfile that performs some configurations

###Launch the Vagrant Box###

	$ vagrant up   #to launch and provision the vagrant environment
	$ vagrant ssh  #to login to your vagrant environment

###Install the python requirements###

    $ sudo apt-get install python python-pip    #install python and pip
    $ virtualenv env                            #create a virtual environment
    $ source env/bin/activate                   #activate the virtual environment
    $ pip install -r requirements.txt         #install the necessary python libraries
    
###Setup OAuth###
In order to let users signin with google plus and facebook you have to authenticate your app in the google and facebook
developer platform

[Facebook Api] (https://developers.facebook.com/apps/)<br>
[Google+ Api] (https://console.cloud.google.com/) 

After you get your credentails from the google+ and facebook api run :
    
    $ python setup.py

And insert your information using the menu 
    
    ------------------- Welcome to Sportia Api Setup ----------------------
    1. Google+ Api
    2. Facebook Api
    99. Exit
    Your Choice (ex: 1): 1
    ----------------------Google Plus Api ---------------------------------
    Enter the Client ID: xxxxxxxxxxxxxxxxxxxxxxxxxxx
    Enter the Project ID: xxxxxxxxxxxxxxxxxxxxxxx
    Enter the Client Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

###Initialize the database###
    
    $ python models.py      #to create the database
	$ python data.py        #to insert the dummy data into the database

###Run the App###

	$ python manage.py      #to run the app


###Shutdown Vagrant machine###

	$ vagrant halt


###Destroy the Vagrant machine###

	$ vagrant destroy

###Licence###

```

The MIT License (MIT)

Copyright (c) 2015 Ilyes Hammadi Ahmed

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
