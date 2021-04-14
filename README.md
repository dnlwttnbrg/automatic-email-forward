# Information
This script automaticaly send incoming emails to a new email address.

# Installation
The script needs Python 3.x
This script is using following packages:

- imaplib <br>
- configparser <br>
- smtplib <br>
- logging <br>
- email <br>


All packages should be pre installed
To download the scripts enter `git clone https://github.com/dnlwttnbrg/automatic-email-forward.git` into the console.
Execute the script by entering `python3 automatic_email_forward.py`. On a linux server type `python3 automatic_email_forward.py &` to run the script in the background.



------------

# Configuration
There are several configurations that needs to be done. All configurations can be done in `config.ini`. <br>
## General
- language: There are at the moment two languages available. `german` and `english`.
## RECEIVE EMAIL
- host: The IMAP-host-server. For example `imap.gmail.com`.<br>
- port: The Imap-Port. For example (google): `993`.<br>
- name: Login name. Check your provider what credentials you need to use.<br>
- password: Password for your account. Check your provider what credentials you need to use.<br>
## SEND EMAIL
- host: The SMTP-host-server. For example `smtp.gmail.com`.<br>
- port: The SMTP-Port. For example (google): `465`.<br>
- name: Login name. Check your provider what credentials you need to use.<br>
- password: Password for your account. Check your provider what credentials you need to use.<br>
- sender: The email-address the new email is send from. <br>
- targets: The email.address the new email is send to.

