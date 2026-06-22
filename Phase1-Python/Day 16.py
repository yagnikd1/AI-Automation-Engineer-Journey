# ----------------------------------------------------------------------------------------------------------  Real File Locations & Paths --------------------------------

# --------------------------------------------------   Relative Path 

file = open("report.txt", "w")



# --------------------------------------------------   Absolute Path

file = open(r"C:\Users\Yagnik\Desktop\report.txt", "w")



# --------------------------------------------------    Example

file = open(
r"C:\Users\Yagnik\Desktop\sales_report.txt",
"w"
)



# ----------------------------------------------------------------------------------------------------------  Creating Files Inside Folders ---------------------------



file = open("Reports/report.txt", "w")

file.write("Sales Report")

file.close()





# ----------------------------------------------------------------------------------------------------------  Creating Folders Automatically ---------------------------

import os

os.mkdir("Reports")





# ----------------------------------------------------------------------------------------------------------  Deleting Files -------------------------------------------


import os

os.remove("employee.txt")



# ----------------------------------------------------------------------------------------------------------  Check If File Exists -------------------------------------


import os

if os.path.exists("employee.txt"):
    os.remove("employee.txt")



# ----------------------------------------------------------------------------------------------------------  Rename Files ---------------------------------------------


import os

os.rename("report.txt", "sales_report.txt")


# ------------------------------------------------------------------------------------------------  File Cleanup Automation ---------------------------------------------


import os

if os.path.exists("old_reports.txt"):
   os.rename("old_reports.txt", "report_backup.txt" ) 



# ------------------------------------------------------------------------------------------------  File Cleanup Automation Project  ------------------------------------

import os

if os.path.exists("old_report.txt"):
    os.rename("old_report.txt", "report_backup.txt")

file = open("report.txt", "w")
file.write("New Report Created")
file.close()





# ------------------------------------------------------------------------------------------------  File Handling Mastery Project  ------------------------------------


# --------------------------------------------------   Relative Path

import os

if os.path.exists("report.txt"):
    os.rename("report.txt", "report_backup.txt")    

report = ("Enter Today's Report: ") 

file = open("report.txt", "w")
file.write(report)
file.close()


# --------------------------------------------------   Employee Record System

name = input("Enter Employee Name: ")
city = input("Enter City")

import os
if os.path.exists("employee.txt"):
    os.rename("employee.txt", "employee_backup.txt")

file = open("employee.txt", "w")
file.write("Employee: ")
file.write(name)
file.write("\n")
file.write("City: ")
file.write(city)

file.close()