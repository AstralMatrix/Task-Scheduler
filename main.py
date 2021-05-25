#!/usr/bin/env python3
import sys
from package.src.file_processor import FileProcessor
from package.src.task import Task
from package.src.form import Form
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QIcon

'''x = FileProcessor.load_csv("data/input.csv")
for item in Task.display_tasks(x):
    print(item)
    '''

app = QApplication(sys.argv)
ex = Form()
sys.exit(app.exec_())
