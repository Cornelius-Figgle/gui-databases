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

from PyQt6 import sip
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel, 
    QLineEdit,
    QHBoxLayout,
    QPushButton,
    QMessageBox
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
        self.setWindowTitle('GUI Databases')
        
        # creates a widget to hold our layout
        self.layout_widget = QWidget()
        self.setCentralWidget(self.layout_widget)

        # creates a layout to hold our widgets
        self.layout_current = QGridLayout()
        self.layout_widget.setLayout(self.layout_current)

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

    def data_entry(self) -> None:
        '''
        Handles the main content window.
        '''

        # reinitialise the layout
        self.clear_screen()
        
        # stores all the widgets for this screen
        widget_dict = dict()

        # creates a title and adds it to the window's layout
        widget_dict['title_text'] = QLabel(
            f'<h1>Database Manager for {self.BackendObj.active_user}</h1>'
        )
        self.layout_current.addWidget(widget_dict['title_text'], 0, 0)

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
