import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontDatabase

# main window
class window(QMainWindow):
   def __init__(self, parent = None):
      super(window, self).__init__(parent)
      self.setFixedSize(1120,560)
      self.setWindowTitle("Housify")  
      self.setStyleSheet('background:url("./src/background.png") center no-repeat') 
      self.mainTitle=QLabel("HOUSIFY",self)
      self.mainTitle.setFixedWidth(1120)
      self.mainTitle.setFixedHeight(50)
      self.mainTitle.move(0,200)
      self.mainTitle.setAlignment(QtCore.Qt.AlignCenter)
      self.mainTitle.setStyleSheet("font-family: Paytone One; background: transparent; font-size:45px")

def main():
   app = QApplication(sys.argv)
   QFontDatabase.addApplicationFont('./src/fonts/Paytone_One/PaytoneOne-Regular.ttf')
   QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-Regular.ttf')
   ex = window()
   ex.show()
   sys.exit(app.exec_())
   
if __name__ == '__main__':
   main()
