import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontDatabase , QPixmap , QPalette , QBrush

# main window
class mainWindow(QWidget):
   def __init__(self):
      super().__init__()
      self.setFixedSize(1120,560)
      self.setWindowTitle("Housify")
      pixmap = QPixmap('./src/background.png')
      palette = self.palette()
      palette.setBrush(QPalette.Background, QBrush(pixmap))
      self.setPalette(palette)
      
      # Title
      self.mainTitle=QLabel("HOUSIFY",self)
      self.mainTitle.setFixedSize(1120,50)
      self.mainTitle.move(0,210)
      self.mainTitle.setAlignment(QtCore.Qt.AlignCenter)
      self.mainTitle.setStyleSheet("font-family: Paytone One; background: transparent; font-size:60px")

      # Host a Game Button
      self.hostGame=QPushButton('Host a Game',self)
      self.hostGame.setStyleSheet('''QPushButton{
                                  font-family: Poppins; 
                                  font-size: 21px; 
                                  background: #69B1F4; 
                                  border: 2px solid black;
                                  }
                                  QPushButton::hover{
                                  background: #63a9eb;
                                  }''')
      self.hostGame.setFixedSize(200,55)
      self.hostGame.move(340,310)
      #self.hostGame.clicked.connect()

      # Join a Game Button
      self.joinGame=QPushButton('Join a Game',self)
      self.joinGame.setStyleSheet('''QPushButton{
                                  font-family: Poppins; 
                                  font-size: 21px; 
                                  background: #69B1F4; 
                                  border: 2px solid black;
                                  }
                                  QPushButton::hover{
                                  background: #63a9eb;
                                  }''')
      self.joinGame.setFixedSize(200,55)
      self.joinGame.move(580,310)
      #self.joinGame.clicked.connect()

      # Copyrights
      self.copyright=QLabel('© All rights reserved, Housify Pvt Ltd, 2024',self)
      self.copyright.setStyleSheet('font-family: Poppins; font-size: 10px; background: transparent')
      self.copyright.setFixedWidth(560)
      self.copyright.setAlignment(QtCore.Qt.AlignCenter)
      self.copyright.move(280,390)

def main():
   app = QApplication(sys.argv)
   QFontDatabase.addApplicationFont('./src/fonts/Paytone_One/PaytoneOne-Regular.ttf')
   QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-Regular.ttf')
   ex = mainWindow()
   ex.show()
   sys.exit(app.exec_())
   
if __name__ == '__main__':
   main()
