import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontDatabase , QPixmap , QPalette , QBrush
import random
import pyperclip
from connection import Client
import logic
import ticket
from player_list import PlayerList
import GRID

# TODO: create a parent window object
# TODO: use QMessageBox.information for all occurrences

# enter username
class usernameWindow(QWidget):
   def __init__(self):
      super().__init__()
      self.setFixedSize(500,200)
      self.setWindowTitle("Housify")
      self.setStyleSheet('background-color: rgb(50,50,50)')
      self.mainUI()
   
   def openCloseWindow(self,username):
      global name, client
      with open('username.txt','w') as file:
         file.write(username)
      name=username
      # Connect the client to server
      client.connect(name)
      client.run()
      self.hide()
      self.close()
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
      self.hide()
      self.close()
   
   # function to show hostGameWindow
   def hostGameButton(self):
      game_code = str(random.randint(10000,99999))
      obj = {"username": name, "role" : "HOST", "event" : "CREATE GAME", "code" : game_code}
      client.send(obj)
      self.newWin = hostGameWindow(game_code)
      self.newWin.show()
      self.hide()
      self.close()

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
      client.msgSignal.connect(self.onJoin)
      self.setPalette(palette)
      self.MainUI()

   def joinGameButton(self):
      self.game_code = self.enterGameCode.text()
      obj = {"username": name, "role" : "PLAYER", "event" : "JOIN GAME", "code" : self.game_code}
      client.send(obj)

   @QtCore.pyqtSlot(dict)
   def onJoin(self, msg) :
      msg =  msg["event"] 
      if msg and msg == "SUCCESS" : 
         self.newWin = waitingLobbyWindow(self.game_code)
         self.newWin.show()
         self.close_win()
      elif msg == "FAILED":
         self.dialog = QMessageBox.critical(self,'Error',"There was an error in joining the game. Please make sure that you've entered a correct code")

   def goBack(self):
      self.oldWin = mainWindow()
      self.close()
      self.oldWin.show()

   def MainUI(self):
      # HOUSIFY
      self.mainTitle=QLabel("HOUSIFY",self)
      self.mainTitle.setFixedSize(1120,52)
      self.mainTitle.move(0,210)
      self.mainTitle.setAlignment(QtCore.Qt.AlignCenter)
      self.mainTitle.setStyleSheet("font-family: Paytone One; background: transparent; font-size:60px; color: black;")

      self.backButton = QPushButton('<  Back',self)
      self.backButton.setStyleSheet('''QPushButton{
                                 font-family: Poppins; 
                                 font-size: 16px; 
                                 background: #F0E4CD; 
                                 border: 2px solid black;
                                 color: black;
                                 }
                                 QPushButton::hover{
                                 background: #FFF3DC;}''')
      self.backButton.setFixedSize(90,30)
      self.backButton.move(310,175)
      self.backButton.clicked.connect(self.goBack)

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
      self.submitGameCode.clicked.connect(self.joinGameButton)

   def close_win(self) :
      client.msgSignal.disconnect(self.onJoin) 
      self.hide()
      self.close()

