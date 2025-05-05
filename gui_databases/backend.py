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


import json
import os
from hashlib import sha256


class Backend:
    '''
        
    '''

    def __init__(self, _FrontendObj: type['FrontendObj']) -> None:
        '''
        
        '''

        # create object for the interface
        self.FrontendObj = _FrontendObj

        # the configuration file that holds the user credentials
        self.credfile = os.path.join(
            os.path.dirname(__file__),
            'usrcreds.json'
        )
        
        # create default credfile if not present
        if not os.path.exists(self.credfile):
            with open(self.credfile, 'w') as file:
                print('File `usrcreds.json` does not exist, creating now.')

                # default credentials
                default_creds = [
                    {
                        'usr': 'admin',
                        'passwd': sha256('admin'.encode()).hexdigest(),
                        'name': 'Default Admin'
                    }
                ]

                # writes the defaults to the credfile
                json.dump(default_creds, file)
        
        # loads credentials from the file
        with open(self.credfile, 'r') as file:
            self.usrcreds = json.load(file)

        return
    
    def check_creds(self, creds: dict) -> None:
        '''
        Checks whether or not the supplied credentials are valid.
        '''

        for user in self.usrcreds:
            # check if credentials are valid
            if user['usr'] == creds['usr']:
                # check if password is valid for that username
                if user['passwd'] == creds['passwd']:
                    # login successful, so display data entry screen
                    print(f'Login as user `{creds["usr"]}` successful!')
                    self.active_user = user
                    self.FrontendObj.data_entry()
                    
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
