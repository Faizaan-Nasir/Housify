import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontDatabase
from PyQt5 import QtCore
from logic import joinGame
from functools import partial

ticket=joinGame('12345')

class ticketMain(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(860,300)
        self.MainUI()
        self.setStyleSheet('color:black;')

    def MainUI(self):
        flag = True
        global buttons
        ticketBox = QScrollArea(self)
        ticketBox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        ticketBox.resize(860,300)
        new = QWidget()
        ticketButtons = QGridLayout()
        buttons = {}
        buttonid = 1

        for y in range(3):
            for x in range(9):
                if flag:
                    color = '#D9D9D9'
                    hovercolor = '#cccccc'
                else:
                    color = '#F8EDD9'
                    hovercolor = '#ebe1ce'

                if (x+1,y+1) in ticket:
                    text = ticket[(x+1,y+1)]
                    buttons[buttonid] = QPushButton(str(text),self)
                    buttons[buttonid].setStyleSheet('''QPushButton{
                                                            font-family: poppins;
                                                            font-size: 30px; 
                                                            border: 0px;'''
                                                            f"background: {color};"
                                                            '''}
                                                            QPushButton::hover{'''
                                                            f"background: {hovercolor};"
                                                            "}")
                    buttons[buttonid].setFixedSize(80,80)
                    ticketButtons.addWidget(buttons[buttonid],y,x)
                    buttons[buttonid].clicked.connect(partial(self.disable,buttonid))
                    buttonid += 1
                else:
                    tempButton = QPushButton('',self)
                    tempButton.setStyleSheet('''QPushButton{
                                        font-family: poppins;
                                        font-size: 30px; 
                                        border: 0px;'''
                                        f"background: {color};"'''}''')
                    tempButton.setFixedSize(80,80)
                    ticketButtons.addWidget(tempButton,y,x)
                flag = not flag

        new.setLayout(ticketButtons)
        ticketBox.setWidget(new)
        ticketBox.show()
    
    def disable(self,buttonid):
        buttons[buttonid].setStyleSheet('color:red')

def main():
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-Regular.ttf')
    QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-ExtraBold.ttf')
    QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-SemiBold.ttf')
    ex = ticketMain()
    ex.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()