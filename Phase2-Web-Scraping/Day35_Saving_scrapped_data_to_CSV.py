"""
DAY 35 - SAVING SCRAPED DATA TO CSV
============================================================
Phase 2 - Web Scraping

ROADMAP
HTML -> BeautifulSoup -> select() -> Loop -> Dictionary -> job_list -> Filter -> CSV

TOPICS
1. CSV (Comma-Separated Values)
2. csv module
3. csv.writer()
4. csv.DictWriter()
5. writer.writerow()
6. writer.writeheader()
7. newline='' 
8. encoding='utf-8'
9. 'w' vs 'a'
10. Professional workflow

NOTES
- CSV is a text file readable by Excel/Google Sheets.
- writer() writes lists.
- DictWriter() writes dictionaries.
- writer.writerow() writes ONE row.
- writeheader() writes column headings once.
- newline='' prevents blank rows on Windows.
- utf-8 supports international characters.
- 'w' overwrites existing files.
- 'a' appends to existing files.
- Keep writer.writerow() inside the loop.

COMMON MISTAKES
- writer.writerow() outside loop
- Missing writeheader()
- fieldnames not matching dictionary keys
- Comparing string salary with integer
- Forgetting utf-8/newline

INTERVIEW QUESTIONS
- What is CSV?
- Difference between writer and DictWriter?
- Why newline=''
- Why utf-8?
- Difference between w and a?
"""

import csv
from bs4 import BeautifulSoup

HTML = """
<div class="job-card"><h2 class="job-title">Python Automation Developer</h2><p class="company">Northstar Systems</p><p class="location">Remote</p><p class="salary">65000</p></div>
<div class="job-card"><h2 class="job-title">Web Scraping Assistant</h2><p class="company">Bluewave Analytics</p><p class="location">New York</p><p class="salary">48000</p></div>
<div class="job-card"><h2 class="job-title">Junior Data Engineer</h2><p class="company">Vertex Labs</p><p class="location">London</p><p class="salary">72000</p></div>
"""

def get_high_salary_jobs(job_list, minimum_salary):
    result = []
    for job in job_list:
        if job["Salary"] >= minimum_salary:
            result.append(job)
    return result

soup = BeautifulSoup(HTML, "html.parser")
jobs = soup.select(".job-card")
job_list = []
for job in jobs:
    job_data = {
        "Title": job.select_one(".job-title").text.strip(),
        "Company": job.select_one(".company").text.strip(),
        "Location": job.select_one(".location").text.strip(),
        "Salary": int(job.select_one(".salary").text.strip())
    }
    job_list.append(job_data)

MINIMUM_SALARY = 60000
filtered_jobs = get_high_salary_jobs(job_list, MINIMUM_SALARY)
for job in filtered_jobs:
    print(f"{job['Title']} | {job['Company']} | ${job['Salary']:,}")

with open("filtered_jobs.csv","w",newline="",encoding="utf-8") as file:
    field_names=["Title","Company","Location","Salary"]
    writer=csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()
    for job in filtered_jobs:
        writer.writerow(job)

print("CSV exported successfully.")

# Git Commit Suggestion
# git add .
# git commit -m "Day 35: Added CSV export using csv.writer and DictWriter"
