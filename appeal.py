import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import pyqtSignal, QObject
import ticket
import logic
import index

class appeal(QObject):
    appealSignal = pyqtSignal(list)
    def sendAppeal(self, appealDetails):
        self.appealSignal.connect(index.hostingGame.appealResult)
        self.appealSignal.emit(appealDetails)

class appealWindow(QWidget):
    def __init__(self, appeal, player, ticketId, calledNums):
        super().__init__()
        self.setFixedSize(700,400)
        self.setWindowTitle('Housify - Appeal')
        self.setStyleSheet('background-color: #F0E4CD')
        self.appeal = appeal
        self.player = player
        self.ticketId = ticketId
        self.calledNums = calledNums
        self.MainUI()
    
    def MainUI(self):
        self.title = QLabel(f"{self.player} appeals  :   {self.appeal}",self)
        self.title.setStyleSheet('font-size: 22px; font-family: "Poppins"; color: black;')
        self.title.move(33,25)

        self.displayTicket=ticket.ticketMain(logic.generateTicket(self.ticketId), self, 'host', self.calledNums)
        self.displayTicket.move(33,90)
        self.displayTicket.parent=self
        self.displayTicket.show()

        self.approveButton = QPushButton('Yes, appeal is right.',self)
        self.approveButton.resize(250,50)
        self.approveButton.setStyleSheet('''QPushButton{
                                        font-family: Poppins;
                                        font-size: 18px;
                                        color: black;
                                        font-weight: 500;
                                        background-color: #77DD81;
                                        border: 2px solid black;
                                        }''')
        self.approveButton.move(87,325)
        self.approveButton.clicked.connect(lambda: appeal.sendAppeal(self,['Approved',self.appeal]))

        self.declineButton = QPushButton('No, appeal is wrong.',self)
        self.declineButton.resize(250,50)
        self.declineButton.setStyleSheet('''QPushButton{
                                        font-family: Poppins;
                                        font-size: 18px;
                                        color: black;
                                        font-weight: 500;
                                        background-color: #F46363;
                                        border: 2px solid black;
                                        }''')
        self.declineButton.move(362,325)
        self.declineButton.clicked.connect(lambda: appeal.sendAppeal(self,['Declined',self.appeal]))

# class AppealSignal(QWidget):
#     appealSignal = pyqtSignal(str, str)

    # @QtCore.pyqtSlot(dict) 
    # def react(self, msg)  :
    #     if msg['event'] == 'appeal':
    #         global appealName, appealUser, gameCode
    #         appealName = msg['name']
    #         appealUser = msg['username']
    #         gameCode = msg['code']

def main():
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont('./src/fonts/Paytone_One/PaytoneOne-Regular.ttf')
    QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-Regular.ttf')
    QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-ExtraBold.ttf')
    QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-SemiBold.ttf')
    win = appealWindow('Full House','Aditi','T112233',[1,2,3,52,55,69,72,76])
    win.show()
    code = app.exec_()
    sys.exit(code)

if __name__ == '__main__':
    main()