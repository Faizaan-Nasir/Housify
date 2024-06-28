import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontDatabase
import ticket
import logic

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
        self.displayTicket.move(33,110)
        self.displayTicket.parent=self
        self.displayTicket.show()

        print(self.calledNums)


    # @QtCore.pyqtSlot(dict) 
    # def react(self, msg)  :
    #     if msg['event'] == 'appeal':
    #         global appealName, appealUser, gameCode
    #         appealName = msg['name']
    #         appealUser = msg['username']
    #         gameCode = msg['code']

# def main():
#     app = QApplication(sys.argv)
#     QFontDatabase.addApplicationFont('./src/fonts/Paytone_One/PaytoneOne-Regular.ttf')
#     QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-Regular.ttf')
#     QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-ExtraBold.ttf')
#     QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-SemiBold.ttf')
#     win = appealWindow('Full House','Aditi','T112233')
#     win.show()
#     code = app.exec_()
#     sys.exit(code)

# if __name__ == '__main__':
#     main()