#!/bin/bash

source_log_file="/var/log/apache2/access.log" # This is the source log to monitor

destination="/home/student/Desktop/logAnalysis" #Where to store the extracted logs

pattern_of_interest="127\.0\.0\.1|([0-9]{1,3}\.){3}[0-9]{1,3}" #this can be whatever pattern you are interested in, in this case, a RegEx for an IP address or my localhost IP

dest_file="$destination/filtered_$(date +'%Y-%m-%d').log" #This builds a destination file name; creates one file per day
mkdir -p "$destination" #makes directory at variable destination if that path doesn't already exist
logHawk="/usr/local/bin/logHawk.py" #LogHawk analysis * Make sure logHawk.py is saved here

# Grab the matching lines to the selected pattern of interest since the last run

# "tail -n 100 will gather the most recent 100 lines of the log file - testing purposes, increase/decrease based on your needs
# grep -F completes fixed-string match - can switch to egrep or grep -E for RegEx.
tail -n 100 "$source_log_file" | grep -E "$pattern_of_interest" >> "$dest_file"

#After the filtered log data has been passed to the dest_file, run logHawk with the fresh dest_file
"$logHawk" "$dest_file"
