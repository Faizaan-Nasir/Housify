import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontDatabase , QPixmap , QPalette , QBrush
import pyperclip # for copy to clipboard
import logic # local file
import ticket # local file
import GRID
import random

# create username window
class usernameWindow(QWidget):
   def __init__(self):
      super().__init__()
      self.setFixedSize(500,200)
      self.setWindowTitle("Housify")
      self.mainUI()
   
   # sets a permanent username
   def openCloseWindow(self,username):
      global name
      with open('username.txt','w') as file:
         file.write(username)
      name=username
      self.hide()
      self.newin=mainWindow()
      self.newin.show()

   def mainUI(self):
      # enter username text box
      self.usernameText=QLineEdit(self)
      self.usernameText.setStyleSheet("color: black; font-family: Poppins; font-size: 21px; background: #D7D7D7; border: 2px solid black;")
      self.usernameText.setFixedSize(250,55)
      self.usernameText.move(125,35)
      self.usernameText.setAlignment(QtCore.Qt.AlignCenter)
      self.usernameText.setPlaceholderText('Username')
      self.usernameText.setFocusPolicy(0x2)
      
      # submit button
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

   # Shows the "Playing a Game" Window
   def showGameWindow(self,gameid):
      try:
         playAGameWindow(gameid).show()
      except Exception as error:
         if str(error)=='GameNotFound':
            self.errorMessage=QLabel('<p>Game does not exist.',self)
            self.errorMessage.setStyleSheet('font-family: poppins; font-size: 12px; color: #D2626E;')
            self.errorMessage.setFixedWidth(1120)
            self.errorMessage.setAlignment(QtCore.Qt.AlignCenter)
            self.errorMessage.move(0,375)
            self.errorMessage.show()
            QtCore.QTimer.singleShot(3000, lambda: self.errorMessage.hide())
         elif str(error)=='AlreadyInGame':
            self.errorMessage=QLabel('<p>You have already joined this game.',self)
            self.errorMessage.setStyleSheet('font-family: poppins; font-size: 12px; color: #D2626E;')
            self.errorMessage.setFixedWidth(1120)
            self.errorMessage.setAlignment(QtCore.Qt.AlignCenter)
            self.errorMessage.move(0,375)
            self.errorMessage.show()
            QtCore.QTimer.singleShot(3000, lambda: self.errorMessage.hide())

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
      self.submitGameCode.clicked.connect(lambda: self.showGameWindow(self.enterGameCode.text()))

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

   def startingGame(self):
      self.hostwindow=hostingGame()
      self.hostwindow.show()

   def MainUI(self):
      # HOUSIFY
      self.mainTitle=QLabel("HOUSIFY",self)
      self.mainTitle.setFixedSize(1120,47)
      self.mainTitle.move(0,165)
      self.mainTitle.setAlignment(QtCore.Qt.AlignCenter)
      self.mainTitle.setStyleSheet("font-family: Paytone One; background: transparent; font-size:35px; color: black;")

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
      self.startGame.clicked.connect(self.startingGame)

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

# waiting lobby window
class waitingLobbyWindow(QWidget):
   def __init__(self):
      super().__init__()
      self.setFixedSize(1120,560)
      self.setWindowTitle('Housify - Waiting Lobby')
      pixmap = QPixmap('./src/background_gameplay.png')
      palette = self.palette()
      palette.setBrush(QPalette.Background, QBrush(pixmap))
      self.setPalette(palette)
      self.MainUI()

   # function to leave the game
   def leaveGame(self):
      self.close()

   def MainUI(self):
      # HOUSIFY
      self.mainTitle=QLabel("HOUSIFY",self)
      self.mainTitle.setFixedSize(1120,47)
      self.mainTitle.move(0,120)
      self.mainTitle.setAlignment(QtCore.Qt.AlignCenter)
      self.mainTitle.setStyleSheet("font-family: Paytone One; background: transparent; font-size:35px; color: black;")

      # BODY TEXT
      self.bodyText = QLabel('You have joined the game.',self)
      self.bodyText.setStyleSheet("color: black; font-family: Poppins; font-weight: 400; font-size: 40px;")
      self.bodyText.setFixedSize(1120,50)
      self.bodyText.move(0,220)
      self.bodyText.setAlignment(QtCore.Qt.AlignCenter)

      self.bodyText2 = QLabel('Please wait for the host to start the game.😘',self)
      self.bodyText2.setStyleSheet("color: black; font-family: Poppins; font-weight: 400; font-size: 40px;")
      self.bodyText2.setFixedSize(1120,50)
      self.bodyText2.move(0,280)
      self.bodyText2.setAlignment(QtCore.Qt.AlignCenter)

      self.gameCodeLabel=QLabel('Game code:',self)
      self.gameCodeLabel.setStyleSheet("color: black; font-family: Poppins; font-weight: 700; font-size: 22px;")
      self.gameCodeLabel.move(120,410)

      #TODO: NEED TO FIGURE OUT CODE FOR BRINGING GAME CODE (SAVE INTO A LOCAL FILE/RETRIEVE FROM DB)
      self.gameCode=QLabel('61123',self)
      self.gameCode.setStyleSheet("color: black; font-family: Paytone One; font-size: 62px;")
      self.gameCode.move(270,375)

      # LEAVE BUTTON
      self.leaveButton = QPushButton('Leave Game',self)
      self.leaveButton.setStyleSheet('''QPushButton{
                                 font-family: Poppins; 
                                 font-size: 18px; 
                                 background: #F46363; 
                                 border: 2px solid black;
                                 color: black;
                                 }
                                 QPushButton::hover{
                                 background: #F27D7D;}''')
      self.leaveButton.setFixedSize(150,55)
      self.leaveButton.move(860,400)
      self.leaveButton.clicked.connect(self.leaveGame)

