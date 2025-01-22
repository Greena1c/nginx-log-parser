import re
import csv
import subprocess
import argparse
from datetime import datetime

log_file = "nginx.log"
all_logs_csv = "all_logs.csv"
filtered_logs_csv = "filtered_logs.csv"

pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)" (\d+) (\d+\.\d+) \[.*?\] \[\] (\d+\.\d+\.\d+\.\d+:\d+) (\d+) (\d+\.\d+) (\d+) (.*)'

def push_to_git():
    try:
        subprocess.run(["git", "add", "."], check=True)
        print("All files added to git")
        subprocess.run(["git", "commit", "-m", "Updated logs", "--allow-empty"], check=True)
        print("Commit created")
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Changes pushed to GitHub")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while pushing to Git: {e}")

parser = argparse.ArgumentParser(description="Парсинг логів Nginx із фільтрацією та сортуванням")
parser.add_argument('--status-range', type=str, help='Діапазон HTTP-статусів, наприклад, "400-500"')
parser.add_argument('--date', type=str, help='Фільтр за датою у форматі "DD/MM/YYYY", наприклад, "26/04/2021"')
parser.add_argument('--sort-by', type=str, help='Поле для сортування (наприклад, "Status", "Size")')
parser.add_argument('--sort-order', type=str, choices=['asc', 'desc'], default='asc', help='Порядок сортування (asc/desc)')
args = parser.parse_args()

status_min, status_max = None, None
filter_date = None

if args.status_range:
    try:
        status_min, status_max = map(int, args.status_range.split('-'))
    except ValueError:
        print("Неправильний формат діапазону статусів. Використовуйте формат '400-500'.")
        exit(1)

if args.date:
    try:
        filter_date = datetime.strptime(args.date, "%d/%m/%Y")
    except ValueError:
        print("Неправильний формат дати. Використовуйте формат 'DD/MM/YYYY'.")
        exit(1)

all_rows = []
filtered_rows = []

with open(log_file, "r") as file:
    for line in file:
        match = re.match(pattern, line)
        if not match:
            print(f"Не вдалося зіставити рядок: {line}")
            continue

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
        all_rows.append(row)

        if status_min is not None and status_max is not None:
            status = int(row['Status'])
            if not (status_min <= status <= status_max):
                continue

        if filter_date:
            log_date = datetime.strptime(row['Timestamp'].split(':')[0], "%d/%b/%Y")
            if log_date.date() != filter_date.date():
                continue

        filtered_rows.append(row)

if not args.status_range and not args.date and not args.sort_by:
    print("Запуск без фільтрації: всі рядки додаються до результату")
    filtered_rows = all_rows

if args.sort_by:
    filtered_rows.sort(
        key=lambda x: int(x[args.sort_by]) if x[args.sort_by].isdigit() else x[args.sort_by],
        reverse=(args.sort_order == "desc")
    )

print(f"Усі рядки: {len(all_rows)}")
print(f"Фільтровані рядки після фільтрації: {len(filtered_rows)}")

with open(all_logs_csv, "w", newline="") as csvfile:
    fieldnames = list(all_rows[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_rows)

with open(filtered_logs_csv, "w", newline="") as csvfile:
    fieldnames = list(all_rows[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    if filtered_rows:
        writer.writerows(filtered_rows)
    else:
        print("Немає результатів для запису у filtered_logs.csv")

push_to_git()
