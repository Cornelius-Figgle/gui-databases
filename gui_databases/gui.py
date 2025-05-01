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

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout
)


class GUI_Interface(QMainWindow):
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

    def draw_screen(self) -> None:
        '''
            
        '''

        ...

        return

    def login(self) -> None:
        '''
            
        '''

        ...

        return


def main() -> None:
    '''
    Controls the main program flow.
    '''

    # creates the window
    AppObj = QApplication([])
    WindowObj = GUI_Interface(AppObj)
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
