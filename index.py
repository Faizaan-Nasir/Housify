import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontDatabase , QPixmap , QPalette , QBrush
import pyperclip
import logic

# enter username
class usernameWindow(QWidget):
   def __init__(self):
      super().__init__()
      self.setFixedSize(500,200)
      self.setWindowTitle("Housify")
      self.mainUI()
   
   def openCloseWindow(self,username):
      global name
      with open('username.txt','w') as file:
         file.write(username)
      name=username
      self.hide()
      self.newin=mainWindow()
      self.newin.show()

   def mainUI(self):
      self.usernameText=QLineEdit(self)
      self.usernameText.setStyleSheet("color: black; font-family: Poppins; font-size: 21px; background: #D7D7D7; border: 2px solid black;")
      self.usernameText.setFixedSize(250,55)
      self.usernameText.move(125,35)
      self.usernameText.setAlignment(QtCore.Qt.AlignCenter)
      self.usernameText.setPlaceholderText('Username')
      self.usernameText.setFocusPolicy(0x2)
      
      self.submit=QPushButton('Submit',self)
      self.submit.setStyleSheet('''QPushButton{
                                 font-family: Poppins; 
                                 font-size: 21px; 
                                 background: #69B1F4; 
                                 border: 2px solid black;
                                 color: black;
                                 }
                                 QPushButton::hover{
                                 background: #63a9eb;}''')
      self.submit.setFixedSize(150,55)
      self.submit.move(175,115)
      self.submit.clicked.connect(lambda: self.openCloseWindow(self.usernameText.text()))

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
      self.MainUI()
   
   # function to show joinGameWindow
   def joinGameButton(self):
      self.newWin = joinGameWindow()
      self.newWin.show()
      # self.hide()
   
   # function to show hostGameWindow
   def hostGameButton(self):
      self.newWin = hostGameWindow()
      self.newWin.show()
      # self.hide()

   def MainUI(self):
      # HOUSIFY
      self.mainTitle=QLabel("HOUSIFY",self)
      self.mainTitle.setFixedSize(1120,52)
      self.mainTitle.move(0,210)
      self.mainTitle.setAlignment(QtCore.Qt.AlignCenter)
      self.mainTitle.setStyleSheet("font-family: Paytone One; font-weight: 600; background: transparent; font-size:60px; color: black;")
      
      # Host a Game Button
      self.hostGame=QPushButton('Host a Game',self)
      self.hostGame.setStyleSheet('''QPushButton{
                                 font-family: Poppins; 
                                 font-size: 21px; 
                                 background: #69B1F4; 
                                 border: 2px solid black;
                                 color: black;
                                 }
                                 QPushButton::hover{
                                 background: #63a9eb;}''')
      self.hostGame.setFixedSize(200,55)
      self.hostGame.move(340,310)
      self.hostGame.clicked.connect(self.hostGameButton)

      # Join a Game Button
      self.joinGame=QPushButton('Join a Game',self)
      self.joinGame.setStyleSheet('''QPushButton{
                                 font-family: Poppins; 
                                 font-size: 21px; 
                                 background: #69B1F4; 
                                 border: 2px solid black;
                                 color: black;
                                 }
                                 QPushButton::hover{
                                 background: #63a9eb;}''')
      self.joinGame.setFixedSize(200,55)
      self.joinGame.move(580,310)
      self.joinGame.clicked.connect(self.joinGameButton)

      # Copyrights
      self.copyright=QLabel('© All rights reserved, Housify Pvt Ltd, 2024',self)
      self.copyright.setStyleSheet('font-family: Poppins; font-size: 10px; background: transparent; color: black;')
      self.copyright.setFixedWidth(560)
      self.copyright.setAlignment(QtCore.Qt.AlignCenter)
      self.copyright.move(280,390)

# join a game window
class joinGameWindow(QWidget):
   def __init__(self):
      super().__init__()
      self.setFixedSize(1120,560)
      self.setWindowTitle("Housify - Join a Game")
      pixmap = QPixmap('./src/background.png')
      palette = self.palette()
      palette.setBrush(QPalette.Background, QBrush(pixmap))
      self.setPalette(palette)
      self.MainUI()

   def MainUI(self):
      # HOUSIFY
      self.mainTitle=QLabel("HOUSIFY",self)
      self.mainTitle.setFixedSize(1120,52)
      self.mainTitle.move(0,210)
      self.mainTitle.setAlignment(QtCore.Qt.AlignCenter)
      self.mainTitle.setStyleSheet("font-family: Paytone One; background: transparent; font-size:60px; color: black;")

      # Game Code
      self.enterGameCode=QLineEdit(self)
      self.enterGameCode.setStyleSheet("color: black; font-family: Poppins; font-size: 21px; background: #D7D7D7; border: 2px solid black;")
      self.enterGameCode.setFixedSize(200,55)
      self.enterGameCode.move(340,310)
      self.enterGameCode.setAlignment(QtCore.Qt.AlignCenter)
      self.enterGameCode.setPlaceholderText('Game Code')
      self.enterGameCode.setFocusPolicy(0x2)

      # Submit Button
      self.submitGameCode=QPushButton('Submit',self)
      self.submitGameCode.setStyleSheet('''QPushButton{
                                 font-family: Poppins; 
                                 font-size: 21px; 
                                 background: #69B1F4; 
                                 border: 2px solid black;
                                 color: black;
                                 }
                                 QPushButton::hover{
                                 background: #63a9eb;
                                 }''')
      self.submitGameCode.setFixedSize(200,55)
      self.submitGameCode.move(580,310)
      self.submitGameCode.clicked.connect(lambda: logic.joinGame(self.enterGameCode.text(),name))

