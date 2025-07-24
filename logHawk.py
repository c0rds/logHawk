#!/bin/env python3
#logHawk
import re #RegEx module
import sys #access to command-line args
import os #path helpers
from collections import Counter, defaultdict #importing built-in counter module to script

if len(sys.argv) != 2: #counts how many elements are in list.. this script expects only one real argument
    sys.exit("Usage: logHawk.py <filtered.-log>") #stops script with error message if we didn't provide exactly one filepath 
    #prevents logHawk from running with bad input and crashing later (i.e., early error catching)

log_path = sys.argv[1] #full path to filtered log file

status_count = defaultdict(int)  #Using dictionary for the counts - auto-creates new keys at 0
ip_addresses = []  # List to collect matching IPs

#Reading the log file,
with open(log_path, "r", encoding="utf-8") as logFile: #Open logfile for reading
    for line in logFile: #loop through lines in logfile
        match = re.search(r'(\d+.\d+.\d+.\d+).*"\s(\d{3})\s', line) #Switched to RegEx for match.group2 because of output issues
        if match: # Was pattern found?
            ip = match.group(1) # first set of brackets in match relates to IP address RegEx
            status = match.group(2) # Second set of brackets for error codes
            status_count[status] += 1 # Tally of total instances of error code entries
            ip_addresses.append(ip) #Storing IPs for later retrival 

#Preparing output (building report lines)
output_lines = []
output_lines.append(f"Number of occurrences of '404': {status_count['404']}") 
output_lines.append(f"Number of occurrences of '500': {status_count['500']}")
#with defaultdict, you can add any error code you would like here to be counted
ip_counts = Counter(ip_addresses)
sorted_ips = sorted(ip_counts, key=ip_counts.get, reverse=True) 
output_lines.append("Sorted IP addresses (most common to least):") #Sorted high -> low
for ip in sorted_ips:
    output_lines.append(f"{ip} : {ip_counts[ip]}") #add each IP line

# 1. Writing output to a file: 

#1.1 Expands '~' to the actual home directory and point to desktop folder
#e.g., "/home/student/Desktop/logHawk_analysis"
desktop_dir = os.path.expanduser("~/Desktop/logHawk_analysis") 

#1.2 Create logHawk_analysis directory if it doesn't already exist
os.makedirs(desktop_dir, exist_ok=True) #exist_ok=True -> prevents error if it already exists

#1.3 Pull only filename portion out of the full file path
base = os.path.basename(log_path) # e.g., "filtered_2025-07-23-10.log"

#1.4 Convert old filtered log filename to report filename
report = "report_" + base.replace("filtered_", "").rsplit(".", 1)[0] + ".txt"
#      -new prefix-      -drop old prefix-     -remove .log extension-   -add .txt extension-

#1.5 Add new file to new directory to create new filepath
output_file_path = os.path.join(desktop_dir, report)

with open(output_file_path, "w", encoding="utf-8") as output_file:
    for line in output_lines:
        output_file.write(line + "\n") # one line per entry

print(f"Output written to {output_file_path}") # confirmation for user
