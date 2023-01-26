###############################################################################
# 2023 Jaap de Vos
# netbackup (https://github.com/jwdevos/netbackup)
#
# The purpose of netbackup is to make configuration backups of
#  network devices from multiple vendors, via multiple communication channels.
#  At present, SSH (with the Python netmiko library) and HTTP GET (to device
#  API's) are supported.
#
# Netbackup was tested for Mikrotik (RouterOS), UBNT (EdgeSwitch),
#  and Fortinet (FortiGates). If a vendor has netmiko or API support, adding
#  them to netbackup should require only a minimum amount of work.
#
# Netbackup uses CSV and ENV files as input, and backup and log directories
#  for output. The paths for this are configured via CLI arguments.
#  Run netbackup with the -h argument for more information.
#
# At the top of the script, under "Global variables", supported device types
#  and corresponding API URL's and netmiko commands are defined.
#  Here, support for additional vendors can be added. Adding new vendors
#  will probably require some more steps, like introducing support for the
#  enable mode for certain vendors in the netmiko_read function, or support
#  for HTTP POST requests.
#
# If netbackup is of use to you, feel free to use this code and use
#  it as you see fit. Please let me know how you like it.
#
###############################################################################


###############################################################################
# Imports                                                                     #
###############################################################################
import argparse
import csv
import logging
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from netmiko import ConnectHandler


###############################################################################
# Global variables                                                            #
###############################################################################
# Storing the API device types that are supported, and their corresponding
#  API URL's, in an array and a dictionary
api_device_types = [
    'fortinet'
]
api_strings = {
    'fortinet': '/api/v2/monitor/system/config/backup?scope=global&access_token='
}

# Storing the netmiko device types that are supported, and their corresponding
#  commands, in an array and a dictionary
netmiko_device_types = [
    'mikrotik_routeros',
    'ubiquiti_edgeswitch'
]
netmiko_device_commands = {
    'mikrotik_routeros': 'export',
    'ubiquiti_edgeswitch': 'show run'
}


###############################################################################
# Main                                                                        #
###############################################################################
def main():
    # Grabbing the current time for later processing
    start_time = datetime.now()

    # Reading the arguments that the script needs to run with,
    #  to determine the BCK, CSV and ENV paths
    args = read_args()
    print(args)

    # Creating a backup directory for the current day
    today_path = args.bck + get_date()
    if not os.path.exists(today_path):
        os.mkdir(today_path)

    # Loading the env vars
    load_dotenv_file(args.env)

    # Creating an empty array to later store status information in
    status = []

    # Reading the input CSV and doing stuff for each entry
    csv_content = load_csv_file(args.csv)
    for row in csv_content:
        print(row[0] + ' ' + row[2])

        # Creating a variable to store row status
        row_status = [row[0],'NOT OK']
        print(row_status)

        # Variable to track the communication type (SSH via netmiko, or direct API)
        comm_type = ''

        # Variable to store device config data
        device_data = ''

        # Validation of device_type input
        if row[2] not in netmiko_device_types and row[2] not in api_device_types:
            print('Something wrong with device_type for ' + row[0])
            break

        # Set comm_type to netmiko if needed
        if row[2] in netmiko_device_types and row[2] not in api_device_types:
            comm_type = 'netmiko'

        # Set comm_type to api if needed
        if row[2] in api_device_types and row[2] not in netmiko_device_types:
            comm_type = 'api'

        # Calling the right backup function depending on comm_type
        match comm_type:
            case 'netmiko':
                # Defining empty user and password vars
                user = ''
                pw = ''

                # Filling the user and password vars from the .env file
                if row[3] == 'MAIN_USER':
                    user = os.getenv('MAIN_USER')
                    pw = os.getenv('MAIN_PASS')

                # Creating the device object to pass to netmiko
                netmiko_device = {
                    'host': row[1],
                    'username': user,
                    'password': pw,
                    'secret': pw,
                    'global_delay_factor': 4,
                    'device_type': row[2]
                }

                print(netmiko_device['password'])

                # Calling netmiko_read to get device config data
                device_data = netmiko_read(netmiko_device, netmiko_device_commands)

            case 'api':
                # Creating the API URL from the host, the proper string for the
                #  device_type and the key
                api_url = 'https://' + row[1] + api_strings[row[2]] + os.getenv(row[3])

                # Setting requests to disable warnings because network devices
                #  don't have proper certificates
                requests.packages.urllib3.disable_warnings()

                # Running a GET request to the API URL and storing the response
                response = requests.get(api_url, verify=False)

                # Converting the resonse to text and storing it in the
                #  variable for the device config data
                device_data = response.text

        # If device_data isn't empty, save it to a file and set row_status to OK
        if device_data:
            save_file(today_path, row[0], device_data)
            row_status[1] = 'OK'

        # Appending the row_status for this row to the overall status array
        status.append(row_status)

    # Printing the program execution time
    end_time = datetime.now()
    print(f'Total execution time: {end_time - start_time}')


