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


import sys
from hashlib import sha256

import qtawesome as qta
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel, 
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QStatusBar,
    QToolBar
)

from backend import Backend


class Frontend(QMainWindow):
    '''
    Handles the interface to the database.
    '''

    def __init__(self, _AppObj: type[QApplication]) -> None:
        '''
        Sets up the gui and handles the main program loop after exec is
        handed over.
        '''

        # initialises from QMainWindow
        super().__init__()

        # initalise the backend
        self.BackendObj = Backend(self)
       
        # stores the QApplication object for later use
        self.AppObj = _AppObj

        # sets title
        self.setWindowTitle('Account Manager')
        
        # creates a widget to hold our layout
        self.layout_widget = QWidget()
        self.setCentralWidget(self.layout_widget)

        # creates a layout to hold our widgets
        self.layout_current = QGridLayout()
        self.layout_widget.setLayout(self.layout_current)

        # create blank toolbar dict
        self.toolbar_dict = dict()

        # start the login process
        self.login()

        return

    def _quit(self) -> None:
        '''
        Gracefully exits the application.
        '''

        self.AppObj.quit()

        return

    def clear_screen(self) -> None:
        '''
        Clears the layout to allow new widgets to be added.
        '''

        # a widget is deleted when its parent is deleted
        # thus we iterate over the layout and remove widgets' parents
        # in reverse order so the order of the widgets doesn't change
        for i in reversed(range(self.layout_current.count())): 
            self.layout_current.itemAt(i).widget().setParent(None)

        # remove toolbar
        for widget in self.toolbar_dict:
            self.toolbar_dict[widget].setParent(None)

        return
        
    def raise_error(self, title: str, content: str) -> None:
        '''
        Informs the user of an error, usually used in conjunction with
        input validation.
        '''

        QMessageBox.warning(self, title, content)

        return

    def login(self) -> None:
        '''
        Handles the login window.
        '''
        
        # reinitialise the layout
        self.clear_screen()

        # stores all the widgets for this screen
        widget_dict = dict()

        # creates a title and adds it to the window's layout
        widget_dict['title_text'] = QLabel('<h1>Login to the database</h1>')
        self.layout_current.addWidget(widget_dict['title_text'], 0, 0)

        # grid to hold the labels and their input boxes
        widget_dict['cred_grid_widget'] = QWidget()
        widget_dict['cred_grid_layout'] = QGridLayout()
        
        widget_dict['usr_label'] = QLabel('Username: ')
        widget_dict['usr_input'] = QLineEdit()
        widget_dict['passwd_label'] = QLabel('Password: ')
        widget_dict['passwd_input'] = QLineEdit()
        widget_dict['passwd_input'].setEchoMode(QLineEdit.EchoMode.Password)
        
        widget_dict['cred_grid_layout'].addWidget(
            widget_dict['usr_label'],
            0, 0
        )
        widget_dict['cred_grid_layout'].addWidget(
            widget_dict['usr_input'],
            0, 1
        )
        widget_dict['cred_grid_layout'].addWidget(
            widget_dict['passwd_label'],
            1, 0
        )
        widget_dict['cred_grid_layout'].addWidget(
            widget_dict['passwd_input'],
            1, 1
        )
        
        widget_dict['cred_grid_widget'].setLayout(
            widget_dict['cred_grid_layout']
        )

        self.layout_current.addWidget(widget_dict['cred_grid_widget'], 1, 0)

        # hbox to buffer the submit button to the right
        widget_dict['submit_hbox_widget'] = QWidget()
        widget_dict['submit_hbox_layout'] = QHBoxLayout()

        widget_dict['submit_hbox_layout'].addWidget(
            QWidget()
        )
        widget_dict['submit_hbox_layout'].addWidget(
            QWidget()
        )

        widget_dict['submit_button'] = QPushButton('Login')
        widget_dict['submit_button'].clicked.connect(
            lambda event: self.BackendObj.check_creds(
                creds={
                    'usr': widget_dict['usr_input'].text().lower(),
                    'passwd': sha256(
                        widget_dict['passwd_input'].text().encode()
                    ).hexdigest()
                }
            )
        )
        widget_dict['submit_hbox_layout'].addWidget(
            widget_dict['submit_button']
        )

        widget_dict['submit_hbox_widget'].setLayout(
            widget_dict['submit_hbox_layout']
        )
        
        self.layout_current.addWidget(widget_dict['submit_hbox_widget'], 2, 0)

        # set the layout
        self.layout_widget.setLayout(self.layout_current)

        return

    def main_menu(self) -> None:
        '''
        Handles the main content window.
        '''

        # reinitialise the layout
        self.clear_screen()
        
        # stores all the widgets for this screen
        widget_dict = dict()

        # main toolbar
        self.toolbar_dict['main'] = QToolBar('Main toolbar')
        self.toolbar_dict['main'].setIconSize(QSize(16, 16))
        self.toolbar_dict['main'].setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextBesideIcon
        )
        self.toolbar_dict['main'].setFloatable(True)
        self.addToolBar(self.toolbar_dict['main'])

        # create new account
        self.toolbar_dict['add'] = QAction(
            qta.icon('mdi.account-plus'),
            '&Add User',
            self
        )
        self.toolbar_dict['add'].setStatusTip('Create a new user')
        self.toolbar_dict['main'].addAction(self.toolbar_dict['add'])

        self.toolbar_dict['main'].addSeparator()

        # return to login screen
        self.toolbar_dict['logout'] = QAction(
            qta.icon('mdi.account-arrow-right'),
            '&Logout',
            self
        )
        self.toolbar_dict['logout'].setStatusTip('Return to login screen')
        self.toolbar_dict['logout'].triggered.connect(self.login)
        self.toolbar_dict['main'].addAction(self.toolbar_dict['logout'])

        # quit program
        self.toolbar_dict['exit'] = QAction(
            qta.icon('mdi.exit-run'),
            '&Exit',
            self
        )
        self.toolbar_dict['exit'].setStatusTip('Exit the program')
        self.toolbar_dict['exit'].triggered.connect(self._quit)
        self.toolbar_dict['main'].addAction(self.toolbar_dict['exit'])
        
        # status bar
        widget_dict['statusbar'] = QStatusBar(self)
        self.setStatusBar(widget_dict['statusbar'])
        widget_dict['statusbar'].showMessage(
            'Successfully logged in as '
                +f'"{self.BackendObj.active_user["usr"]}"',
            3000
        ) 
        
        # vbox to hold the accounts list
        widget_dict['account_vbox_widget'] = QWidget()
        widget_dict['account_vbox_layout'] = QVBoxLayout()

        # list of widgets for each account
        widget_dict['account_hboxes'] = list()

        # only show all accounts to admins
        if self.BackendObj.active_user['admin']:
            # all accounts
            users_to_show = self.BackendObj.usrcreds
        else:
            # only their account
            users_to_show = [self.BackendObj.active_user]

        for account in users_to_show:
            widget_dict['account_hboxes'].append(
                {
                    'widget': QWidget(),
                    'layout': QHBoxLayout()
                }
            )

            # username
            widget_dict['account_hboxes'][-1]['usr'] = QLabel(
                account['usr']
            )
            widget_dict['account_hboxes'][-1]['layout'].addWidget(
                widget_dict['account_hboxes'][-1]['usr']
            )

            # button to open the management page for that user
            widget_dict['account_hboxes'][-1]['usr_view'] = QPushButton(
                'View'
            )
            widget_dict['account_hboxes'][-1]['layout'].addWidget(
                widget_dict['account_hboxes'][-1]['usr_view']
            )

            # button to open the management page for that user
            widget_dict['account_hboxes'][-1]['usr_manage'] = QPushButton(
                'Manage'
            )
            widget_dict['account_hboxes'][-1]['layout'].addWidget(
                widget_dict['account_hboxes'][-1]['usr_manage']
            )

            # set hbox layout
            widget_dict['account_hboxes'][-1]['widget'].setLayout(
                widget_dict['account_hboxes'][-1]['layout']
            )

            # add the hbox to the layout, uses position len()-1
            self.layout_current.addWidget(
                widget_dict['account_hboxes'][-1]['widget'],
                len(widget_dict['account_hboxes']) - 1, 0
            )

        # set the layout
        self.layout_widget.setLayout(self.layout_current)

        return


def main() -> None:
    '''
    Controls the main program flow.
    '''

    # creates the window
    AppObj = QApplication([])
    WindowObj = Frontend(AppObj)
    WindowObj.show()

    # hands control of the program flow over to Qt
    AppObj.exec()
   
    return


# only execute if called directly
if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        sys.exit()
