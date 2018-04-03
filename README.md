# Summary

This program takes publicly available EDGAR files, reads them line-by-line, and then identifies when a user visits, how many documents they access during their visit, and how long they stay. It then writes this information to a txt file. Each line represents a user, when they accessed the site, when they left it, how long they stayed, and how many documents they looked at in that time.

# Dependencies
This program is written in Python, and uses the following packages:
os
csv
datetime
collections


## Input files

### `log.csv`

The data for this challenge comes from the SEC. The SEC provides weblogs stretching back years and is [regularly updated, although with a six month delay](https://www.sec.gov/dera/data/edgar-log-file-data-set.html). This program is designed to process one set of those files.

### `inactivity_period.txt`
This file holds a single integer value denoting the period of inactivity (in seconds) to identify a user session. 

## Output file

The output file, `sessionization.txt` contains

* IP address of the user exactly as found in `log.csv`
* date and time of the first webpage request in the session (yyyy-mm-dd hh:mm:ss)
* date and time of the last webpage request in the session (yyyy-mm-dd hh:mm:ss)
* duration of the session in seconds
* count of webpage requests during the session