# host a game window
class hostGameWindow(QWidget):
   def __init__(self):
      super().__init__()
      self.setFixedSize(1120,560)
      self.setWindowTitle('Housify - Host a Game')
      pixmap = QPixmap('./src/background_host.png')
      palette = self.palette()
      palette.setBrush(QPalette.Background, QBrush(pixmap))
      self.setPalette(palette)
      self.MainUI()
   
   def MainUI(self):
      # HOUSIFY
      self.mainTitle=QLabel("HOUSIFY",self)
      self.mainTitle.setFixedSize(1120,47)
      self.mainTitle.move(0,165)
      self.mainTitle.setAlignment(QtCore.Qt.AlignCenter)
      self.mainTitle.setStyleSheet("font-family: Poppins; font-weight: 900; background: transparent; font-size:35px; color: black;")

      # Game Code Label
      self.gameCodeLabelGame=QLabel('Game',self)
      self.gameCodeLabelGame.setStyleSheet("color: black; font-family: Poppins; font-weight: 700; font-size: 22px;")
      self.gameCodeLabelGame.move(393,235)
      self.gameCodeLabelCode=QLabel('Code',self)
      self.gameCodeLabelCode.setStyleSheet("color: black; font-family: Poppins; font-weight: 700; font-size: 22px;")
      self.gameCodeLabelCode.move(397,260)

      # Colon
      self.colon=QLabel(':',self)
      self.colon.setStyleSheet("color: black; font-family: Poppins; font-weight: 900; font-size: 65px;")
      self.colon.move(490,210)

      # Game Code
      self.newGameCode=logic.createGame()
      self.gameCode=QLabel(self.newGameCode,self)
      self.gameCode.setStyleSheet("color: black; font-family: Poppins; font-weight: 900; font-size: 62px;")
      self.gameCode.move(535,215)

      # Start Game Button
      self.startGame=QPushButton('Start Game',self)
      self.startGame.setStyleSheet('''QPushButton{
                                 font-family: Poppins; 
                                 font-size: 18px; 
                                 background: #69B1F4; 
                                 border: 2px solid black;
                                 color: black;
                                 }
                                 QPushButton::hover{
                                 background: #63a9eb;}''')
      self.startGame.setFixedSize(200,55)
      self.startGame.move(340,325)
      #self.startGame.clicked.connect()

      # Copy to Clipboard Function
      def c2cbFunc(self):
         pyperclip.copy(self.newGameCode)
         self.copied=QLabel('Copied to Clipboard',self)
         self.copied.setStyleSheet('font-family: poppins; font-size: 12px; color: #D2626E;')
         self.copied.setFixedWidth(1120)
         self.copied.setAlignment(QtCore.Qt.AlignCenter)
         self.copied.move(0,390)
         self.copied.show()
         QtCore.QTimer.singleShot(5000,lambda: self.copied.hide())

      # Copy to Clipboard Button
      self.c2cb=QPushButton('Copy to Clipboard',self)
      self.c2cb.setStyleSheet('''QPushButton{
                                 font-family: Poppins; 
                                 font-size: 18px; 
                                 background: #69B1F4; 
                                 border: 2px solid black;
                                 color: black;
                                 }
                                 QPushButton::hover{
                                 background: #63a9eb;}''')
      self.c2cb.setFixedSize(200,55)
      self.c2cb.move(580,325)
      self.c2cb.clicked.connect(lambda: c2cbFunc(self))

def main():
   global name
   logic.connectMe()
   app = QApplication(sys.argv)
   try:
      name = logic.getName()
      ex = mainWindow()
      ex.show()
   except:
      ex = usernameWindow()
      ex.show()
   QFontDatabase.addApplicationFont('./src/fonts/Paytone_One/PaytoneOne-Regular.ttf')
   QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-Regular.ttf')
   QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-ExtraBold.ttf')
   QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-SemiBold.ttf')
   sys.exit(app.exec_())
   
if __name__ == '__main__':
   main()
