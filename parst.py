import re
import csv
import subprocess
import argparse

log_file = "nginx.log"
output_csv = "output.csv"

pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)" (\d+) (\d+\.\d+) \[.*?\] \[\] (\d+\.\d+\.\d+\.\d+:\d+) (\d+) (\d+\.\d+) (\d+) (.*)'

def push_to_git(file_path):
    try:
        subprocess.run(["git", "add", "."], check=True)
        print(f"File {file_path} added to git")
        subprocess.run(["git", "commit", "-m", "Commit:1.2.0"], check=True)
        print("Commit created")
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Pushed to git")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

parser = argparse.ArgumentParser(description="Парсинг логів Nginx із фільтрацією")
parser.add_argument('--filter-status', type=str, help='Фільтр за HTTP-статусом (наприклад, 200)')
args = parser.parse_args()

print(f"Значення фільтра статусу: {args.filter_status}")

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

                if args.filter_status and row['Status'] != args.filter_status:
                    continue
                
                writer.writerow(row)

push_to_git(output_csv)
