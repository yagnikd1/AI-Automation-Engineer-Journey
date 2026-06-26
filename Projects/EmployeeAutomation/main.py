from colorama import Fore, Style

def welcome_message():
    return "Welcome to Employee Automation Project"

def show_message(message):
    print(Fore.GREEN + message + Style.RESET_ALL)

message = welcome_message()
show_message(message)

