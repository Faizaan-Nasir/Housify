from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt


class PlayerList(QWidget) : 
    
    changeSignal = pyqtSignal()

    def __init__(self, heading, parent = None) :
        super(PlayerList, self).__init__(parent)
        self.setFixedSize(244,276)
        self.players = []
        self.heading = heading
        self.initUI()
        self.changeSignal.connect(self.change)
    
    def initUI(self) :
        self.Layout=QVBoxLayout()
        self.headingLabel = QLabel(self.heading)
        self.headingLabel.setStyleSheet("color: black; font-family: Poppins; font-weight: 900; font-size: 35px;")
        self.headingLabel.setFixedSize(244,100)
        self.headingLabel.setAlignment(Qt.AlignCenter)
        self.Layout.addWidget(self.headingLabel)
        for i in range(4):
            self.label=QLabel('') 
            self.label.setStyleSheet("color: #D2626E; font-family: Poppins; font-weight: 600; font-size: 22px;")
            self.label.setFixedWidth(244)
            self.label.setAlignment(Qt.AlignCenter)
            self.Layout.addWidget(self.label)
        self.setLayout(self.Layout)    

    def add_player(self, p) :
        self.players.append(p)
        self.changeSignal.emit()

    def remove_player(self, p) : 
        self.players.remove(p)
        self.changeSignal.emit()
    
    @pyqtSlot()
    def change(self):
        if self.Layout is not None:
            for i in reversed(range(1,self.Layout.count())):
                self.Layout.itemAt(i).widget().deleteLater()
        a=1
        for i in self.players:
            if a<4:
                self.label=QLabel(i) 
                self.label.setStyleSheet("color: black; font-family: Poppins; font-weight: 600; font-size: 22px;")
                self.label.setFixedWidth(244)
                self.label.setAlignment(Qt.AlignCenter)
                self.Layout.addWidget(self.label)
            a+=1
        else:
            if a>4:
                self.label=QLabel(f'{a-4} more player(s)') 
                self.label.setStyleSheet("color: #D2626E; font-family: Poppins; font-weight: 600; font-size: 22px;")
                self.label.setFixedWidth(244)
                self.label.setAlignment(Qt.AlignCenter)
                self.Layout.addWidget(self.label)
            else:
                print(a)
                for i in range(5-a):
                    self.label=QLabel('') 
                    self.label.setStyleSheet("color: #D2626E; font-family: Poppins; font-weight: 600; font-size: 22px;")
                    self.label.setFixedWidth(244)
                    self.label.setAlignment(Qt.AlignCenter)
                    self.Layout.addWidget(self.label)