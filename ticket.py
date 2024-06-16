import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontDatabase
from logic import joinGame

ticket=joinGame('12345')

class ticketMain(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(720,240)
        self.ticketImage()

    def ticketImage(self):
        self.buttons=[]
        flag=True
        # for loop that introduces buttons appropriately
        for y in range(3):
            for x in range(9):
                if flag:
                    color='#D9D9D9'
                    hovercolor='#cccccc'
                else:
                    color='#F8EDD9'
                    hovercolor='#ebe1ce'
                if (x+1,y+1) in ticket:
                    text=ticket[(x+1,y+1)]
                else:
                    text=''
                tempButton=QPushButton(str(text),self)
                tempButton.setStyleSheet('''QPushButton{
                                        font-family: poppins;
                                        font-size: 30px; 
                                        border: 0px;'''
                                        f"background: {color};"
                                        '''}
                                        QPushButton::hover{'''
                                        f"background: {hovercolor};"
                                        "}")
                tempButton.setFixedSize(80,80)
                tempButton.move(x*80,y*80)
                flag= not flag

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