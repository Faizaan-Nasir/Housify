import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontDatabase
from PyQt5 import QtCore
from functools import partial

# this is literally a ticket widget imported to the "Playing a Game" window
class ticketMain(QWidget):
    def __init__(self,ticket,parent):
        self.ticket=ticket
        super().__init__(parent)
        self.setFixedSize(634,214)
        self.MainUI()
        self.setStyleSheet('color:black;')

    def MainUI(self):
        flag = True
        global buttons
        ticketBox = QScrollArea(self)
        ticketBox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        ticketBox.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        ticketBox.resize(634,214)
        ticketBox.setStyleSheet('border: 2px solid black;')
        new = QWidget()
        ticketButtons = QGridLayout()
        ticketButtons.setSpacing(0)
        ticketButtons.setContentsMargins(0,0,0,0)
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

                if (x+1,y+1) in self.ticket:
                    text = self.ticket[(x+1,y+1)]
                    buttons[buttonid] = QPushButton(str(text),self)
                    buttons[buttonid].setStyleSheet('''QPushButton{
                                                            font-family: poppins;
                                                            font-size: 30px; 
                                                            font-weight: 500;
                                                            border: 0px;'''
                                                            f"background: {color};"
                                                            '''}
                                                            QPushButton::hover{'''
                                                            f"background: {hovercolor};"
                                                            "}")
                    buttons[buttonid].setFixedSize(70,70)
                    ticketButtons.addWidget(buttons[buttonid],y,x)
                    buttons[buttonid].clicked.connect(partial(self.disable,buttonid))
                    buttonid += 1
                else:
                    tempButton = QPushButton('',self)
                    tempButton.setStyleSheet('''QPushButton{
                                        font-family: poppins;
                                        font-size: 30px; 
                                        font-weight: 500;
                                        border: 0px;'''
                                        f"background: {color};"'''}''')
                    tempButton.setFixedSize(70,70)
                    ticketButtons.addWidget(tempButton,y,x)
                flag = not flag

        new.setLayout(ticketButtons)
        ticketBox.setWidget(new)
        ticketBox.show()
    
    def disable(self,buttonid):
        buttons[buttonid].setStyleSheet('''font-family: poppins;
                                        font-size: 30px;
                                        border: 0px;
                                        font-weight: 500;
                                        background: #c9c9c7;
                                        color: #b8b8b8;''')

# uncomment the following if u wish to style it here
# def main():
#     app = QApplication(sys.argv)
#     QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-Regular.ttf')
#     QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-ExtraBold.ttf')
#     QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-SemiBold.ttf')
#     temptick=logic.generateTicket('112233')
#     ex = ticketMain(temptick)
#     ex.show()
#     sys.exit(app.exec_())

# if __name__=='__main__':
#     main()