# host a game window
class hostGameWindow(QWidget):

   def __init__(self, newGameCode):
      super().__init__()
      self.newGameCode= newGameCode
      self.setFixedSize(1120,560)
      self.setWindowTitle('Housify - Host a Game')
      pixmap = QPixmap('./src/background_host.png')
      palette = self.palette()
      palette.setBrush(QPalette.Background, QBrush(pixmap))
      self.setPalette(palette)
      self.MainUI()
      client.msgSignal.connect(self.updatePlayers)

   # function start game button
   def startingGame(self):
      msg = {"event" : "START GAME", "code" : self.newGameCode, "username" : name}
      client.send(msg)
      self.hostwindow=hostingGame(self.newGameCode)
      self.hostwindow.show()
      self.close_win()

   # function go back button
   def goBack(self):
      self.oldWin = mainWindow()
      self.close()
      self.oldWin.show()

   # what happens when new player joins
   @QtCore.pyqtSlot(dict)
   def updatePlayers(self, msg): 
      if msg["event"] == "PLAYER JOIN" :
         self.p.add_player(msg["player_name"])
      elif msg["event"] == "PLAYER LEAVE"  : 
         self.p.remove_player(msg["player"])

   def MainUI(self):
      # HOUSIFY
      self.mainTitle=QLabel("HOUSIFY",self)
      self.mainTitle.setFixedSize(1120,47)
      self.mainTitle.move(0,165)
      self.mainTitle.setAlignment(QtCore.Qt.AlignCenter)
      self.mainTitle.setStyleSheet("font-family: Paytone One; background: transparent; font-size:35px; color: black;")

      # back button
      self.backButton = QPushButton('<  Back',self)
      self.backButton.setStyleSheet('''QPushButton{
                                 font-family: Poppins; 
                                 font-size: 16px; 
                                 background: #F0E4CD; 
                                 border: 2px solid black;
                                 color: black;
                                 }
                                 QPushButton::hover{
                                 background: #FFF3DC;}''')
      self.backButton.setFixedSize(90,30)
      self.backButton.move(310,175)
      self.backButton.clicked.connect(self.goBack)

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
      self.gameCode=QLabel(self.newGameCode,self)
      self.gameCode.setStyleSheet("color: black; font-family: Poppins; font-weight: 900; font-size: 62px;")
      self.gameCode.move(535,215)

      # Player list
      self.p = PlayerList("PLAYERS", self)
      self.p.move(870, 140)
      self.p.show()

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

   # what happens when window closes
   def close_win(self) : 
      client.msgSignal.disconnect(self.updatePlayers)
      self.hide()
      self.close() 

# waiting lobby window
class waitingLobbyWindow(QWidget):
   def __init__(self, code):
      super().__init__()
      self.setFixedSize(1120,560)
      self.setWindowTitle('Housify - Waiting Lobby')
      pixmap = QPixmap('./src/background_gameplay.png')
      palette = self.palette()
      self.code = code
      palette.setBrush(QPalette.Background, QBrush(pixmap))
      self.setPalette(palette)
      self.MainUI()
      client.msgSignal.connect(self.startGame)
   
   @QtCore.pyqtSlot(dict)
   def startGame(self, msg) :
      if msg["event"] == "START GAME" : 
         self.newin = playAGameWindow(self.code)
         self.newin.show()
         self.close_win()

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

      # display of game code
      self.gameCodeLabel=QLabel('Game code:',self)
      self.gameCodeLabel.setStyleSheet("color: black; font-family: Poppins; font-weight: 700; font-size: 22px;")
      self.gameCodeLabel.move(120,410)

      self.gameCode=QLabel(self.code,self)
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
      self.leaveButton.clicked.connect(self.onLeaveGame)

   # leave game button function
   def onLeaveGame(self) :
      client.send({"event" : "LEAVE GAME", "code" : self.code})
      self.newin = mainWindow()
      self.newin.show()
      self.close_win()

   def close_win(self) : 
      client.msgSignal.disconnect(self.startGame)
      self.hide()
      self.close()

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
      client.msgSignal.connect(self.react)
   
   # when someone appeals for something function
   def appeal(self,appealName):
      self.appealedLabel=QLabel(f'You have appealed for {appealName}, please wait while the host checks your ticket!',self)
      self.appealedLabel.setStyleSheet('font-family: poppins; font-size: 12px; color: #D2626E;')
      self.appealedLabel.move(370,340)
      self.appealedLabel.setFixedWidth(630)
      self.appealedLabel.setAlignment(QtCore.Qt.AlignCenter)
      self.appealedLabel.show()
      client.send({"event":"appeal","name":appealName,"username":name,"code":self.gamecode, "ticketId":self.ticketid})

   def MainUI(self):
      # Title PLAY
      self.playLabel=QLabel('PLAY',self)
      self.playLabel.setStyleSheet('font-family: Paytone One; font-weight: 600; background: transparent; font-size:50px; color: black;')
      self.playLabel.move(110,90)

      # Bringing Ticket to the Window
      self.ticketid='T'+str(random.randint(10000,99999))
      self.displayTicket=ticket.ticketMain(logic.generateTicket(self.ticketid), self, 'player', None)
      self.displayTicket.move(370,110)
      self.displayTicket.parent=self
      self.displayTicket.show()

      # title of 'Status'
      self.statusLabel = QLabel('Status:',self)
      self.statusLabel.setStyleSheet('font-family: Paytone One; font-weight: 600; background: transparent; font-size: 34px; color: black;')
      self.statusLabel.move(110,160)
      
      # body of status
      self.statusText = QLabel(f'''
            <div style="font-family: 'Poppins'; font-weight: 500; font-size: 20px; line-height: 0.85; color: black;">
                Numbers left: 90<br>First row<br>Second row<br>Third row<br>Full house
            </div>
        ''', self)
      self.statusText.move(110,210)

      # number called label
      self.number = QLabel('Called: ',self)
      self.number.setStyleSheet('''QLabel{
                                    font-family: Poppins;
                                    font-size: 30px;
                                    color: black;
                                    background-color: #F8EDD9;
                                    font-weight: 500;
                                    border: 2px solid black;
                                 }''')
      self.number.resize(200,76)
      self.number.setAlignment(QtCore.Qt.AlignCenter)
      self.number.move(110,380)

      # appeal button first row
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
      self.firstHouse.clicked.connect(lambda: self.appeal('First Row'))

      # appeal button second row
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
      self.secondHouse.clicked.connect(lambda: self.appeal('Second Row'))

      # appeal button third row
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
      self.thirdHouse.clicked.connect(lambda: self.appeal('Third Row'))

      # appeal button full house
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
      self.fullHouse.clicked.connect(lambda: self.appeal('Full House'))

      # leave game button
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
      self.leaveGame.clicked.connect(self.onLeaveGame)
   
   # function leave game button
   def onLeaveGame(self) :
      client.send({"event" : "LEAVE GAME", "code" : self.gamecode})
      self.newin = mainWindow()
      self.newin.show()
      self.close_win()
   
   # client - server dealing with call number and end game
   @QtCore.pyqtSlot(dict)
   def react(self, msg) : 
      if msg["event"] == "CALL NUMBER" : 
         self.number.setText(f'Called: {msg["num"]}')
         self.statusText.setText(msg["status_text"])
      if msg["event"] == "END GAME" : 
         reason = msg["reason"]
         self.dialog = QMessageBox.information(self,'GAME OVER',f"Game ended. {reason}")
         self.newin = mainWindow()
         self.newin.show()
         self.close_win()

   def close_win(self) : 
      client.msgSignal.disconnect(self.react)
      self.hide()
      self.close() 

