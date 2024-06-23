from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt


class PlayerList(QWidget) : 
    
    changeSignal = pyqtSignal()

    def __init__(self, heading, parent = None) :
        super(PlayerList, self).__init__(parent)
        self.players = []
        self.heading = heading
        self.initUI()
        self.changeSignal.connect(self.change)
    
    def initUI(self) :
        self.heading = QLabel(self.heading, self)
        self.heading.setStyleSheet("color: black; font-family: Poppins; font-weight: 900; font-size: 35px;")
        self.heading.setFixedSize(160,100)
        self.heading.setAlignment(Qt.AlignCenter)
        self.heading.move(0, 0)
        # self.heading.show()
        self.label = QLabel("", self)
        self.label.setStyleSheet("color: black; font-family: Poppins; font-weight: 900; font-size: 22px;")
        self.label.setFixedSize(160, 80)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.set
        self.label.move(0, 40)

    def add_player(self, p) :
        print("Added")
        self.players.append(p)
        self.changeSignal.emit()

    def remove_player(self, p) : 
        self.players.remove(p)
        self.changeSignal.emit()
    
    @pyqtSlot()
    def change(self) : 
        self.label.setText("\n".join(self.players))