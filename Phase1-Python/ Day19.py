# ============================================================
# Day 19 - pip & Virtual Environments
# AI Automation Engineer Journey
# ============================================================

# ------------------------------------------------------------
# WHAT I LEARNED TODAY
# ------------------------------------------------------------

# 1. Difference between Module and Package
#
# Module  -> A single Python file.
# Example:
# import random
# import os
#
# Package -> Collection of Python modules.
# Example:
# requests
# pandas
# beautifulsoup4


# ------------------------------------------------------------
# pip Commands
# ------------------------------------------------------------

# Install Package
# pip install requests

# Show Installed Packages
# pip list

# Show Package Information
# pip show requests

# Upgrade Package
# pip install --upgrade requests

# Upgrade pip
# python -m pip install --upgrade pip

# Freeze Installed Packages
# pip freeze

# Remove Package
# pip uninstall requests


# ------------------------------------------------------------
# Virtual Environment Workflow
# ------------------------------------------------------------

# Step 1
# Create Project Folder

# Step 2
# Create Virtual Environment
# python -m venv myenv

# Step 3
# Activate Virtual Environment (PowerShell)
# .\myenv\Scripts\Activate

# Step 4
# Install Packages
# pip install requests

# Step 5
# Verify Package
# pip show requests

# Step 6
# List Installed Packages
# pip list

# Step 7
# Deactivate Virtual Environment
# deactivate


# ------------------------------------------------------------
# Important Notes
# ------------------------------------------------------------

# Virtual Environment keeps project packages separate.

# Every project should have its own virtual environment.

# Packages installed after activation are stored inside:
# myenv/Lib/site-packages

# requests automatically installs its dependencies:
# - urllib3
# - certifi
# - charset-normalizer
# - idna

# Do NOT upload the myenv folder to GitHub.
# Only upload your source code.


# ------------------------------------------------------------
# End of Day 19
# ============================================================