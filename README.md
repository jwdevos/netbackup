# netbackup
![Supported Versions](https://img.shields.io/badge/python-3.10+-blue)  
  
The purpose of netbackup is to make configuration backups of network devices from multiple vendors, via multiple communication channels.

<img src="report_screenshot.jpg" width="400">

### Overview
The overview as given in the script header:
```
###############################################################################
#                                                                             #
# 2023 Jaap de Vos                                                            #
# netbackup (https://github.com/jwdevos/netbackup)                            #
#                                                                             #
# The purpose of netbackup is to make configuration backups of                #
#  network devices from multiple vendors, via multiple                        #
#  communication channels. At present, SSH (with the Python netmiko           #
#  library) and HTTP GET (to device API's) are supported.                     #
#                                                                             #
# Netbackup was tested for Mikrotik (RouterOS), UBNT (EdgeSwitch),            #
#  Cisco Small Business switches, and Fortinet (FortiGates).                  #
#  If a vendor has netmiko or API support, adding them to netbackup           #
#  should require only a minimum amount of work.                              #
#                                                                             #
# Netbackup uses CSV and ENV files as input, and backup and log directories   #
#  for output. The paths for this are configured via CLI arguments.           #
#  Run netbackup with the -h argument for more information.                   #
#                                                                             #
# Netbackup can e-mail a status report. The report is based on a              #
#  Jinja2 template which is supplied in the same way as the CSV and           #
#  ENV files. The report gets mailed via SMTP (tested with Office 365).       #
#                                                                             #
# At the top of the script, under "Global variables", supported device types  #
#  and corresponding API URL's and netmiko commands are defined.              #
#  Here, support for additional vendors can be added. Adding new vendors      #
#  will probably require some more steps, like introducing support for the    #
#  enable mode for certain vendors in the netmiko_read function, or support   #
#  for HTTP POST requests.                                                    #
#                                                                             #
# Supported netmiko platforms are documented here:                            #
#  https://github.com/ktbyers/netmiko/blob/develop/PLATFORMS.md               #
#                                                                             #
# If netbackup is of use to you, feel free to take this code and use          #
#  it as you see fit. Please let me know how you like it.                     #
#                                                                             #
###############################################################################
```

### Recommended Usage
The recommended way to use netbackup is to set up a folder structure something like this:
```
/home/user/customers/customer-1/backups/
/home/user/customers/customer-1/cfg/
/home/user/customers/customer-1/logs/
/home/user/customers/customer-1/cronlogs/
```
Next, create a python venv:
```
python3 -m venv netbackup
```
Clone the netbackup repo, and put `main.py` and `requirements.txt` in the netbackup venv folder. The assumed path of the netbackup venv folder in these instructions is `/home/user/python/netbackup/`. Activate the venv and install the requirements:
```
source bin/activate
pip install -r requirements.txt
```
Next, populate the cfg folder with the CSV file, the ENV file, the report template and the run-script. Set the ROOT_PATH variable in the run-script to correspond with the folder structure that was setup before. Don't forget to make the run-script executable:
```
chmod +x /home/user/customers/customer-1/cfg/netbackup-run.sh
```
Now, edit CSV file, the ENV file, and the run-script with variables that work for you, then run the run-script to start the backup procedure. You can also adjust the report template if you wish.  
  
The run-script is also compatible with cron jobs without much hassle, mostly thanks to the explicit paths everywhere. As an example, the following crontab entry will run netbackup every Sunday at 01:00. The output of the cron job will be logged:
```
0 1 * * 0 /home/user/customers/customer-1/cfg/netbackup-run.sh >> /home/user/customers/customer-1/cronlogs/netbackup-cronlog.txt 2>&1
```

### Additional Information
- The current incarnation of netbackup assumes that just a single user/password (the MAIN_USER and MAIN_PASS as set in the ENV file) is enough. If you need per-device flexibility with the user/password, additional logic needs to be added in the script
- Using Mikrotik devices in your CSV will make netbackup considerably slower. This is a result of the way the Mikrotik CLI prompt works when exporting the current configuration, combined with how Python libraries like netmiko have to determine whether or not the export command has finished. I opted for a minute-long hard-coded time-out to make sure Mikrotik backups are working properly in most situations

### Next Up
- Support for HPE ProCurve switches

