# -----------------------------
# Day 20 - Python Package Management
# AI Automation Engineer Roadmap
# -----------------------------


# Today's main topics:
# 1. Virtual environments
# 2. pip install
# 3. pip list
# 4. pip freeze
# 5. requirements.txt
# 6. Using installed packages in Python


# -----------------------------
# Virtual Environment
# -----------------------------

# Create a virtual environment
# Command:
# python -m venv myenv

# Activate (PowerShell)
# .\myenv\Scripts\activate

# Deactivate
# deactivate


# -----------------------------
# Package Management
# -----------------------------

# Install a package
# python -m pip install colorama

# Show installed packages
# python -m pip list

# Show installed packages with exact versions
# python -m pip freeze

# Save installed packages into requirements.txt
# python -m pip freeze > requirements.txt

# Install packages from requirements.txt
# python -m pip install -r requirements.txt


# -----------------------------
# Practical Example
# -----------------------------

from colorama import Fore, Style

def welcome_message():
    return "Welcome to Employee Automation Project"

def show_message(message):
    print(Fore.GREEN + message + Style.RESET_ALL)

message = welcome_message()
show_message(message)

print("\n")

# -----------------------------
# Day 20 Summary
# -----------------------------

from colorama import Fore, Style

print(Fore.CYAN + "\n=== Day 20 Summary ===" + Style.RESET_ALL)

print("✔ Virtual Environment")
print("✔ pip install")
print("✔ pip list")
print("✔ pip freeze")
print("✔ requirements.txt")
print("✔ colorama package")
print("✔ Project completed successfully")