# playing a game window
class playAGameWindow(QWidget):
   def __init__(self,gamecode):
      self.gamecode=gamecode
      super().__init__()
      self.setFixedSize(1120,560)
      self.setWindowTitle('Housify - Playing a Game')
      pixmap = QPixmap('./src/gameplay-background.png')
      palette = self.palette()
      palette.setBrush(QPalette.Background, QBrush(pixmap))
      self.setPalette(palette)
      self.MainUI()
      
   def MainUI(self):
      # Title PLAY
      self.playLabel=QLabel('PLAY',self)
      self.playLabel.setStyleSheet('font-family: Paytone One; font-weight: 600; background: transparent; font-size:50px; color: black;')
      self.playLabel.move(110,90)

      # Bringing Ticket to the Window
      self.code=logic.joinGame(self.gamecode,name)
      self.displayTicket=ticket.ticketMain(logic.generateTicket(self.code),self)
      self.displayTicket.move(370,110)
      self.displayTicket.parent=self
      self.displayTicket.show()

      self.statusLabel = QLabel('Status:',self)
      self.statusLabel.setStyleSheet('font-family: Paytone One; font-weight: 600; background: transparent; font-size: 34px; color: black;')
      self.statusLabel.move(110,160)
      
      self.statusText = QLabel('''
            <div style="font-family: 'Poppins'; font-weight: 500; font-size: 20px; line-height: 0.85; color: black;">
                Numbers left: 48<br>First row<br>Second row<br>Third row<br>Full house
            </div>
        ''', self)
      self.statusText.move(110,210)

      self.number = QPushButton('Called: 16',self)
      self.number.setStyleSheet('''QPushButton{
                                    font-family: Poppins;
                                    font-size: 30px;
                                    color: black;
                                    background-color: #F8EDD9;
                                    font-weight: 500;
                                    border: 2px solid black;
                                 }''')
      self.number.resize(200,76)
      self.number.move(110,380)

      self.firstHouse = QPushButton('1st\nRow',self)
      self.firstHouse.resize(100,76)
      self.firstHouse.setStyleSheet('''QPushButton{
                                    font-family: Poppins;
                                    font-size: 18px;
                                    color: black;
                                    font-weight: 500;
                                    background-color: #F8EDD9;
                                    border: 2px solid black;
                                 }''')
      self.firstHouse.move(370,380)

      self.secondHouse = QPushButton('2nd\nRow',self)
      self.secondHouse.resize(100,76)
      self.secondHouse.setStyleSheet('''QPushButton{
                                    font-family: Poppins;
                                    font-size: 18px;
                                    color: black;
                                    font-weight: 500;
                                    background-color: #F8EDD9;
                                    border: 2px solid black;
                                 }''')
      self.secondHouse.move(480,380)

      self.thirdHouse = QPushButton('3rd\nrow',self)
      self.thirdHouse.resize(100,76)
      self.thirdHouse.setStyleSheet('''QPushButton{
                                    font-family: Poppins;
                                    font-size: 18px;
                                    color: black;
                                    font-weight: 500;
                                    background-color: #F8EDD9;
                                    border: 2px solid black;
                                 }''')
      self.thirdHouse.move(590,380)

      self.fullHouse = QPushButton('Full\nHouse',self)
      self.fullHouse.resize(100,76)
      self.fullHouse.setStyleSheet('''QPushButton{
                                    font-family: Poppins;
                                    font-size: 18px;
                                    color: black;
                                    font-weight: 500;
                                    background-color: #F8EDD9;
                                    border: 2px solid black;
                                 }''')
      self.fullHouse.move(700,380)

      self.leaveGame = QPushButton('Leave Game',self)
      self.leaveGame.resize(150,76)
      self.leaveGame.setStyleSheet('''QPushButton{
                                    font-family: Poppins;
                                    font-size: 18px;
                                    color: black;
                                    font-weight: 500;
                                    background-color: #F46363;
                                    border: 2px solid black;
                                 }''')
      self.leaveGame.move(855,380)

