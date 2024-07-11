import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontDatabase

class theGrid(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setFixedSize(400,360)
        self.allNums = {}
        self.MainUI()

    def MainUI(self):
        layout=QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        key=1
        for x in range(1,10):
            for y in range(1,11):
                number=QLabel(f'{(x-1)*10+y}')
                number.setFixedSize(40,40)
                number.setStyleSheet("color: black; font-family: poppins; font-size: 20px; font-weight: 500; border: 1px solid black; background: #FFF5DB; color : black;")
                number.setAlignment(QtCore.Qt.AlignCenter)
                layout.addWidget(number,x-1,y-1)
                self.allNums[key]=number
                key+=1
        self.setLayout(layout)

    def updateStyle(self, key):
        self.allNums[key].setStyleSheet("color: black; font-family: poppins; font-size: 20px; font-weight: 500; border: 1px solid black; background: #82BCF2; color : black;")
# def main():
#     app = QApplication(sys.argv)
#     QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-Regular.ttf')
#     QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-ExtraBold.ttf')
#     QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-SemiBold.ttf')
#     ex = theGrid()
#     ex.show()
#     sys.exit(app.exec_())

# if __name__=='__main__':
#     main()