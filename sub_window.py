from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon
import pickle

class Sub_window(QDialog):
    '''Класс дополнительных всплывающих окон'''
    def __init__(self):
        super().__init__()  

    def about(self):
        '''Метод для настройки окна About'''
        about_icon = QIcon("icons/icons8-about.svg")
        self.setWindowIcon(about_icon)
        self.layout = QVBoxLayout()
        
        #Получение текста окна из файла
        with open('about.txt', 'r', encoding='utf-8') as about_file:
            message = QLabel(about_file.read())
            
        self.layout.addWidget(message)
        self.setLayout(self.layout)
        self.setWindowTitle('About')

        #Настройка стиля окна
        with open('stylesettings', 'rb') as pickle_file:
            with open(pickle.load(pickle_file), 'r', encoding='utf-8') as style_sheet_file:
                self.setStyleSheet(style_sheet_file.read())
            
        self.exec_()
        