class hostingGame(QWidget):
   def __init__(self):
      super().__init__()
      self.setFixedSize(1120,560)
      self.setWindowTitle('Housify - Hosting a Game')
      pixmap = QPixmap('./src/gameplay-background.png')
      palette = self.palette()
      palette.setBrush(QPalette.Background, QBrush(pixmap))
      self.setPalette(palette)
      self.MainUI()
   
   def MainUI(self):
      listONumber=list(range(1,91))
      # Title HOST
      self.hostLabel=QLabel('HOST',self)
      self.hostLabel.setStyleSheet('font-family: Paytone One; font-weight: 600; background: transparent; font-size:50px; color: black;')
      self.hostLabel.move(110,90)

      self.statusLabel = QLabel('Status:',self)
      self.statusLabel.setStyleSheet('font-family: "Paytone One"; font-weight: 600; background: transparent; font-size: 34px; color: black;')
      self.statusLabel.move(110,160)
      
      self.statusText = QLabel(f'''
            <div style="font-family: 'Poppins'; font-weight: 500; font-size: 20px; line-height: 0.85; color: black;">
                Numbers left: {len(listONumber)}<br>First row<br>Second row<br>Third row<br>Full house
            </div>
        ''', self)
      self.statusText.move(110,210)

      self.displayNum=QLabel('',self)
      self.displayNum.move(420,210)

      def callingNumber():
         if len(listONumber):
            index=random.randint(0,len(listONumber)-1)
            num=listONumber.pop(index)
            self.statusText.hide()
            self.statusText = QLabel(f'''
               <div style="font-family: 'Poppins'; font-weight: 500; font-size: 20px; line-height: 0.85; color: black;">
                  Numbers left: {len(listONumber)}<br>First row<br>Second row<br>Third row<br>Full house
               </div>
         ''', self)
            self.statusText.move(110,210)
            self.statusText.show()
            self.displayNum.hide()
            self.displayNum=QLabel(f'''<div style="font-family: 'Poppins'; font-weight: 500; font-size: 60px; line-height: 0.85; color: #D2626E;">{num}</div>''',self)
            self.displayNum.setFixedWidth(90)
            self.displayNum.setAlignment(QtCore.Qt.AlignCenter)
            self.displayNum.move(530,375)
            self.displayNum.show()
            GRID.updateStyle(num)

      self.statusText.move(110,210)

      self.callOutNumber = QPushButton('Call Out Number',self)
      self.callOutNumber.setStyleSheet('''QPushButton{
                                    font-family: Poppins;
                                    font-size: 20px;
                                    color: black;
                                    background-color: #69B1F4;
                                    font-weight: 500;
                                    border: 2px solid black;
                                    }
                                    QPushButton::hover{
                                    background: #63a9eb;}
                                 }''')
      self.callOutNumber.resize(200,76)
      self.callOutNumber.move(110,384)
      self.callOutNumber.clicked.connect(callingNumber)

      self.endGame = QPushButton('End Game',self)
      self.endGame.setStyleSheet('''QPushButton{
                                    font-family: Poppins;
                                    font-size: 20px;
                                    color: black;
                                    background-color: #F46363;
                                    font-weight: 500;
                                    border: 2px solid black;
                                 }''')
      self.endGame.resize(200,76)
      self.endGame.move(330,384)

      self.grid=GRID.theGrid(self)
      self.grid.move(620,100)
# ---- END OF ALL MODULES ----
      
def main():
   global name
   logic.connectMe()
   app = QApplication(sys.argv)
   QFontDatabase.addApplicationFont('./src/fonts/Paytone_One/PaytoneOne-Regular.ttf')
   QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-Regular.ttf')
   QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-ExtraBold.ttf')
   QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-SemiBold.ttf')
   try:
      name = logic.getName()
      # ex = playAGameWindow()
      ex = mainWindow()
      ex.show()
   except Exception as error:
      print(error)
      ex = playAGameWindow()
      ex.show()
   sys.exit(app.exec_())
   
if __name__ == '__main__':
   main()