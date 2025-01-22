import re
import csv
import subprocess
import argparse
from datetime import datetime

log_file = "nginx.log"
output_csv = "output.csv"

pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)" (\d+) (\d+\.\d+) \[.*?\] \[\] (\d+\.\d+\.\d+\.\d+:\d+) (\d+) (\d+\.\d+) (\d+) (.*)'

def push_to_git():
    """
    Додає всі файли у Git, створює коміт і пушить у віддалений репозиторій.
    """
    try:
        subprocess.run(["git", "add", "."], check=True)
        print("All files added to git")
        
        subprocess.run(["git", "commit", "-m", "Updated project files"], check=True)
        print("Commit created")
        
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Changes pushed to GitHub")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

parser = argparse.ArgumentParser(description="Парсинг логів Nginx із фільтрацією")
parser.add_argument('--status-range', type=str, help='Діапазон HTTP-статусів, наприклад, "400-500"')
parser.add_argument('--date', type=str, help='Фільтр за датою у форматі "DD/MM/YYYY", наприклад, "26/06/2024"')
args = parser.parse_args()

print(f"Діапазон статусів: {args.status_range}")
print(f"Фільтр за датою: {args.date}")

status_min, status_max = None, None
if args.status_range:
    try:
        status_min, status_max = map(int, args.status_range.split('-'))
    except ValueError:
        print("Неправильний формат діапазону статусів. Використовуйте формат '400-500'.")
        exit(1)

filter_date = None
if args.date:
    try:
        filter_date = datetime.strptime(args.date, "%d/%m/%Y")
    except ValueError:
        print("Неправильний формат дати. Використовуйте формат 'DD/MM/YYYY'.")
        exit(1)

with open(output_csv, "w", newline="") as csvfile:
    fieldnames = [
        'IP', 'Timestamp', 'Request', 'Status', 'Size',
        'Referrer', 'User-Agent', 'Bytes Sent', 'Request Time',
        'Backend Server', 'Backend Response Bytes',
        'Backend Response Time', 'Backend Status', 'Hash'
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    with open(log_file, "r") as file:
        for line in file:
            match = re.match(pattern, line)
            if match:
                row = {
                    'IP': match.group(1),
                    'Timestamp': match.group(2),
                    'Request': match.group(3),
                    'Status': match.group(4),
                    'Size': match.group(5),
                    'Referrer': match.group(6),
                    'User-Agent': match.group(7),
                    'Bytes Sent': match.group(8),
                    'Request Time': match.group(9),
                    'Backend Server': match.group(10),
                    'Backend Response Bytes': match.group(11),
                    'Backend Response Time': match.group(12),
                    'Backend Status': match.group(13),
                    'Hash': match.group(14),
                }

                status = int(row['Status'])
                if status_min is not None and status_max is not None:
                    if not (status_min <= status <= status_max):
                        continue

                log_date = datetime.strptime(row['Timestamp'].split(':')[0], "%d/%b/%Y")
                if filter_date and log_date.date() != filter_date.date():
                    continue

                writer.writerow(row)

push_to_git()
