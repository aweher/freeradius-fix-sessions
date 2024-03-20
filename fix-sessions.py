#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import Error
from datetime import datetime
import configparser
import os

def read_db_config(local_filename='my.cnf', home_filename='~/.my.cnf', section='client'):
    """Read database configuration from local or home directory."""
    # Check for local my.cnf file first
    local_filename = os.path.join(os.getcwd(), local_filename)
    home_filename = os.path.expanduser(home_filename)
    
    if os.path.exists(local_filename):
        filename = local_filename
    else:
        filename = home_filename

    # Create a parser
    parser = configparser.ConfigParser()
    # Try to read the configuration file
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db

def update_record():
    try:
        # Read connection details from my.cnf or ~/.my.cnf
        db_config = read_db_config()
        
        # Connect to the MySQL database
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            
            cursor = connection.cursor(dictionary=True)
            
            # Get username input
            username = input("Enter the username to search for: ")
            
            # Fetch records with acctstoptime NULL or empty
            query = """
            SELECT * FROM radacct 
            WHERE username = %s AND (acctstoptime IS NULL OR acctstoptime = '')
            """
            cursor.execute(query, (username,))
            records = cursor.fetchall()
            
            if records:
                for i, record in enumerate(records, start=1):
                    print(f"{i}. RadID: {record['radacctid']}, Start: {record['acctstarttime']}, IP: {record['framedipaddress']}")
                
                selection = int(input("Select the record number to fix (0 to cancel): "))
                if selection == 0:
                    print("Operation cancelled.")
                    return
                
                # Confirm before proceeding
                confirm = input("Proceed with fixing the selected record? (y/n): ").lower()
                if confirm != 'y':
                    print("Operation cancelled.")
                    return
                
                selected_record = records[selection-1]
                now = datetime.now()
                
                # No need to parse starttime, as it's already a datetime object
                starttime = selected_record['acctstarttime']
                acctsessiontime = int((now - starttime).total_seconds())

                # Update query
                update_query = """
                UPDATE radacct SET 
                acctstoptime = %s, 
                acctsessiontime = %s, 
                acctterminatecause = 'admin fixed', 
                lastupdate = %s 
                WHERE radacctid = %s
                """
                
                cursor.execute(update_query, (now.strftime('%Y-%m-%d %H:%M:%S'), acctsessiontime, now.strftime('%Y-%m-%d %H:%M:%S'), selected_record['radacctid']))
                connection.commit()
                
                print("Record updated successfully.")
            else:
                print("No records found with the specified criteria.")
                
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    while True:
        update_record()