###############################################################################
# Functions                                                                   #
###############################################################################
# Function that returns a formatted date
def get_date():
    return str(datetime.now().date()).replace('-', '')


# Function that returns a formatted time
def get_time():
    return str(datetime.now().time()).replace(':', '')[:6]


# Function that saves a file
def save_file(save_path, device_name, device_data):
    try:
        # Creating a proper filename for the output data of the device
        filename = save_path + '/' + device_name + '.txt'

        # Creating a writable file based on the filename
        file = open(filename, "w+")

        # For line in the list with the output data, write the line to the file
        for line in device_data:
            file.write(line)

        # Closing the file
        file.close()
    except Exception as e:
        print(e)


# Function that reads a CSV file when given a path, and returns the contents
#  as an array without the first (header) line of the CSV
def load_csv_file(csv_path):
    # check if file exists
    if os.path.isfile(csv_path):
        csv_content = []
        with open(csv_path) as csv_file:
            for line in csv.reader(csv_file, delimiter=';'):
                csv_content.append(line)
        csv_content.pop(0)
        return csv_content
    else:
        exit('Something wrong with csv_path')


# Function that reads a .env file when given a path, and makes the
#  variables in the .env file available for use
def load_dotenv_file(env_path):
    # check if file exists
    if os.path.isfile(env_path):
        load_dotenv(env_path)
    else:
        exit('Something wrong with env_path')


# Function that reads the CLI arguments and returns them as a dictionary
def read_args():
    help_bck = '(Required) Provide a backup path, like \'/home/user/backups/\''
    help_csv = '(Required) Provide a CSV file path, like \'/home/user/.csv\''
    help_env = '(Required) Provide a ENV file path, like \'/home/user/.env\''

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bck', help=help_bck)
    parser.add_argument('-c', '--csv', help=help_csv)
    parser.add_argument('-e', '--env', help=help_env)

    args = parser.parse_args()

    if args.bck is None or args.csv is None or args.env is None:
        e = 'Please provide all required arguments. Use \'-h\' for more information'
        exit(e)

    return args


# Function that runs a command on a specified device and saves the output in a file
def netmiko_read(netmiko_device, netmiko_device_commands):
    device_data = ''
    try:
        device_data += '####################################\n'
        device_data += '# Output for device ' + netmiko_device['host'] + '\n'
        device_data += '####################################\n\n'
        netmiko_connect = ConnectHandler(**netmiko_device)
        if netmiko_device['device_type'] == 'mikrotik_routeros':
            output = netmiko_connect.send_command_timing(netmiko_device_commands[netmiko_device['device_type']])
            pass
        else:
            output = netmiko_connect.send_command(netmiko_device_commands[netmiko_device['device_type']])
            pass
        device_data += output
        return device_data

    except Exception as e:
        print(e)


# Making sure main() gets executed when script is called
if __name__ == '__main__':
    main()
