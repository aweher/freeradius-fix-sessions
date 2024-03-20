# fix-sessions.py

This Python script is used to update session records in a MySQL database. It is designed to run continuously, updating records as needed based on the current time and the start time of each session.

## Requirements

This script requires Python3 and the mysql-connector-python package.
You can install this package using pip:

```bash
pip install -U -r requirements.txt
```

The script will try to find a local `my.cnf` file to read the database credentials from. If this file is not found, the script will try to use the file `.my.cnf` from your `$HOME` directory.

The `my.cnf` file should look like this:

```ini
[client]
user=mysql-server-username
password=mysq-server-password
host=mysql-server-ip
database=-mysql-radius-database
```

## How it works

The script first establishes a connection to the MySQL database. It then selects a record from the radacct table where the acctstoptime is NULL.
The acctstarttime is retrieved from the selected record and the acctsessiontime is calculated as the difference between the current time and the acctstarttime.
The script then updates the acctstoptime, acctsessiontime, acctterminatecause, and lastupdate fields in the radacct table for the selected record.
If no records are found that match the criteria, a message is printed to the console.
If an error occurs while connecting to the MySQL database, the error is printed to the console.
Finally, the script ensures that the database connection and cursor are closed.

## Usage

To run the script, simply execute it from the command line:
Please note that the script will run indefinitely until manually stopped.

```bash
python3 fix-sessions.py
```

## Troubleshooting

If you encounter an error while running the script, please check the console output for details.

Common issues include incorrect database credentials or network connectivity issues.