# the window where the host is hosting game
class hostingGame(QWidget):
   def __init__(self, gamecode):
      super().__init__()
      self.setFixedSize(1120,560)
      self.setWindowTitle('Housify - Hosting a Game')
      pixmap = QPixmap('./src/gameplay-background.png')
      self.numbers = random.sample(range(1, 91), 90)
      self.called = []
      palette = self.palette()
      palette.setBrush(QPalette.Background, QBrush(pixmap))
      self.setPalette(palette)
      self.code = gamecode
      self.MainUI()
      client.msgSignal.connect(self.react)
      
   def MainUI(self):
      # Title HOST
      self.hostLabel=QLabel('HOST',self)
      self.hostLabel.setStyleSheet('font-family: Paytone One; font-weight: 600; background: transparent; font-size:50px; color: black;')
      self.hostLabel.move(110,90)

      # title status
      self.statusLabel = QLabel('Status:',self)
      self.statusLabel.setStyleSheet('font-family: "Paytone One"; font-weight: 600; background: transparent; font-size: 34px; color: black;')
      self.statusLabel.move(110,160)
      
      # status body text
      self.statusText = QLabel(f'''
            <div style="font-family: 'Poppins'; font-weight: 500; font-size: 20px; line-height: 0.85; color: black;">
                Numbers left: {len(self.numbers)}<br>First row<br>Second row<br>Third row<br>Full house
            </div>
        ''', self)
      self.statusText.move(110,210)

      # displaying numbers for the host
      self.displayNum=QLabel('''<div style="font-family: 'Poppins'; font-weight: 500; font-size: 60px; line-height: 0.85; color: #D2626E;"></div>''',self)
      self.displayNum.setFixedWidth(90)
      self.displayNum.setAlignment(QtCore.Qt.AlignCenter)
      self.displayNum.move(530,375)

      # button to call out number
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
      self.callOutNumber.clicked.connect(self.call_out)

      # button to end game
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

      # THE 9X10 GRID
      self.grid=GRID.theGrid(self)
      self.grid.move(620,100)
      self.endGame.clicked.connect(self.endgame)

   # ending game button function
   def endgame(self) : 
      client.send({"code" : self.code, "event" : "END GAME"})
      self.newin = mainWindow()
      self.newin.show()
      self.close_win()

   # call out button function
   def call_out(self) :
      if len(self.numbers):
         num = self.numbers.pop()
         self.called.append(num)

         # Updating the status text and display text
         self.statusText.setText(f'''
               <div style="font-family: 'Poppins'; font-weight: 500; font-size: 20px; line-height: 0.85; color: black;">
                  Numbers left: {len(self.numbers)}<br>First row<br>Second row<br>Third row<br>Full house
               </div>
         ''')
         self.displayNum.setText(f'''<div style="font-family: 'Poppins'; font-weight: 500; font-size: 60px; line-height: 0.85; color: #D2626E;">{num}</div>''')
         self.grid.updateStyle(num)

         # Sending it to the server  
         obj = {"event" : "CALL NUMBER", "num" : num, "code" : self.code, "status_text" : self.statusText.text()}
         client.send(obj)

   # what happens when an appeal gets approved
   def approveAppeal(self,Result):
      if Result:
         if self.appealReason=='First Row':
            replaceText=f'''<div style="font-family: 'Poppins'; font-weight: 500; font-size: 20px; line-height: 0.85; color: black;">
                Numbers left: {len(self.numbers)}<br> First row: {self.appealPerson} <br>Second row<br>Third row<br>Full house
            </div>'''
         elif self.appealReason=='Second Row':
            replaceText=f'''<div style="font-family: 'Poppins'; font-weight: 500; font-size: 20px; line-height: 0.85; color: black;">
                Numbers left: {len(self.numbers)}<br>First row<br> Second row: {self.appealPerson} <br>Third row<br>Full house
            </div>'''
         elif self.appealReason=='Third Row':
            replaceText=f'''<div style="font-family: 'Poppins'; font-weight: 500; font-size: 20px; line-height: 0.85; color: black;">
                Numbers left: {len(self.numbers)}<br>First row<br>Second row<br> Third row: {self.appealPerson} <br>Full house
            </div>'''
         elif self.appealReason=='Full House':
            replaceText=f'''<div style="font-family: 'Poppins'; font-weight: 500; font-size: 20px; line-height: 0.85; color: black;">
                Numbers left: {len(self.numbers)}<br>First row<br>Second row<br>Third row<br> Full house: {self.appealPerson}
            </div>'''
         self.statusText.hide()
         self.statusText.setText(replaceText)
         self.statusText.show()

   # client - server connection for leave player and appeal
   @QtCore.pyqtSlot(dict) 
   def react(self, msg)  :
      if msg["event"] == "PLAYER LEAVE" : 
         name = msg["player"]
         self.dialog = QMessageBox.information(self,"INFO",f"{name} left the game.")
      if msg["event"] == "appeal" :
         # self.dialog = QMessageBox.information(self,'INFO',f"{msg['username']} has appealed for {msg['name']}.")
         self.appealReason=msg['name']
         self.appealPerson=msg['username']
         self.appealWindow = appealWindow(self.appealReason,self.appealPerson,msg['ticketId'],self.called)
         self.appealWindow.show()
         self.appealWindow.signalObj.connect(self.approveAppeal)

   def close_win(self) : 
      client.msgSignal.disconnect(self.react)
      self.hide()
      self.close()     

# the appeal window
class appealWindow(QWidget):
    signalObj=QtCore.pyqtSignal(bool)

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
        self.approveButton.clicked.connect(lambda: self.appealResult(True))

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
        self.declineButton.clicked.connect(lambda: self.appealResult(False))

    def appealResult(self, result):
        self.signalObj.emit(result) 
        self.hide()
# ---- END OF ALL MODULES ----
      
def main():
   global name, client
   app = QApplication(sys.argv)
   app.setWindowIcon(QtGui.QIcon('./src/app.ico'))
   QFontDatabase.addApplicationFont('./src/fonts/Paytone_One/PaytoneOne-Regular.ttf')
   QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-Regular.ttf')
   QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-ExtraBold.ttf')
   QFontDatabase.addApplicationFont('./src/fonts/Poppins/Poppins-SemiBold.ttf')

   client = Client()
#    try:
#       name = logic.getName()
#       ex = mainWindow()
#       ex.show()
#    except Exception as error:
#       print(error)
   ex = usernameWindow()
   ex.show()
   code = app.exec_()
   sys.exit(code)
   
if __name__ == '__main__':
   main()