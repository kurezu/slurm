from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout


class Sub_window(QDialog):
    def __init__(self):
        super().__init__()  

    def about(self):
        self = Sub_window()
        self.layout = QVBoxLayout()
        with open('about.txt', 'r', encoding='utf-8') as about_file:
            message = QLabel(about_file.read())
        self.layout.addWidget(message)
        self.setLayout(self.layout)
        
        self.setWindowTitle('About')

        with open('dark.qss', 'r', encoding='utf-8') as style_sheet_file:
            self.setStyleSheet(style_sheet_file.read())
            
        self.exec_()
        