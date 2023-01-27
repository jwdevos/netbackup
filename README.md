# netbackup
![Supported Versions](https://img.shields.io/badge/python-3.10+-blue)  
  
The purpose of netbackup is to make configuration backups of network devices from multiple vendors, via multiple communication channels.

### Overview
The overview as given in the project header:
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
#  and Fortinet (FortiGates). If a vendor has netmiko or API support, adding  #
#  them to netbackup should require only a minimum amount of work.            #
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

### Recommended usage
The recommended way to use netbackup is to set up a folder structure something like this:
```
/home/user/python/netbackup/
/home/user/customers/customer-1/backups/
/home/user/customers/customer-1/cfg/
/home/user/customers/customer-1/logs/
```
bla
