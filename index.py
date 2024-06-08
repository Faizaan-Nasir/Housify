import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class window(QMainWindow):
   def __init__(self, parent = None):
      super(window, self).__init__(parent)
      self.setFixedSize(1120,560)
      self.setWindowTitle("Housify")  
      self.setStyleSheet('background:url("./src/background.png") center no-repeat') 

def main():
   app = QApplication(sys.argv)
   ex = window()
   ex.show()
   sys.exit(app.exec_())
if __name__ == '__main__':
   main()
