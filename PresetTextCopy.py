import sys
import clipboard
from PySide2.QtCore import QRect, QSize
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget, QSizePolicy, QPushButton, QRadioButton, QTextEdit, QHBoxLayout, QSpacerItem

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.intiUi() # UI 구성
        self.textList = [] # 텍스트 리스트
        self.radioButtons = [] # 라디오 버튼 리스트
        self.dataLoad() # 데이터 불러오기

    # UI 구성 메서드
    def intiUi(self):
        self.resize(516, 565) # 기본 창 사이즈
        self.setWindowTitle('Preset Text Copy')

        self.verticalLayout = QVBoxLayout()
        
        self.label_1 = QLabel("복사할 텍스트를 선택하세요.")
        
        self.verticalLayout.addWidget(self.label_1)

        # 스크롤 영역 설정
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 496, 332))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        # 라벨 추가
        self.label_2 = QLabel("복사된 텍스트")
        self.verticalLayout.addWidget(self.label_2)

        # 복사된 텍스트 보여주는 영역
        self.textEdit = QTextEdit()
        self.textEdit.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMinimumSize(QSize(0, 140))
        self.textEdit.setMaximumSize(QSize(16777215, 140))
        self.textEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.textEdit)

        # 텍스트 추가 버튼, 텍스트 삭제 버튼 설정
        self.horizontalLayout = QHBoxLayout()
        self.textAddButton = QPushButton("텍스트 추가")
        self.textAddButton.clicked.connect(self.textAdd)
        self.horizontalLayout.addWidget(self.textAddButton)
        self.textRemoveButton = QPushButton("텍스트 삭제")
        self.textRemoveButton.clicked.connect(self.textRemove)
        self.horizontalLayout.addWidget(self.textRemoveButton)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.verticalLayout.addLayout(self.horizontalLayout)

        # 메인 위젯 설정
        MainWidget = QWidget()
        MainWidget.setLayout(self.verticalLayout) # 레이아웃 설정

        self.setCentralWidget(MainWidget)

    # 데이터 불러오는 메서드
    def dataLoad(self):
        f = open("text_data.txt", 'r', encoding='utf-8')
        self.textList = f.read().split('\n\n')
        if self.textList[0] == '':
            self.textList.pop()
        
        # 라디오 버튼 생성
        for text in self.textList:
            radioBtn = QRadioButton()
            radioBtn.setText(text)
            radioBtn.clicked.connect(self.textCopy)
            self.radioButtons.append(radioBtn)
            self.verticalLayout_2.addWidget(radioBtn)
        f.close()

    # 텍스트 복사 메서드
    def textCopy(self):
        for radioBtn in self.radioButtons:
            if radioBtn.isChecked() and radioBtn.text() != "(삭제된 텍스트)":
                clipboard.copy(radioBtn.text())
                self.textEdit.setText(radioBtn.text())

    # 텍스트 추가 창 띄우는 메서드
    def textAdd(self):
        textAddWindow = TextAdd()
        textAddWindow.exec_()

    # 텍스트 삭제 창 띄우는 메서드
    def textRemove(self):
        textRemoveWindow = TextRemove()
        textRemoveWindow.exec_()

class TextAdd(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowModality(Qt.ApplicationModal)
        self.show()
        self.initUi()
        
    # UI 구성 메서드    
    def initUi(self):
        self.setFixedSize(516, 220) # 기본 창 사이즈
        self.setWindowTitle('텍스트 추가')
        
        # 레이아웃 설정
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout) 

        # 라벨 추가
        self.label_1 = QLabel("추가할 텍스트를 입력하세요.")
        self.verticalLayout.addWidget(self.label_1)

        # 텍스트 입력 영역
        self.textEdit = QTextEdit()
        self.textEdit.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMinimumSize(QSize(0, 140))
        self.textEdit.setMaximumSize(QSize(16777215, 140))
        self.verticalLayout.addWidget(self.textEdit)

        # 하단에 추가 버튼 추가
        self.horizontalLayout = QHBoxLayout()
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.textAddButton = QPushButton("추가")
        self.textAddButton.clicked.connect(self.textAdd)
        self.horizontalLayout.addWidget(self.textAddButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

    # 텍스트 추가 메서드
    def textAdd(self):
        string = self.textEdit.toPlainText() # 텍스트 영역에 입력한 텍스트 불러오기

        # text_data.txt 에 추가한 텍스트 저장
        f = open("text_data.txt", 'a', encoding='utf-8')
        if len(window.textList) == 0:
            f.write(string.strip())
        else:
            f.write("\n\n" + string.strip())
        f.close()

        # 라디오 버튼 추가
        radioBtn = QRadioButton()
        radioBtn.setText(string.strip())
        radioBtn.clicked.connect(window.textCopy)

        # 리스트에 데이터 추가
        window.textList.append(string.strip())
        window.radioButtons.append(radioBtn)

        window.verticalLayout_2.addWidget(radioBtn) # 스크롤 영역에 라디오 버튼 추가

        self.close()

class TextRemove(QDialog):    
    def __init__(self):
        super().__init__()
        self.setWindowModality(Qt.ApplicationModal)
        self.show()
        self.initUi()
        self.radioButtons = []
        self.dataLoad()
        
    # UI 구성 메서드    
    def initUi(self):
        self.resize(516, 465) # 기본 창 사이즈
        self.setWindowTitle('텍스트 삭제')
        
        # 레이아웃 설정
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout) 

        # 스크롤 영역 설정
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 496, 332))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        # 하단에 삭제 버튼 추가
        self.horizontalLayout = QHBoxLayout()
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.textRemoveButton = QPushButton("삭제")
        self.textRemoveButton.clicked.connect(self.textRemove)
        self.horizontalLayout.addWidget(self.textRemoveButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

    # 데이터 불러오는 메서드
    def dataLoad(self):
        f = open("text_data.txt", 'r', encoding='utf-8')
        textList = f.read().split('\n\n')

        # 라디오 버튼 생성
        for text in textList:
            radioBtn = QRadioButton(self.scrollAreaWidgetContents)
            radioBtn.setText(text)
            self.radioButtons.append(radioBtn)
            self.verticalLayout_2.addWidget(radioBtn)
        f.close()

    def textRemove(self):
        temp = "" # 임시 문자열 변수
        
        # 선택한 텍스트 삭제하고 text_data.txt에 저장
        for radioBtn in self.radioButtons:
            if radioBtn.isChecked():
                window.radioButtons[window.textList.index(radioBtn.text())].setText("(삭제된 텍스트)")
                window.textList[window.textList.index(radioBtn.text())] = ""
                
                for i in range(len(window.textList)):
                    if i == len(window.textList) - 1 and window.textList[i] == '':
                        temp += window.textList[i]
                    elif window.textList[i] == '':
                        continue
                    else:
                        temp += window.textList[i] + "\n\n"

                f = open("text_data.txt", 'w', encoding='utf-8')
                f.write(temp.rstrip())
                print(window.textList)
                print(temp)
                f.close()
        self.close()
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()