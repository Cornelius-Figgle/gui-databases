#!/usr/bin/env python3 

'''
# GUI Databases Project (PyQt6)
'''

__version__ = '0.1.0'  
__author__ = 'Cornelius-Figgle'
__email__ = 'max@fullimage.net'
__maintainer__ = 'Cornelius-Figgle'
__copyright__ = 'Copyright (c) 2025 Max Harrison'
__license__ = 'MIT'
__status__ = 'Development'
__credits__ = ['Max Harrison']

# source code: https://github.com/Cornelius-Figgle/gui-databases


import os
from hashlib import sha256

import mysql.connector


class Backend:
    '''
        
    '''

    def __init__(self, _FrontendObj: type['FrontendObj']) -> None:
        '''
        Sets up the database for use.
        '''

        # create object for the interface
        self.FrontendObj = _FrontendObj

        # sets global options for DB connections
        self.db_opts = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',
            'use_pure': True  # https://stackoverflow.com/a/79391956/19860022
        }

        # create db if it doesn't already exist
        print('Creating `accounts_db` if it does not exist already.')
        query_text = '''
            CREATE DATABASE IF NOT EXISTS accounts_db
        '''
        self.sql_query(query_text)

        # set db in global options
        self.db_opts['database'] = 'accounts_db'
        
        # create table if it doesn't already exist
        print('Creating `accountsTbl` if it does not exist already.')
        query_text = '''
            CREATE TABLE IF NOT EXISTS accountsTbl (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username TINYTEXT NOT NULL,
                passwordHash CHAR(64) NOT NULL,
                displayName TINYTEXT NOT NULL,
                admin BOOLEAN NOT NULL     
            )
        '''
        self.sql_query(query_text, commit=True)

        # checks if the table is populated
        query_text = '''
            SELECT EXISTS (
                SELECT 1
                FROM accountsTbl    
            )
        '''
        if not self.sql_query(query_text)[0][0]:
            # create default account if table empty
            print('Creating default user `admin`.')
            query_text = f'''
                INSERT INTO accountsTbl(username, passwordHash, displayName, admin)
                VALUES
                    ("admin", "{sha256('admin'.encode()).hexdigest()}", "Default Admin", TRUE)
            '''
            self.sql_query(query_text, commit=True)

        return

    def sql_query(self,
            query: str,
            opts: dict = None,
            commit: bool = False) -> str:
        
        '''
        Wrapper to query the DB.
        '''

        # set default options
        opts = self.db_opts if opts is None else opts

        # check if tables and default account need creating
        try:
            # connect to DB
            with mysql.connector.connect(**opts) as conn:
                print('ze database device has connected!?!/!?11..1/?1')

                # run the query
                with conn.cursor(buffered=True) as cursor:
                    cursor.execute(query)

                    # required to save changes
                    if commit:
                        conn.commit()
                    
                    response = cursor.fetchall()

            # return the response
            return response
        
        except mysql.connector.Error as e:
            print(e)
            return
    
    def check_creds(self, creds: dict) -> None:
        '''
        Checks whether or not the supplied credentials are valid.
        '''

        # check the provided credetials against each account in the db
        query_text = '''
            SELECT id, username, passwordHash
            FROM accountsTbl
        '''
        for account in self.sql_query(query_text):
            # check if the username is valid
            if account[1] == creds['usr']:
                # check if password is valid for that username
                if account[2] == creds['passwd']:
                    # login successful, so display data entry screen
                    print(f'Login as user `{creds["usr"]}` successful!')
                    self.active_user = account[0]
                    self.FrontendObj.main_menu()
                    
                    break
                else:
                    # log error to stdout
                    print('Login attempt unsuccessful: invalid password for'
                          +f'user `{creds["usr"]}`.')

                    # inform the user of the error
                    self.FrontendObj.raise_error(
                        'Invalid credentials',
                        'The provided password is incorrect, please try again'
                    )

                    break
        else:
            # log error to stdout
            print('Login attempt unsuccessful: invalid username '
                  +f'`{creds["usr"]}`.')

            # inform the user of the error
            self.FrontendObj.raise_error(
                'Invalid credentials',
                'The provided username is invalid, please try again'
            )

        return
