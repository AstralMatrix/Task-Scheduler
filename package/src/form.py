from typing import List, Callable
from package.src.file_processor import FileProcessor
from package.src.task import Task
from package.src.settings import Settings
from package.src.error import Error
from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QListWidget, \
    QGridLayout, QFileDialog, QMessageBox, QDesktopWidget, QMenuBar, QMenu
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect, QPoint


class Form(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.title: str = "TaskMaster"
        self.left: int = 10
        self.top: int = 10
        self.width: int = 640
        self.height: int = 480
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Move window to center of the screen
        geom: QRect = self.frameGeometry()
        center: QPoint = QDesktopWidget().availableGeometry().center()
        geom.moveCenter(center)
        self.move(geom.topLeft())

        screen: QWidget = QWidget()
        self.setCentralWidget(screen)

        layout: QGridLayout = QGridLayout()
        screen.setLayout(layout)

        mainMenu: QMenuBar = self.menuBar()
        fileMenu: QMenu = mainMenu.addMenu('File')
        editMenu: QMenu = mainMenu.addMenu('Edit')

        openButton: QAction = QAction('Open File', self)
        openButton.triggered.connect(self.openFile)
        fileMenu.addAction(openButton)
        saveButton: QAction = QAction('Save File', self)
        saveButton.triggered.connect(self.saveFile)
        fileMenu.addAction(saveButton)
        exitButton: QAction = QAction('Exit', self)
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        addButton: QAction = QAction('Add Task', self)
        addButton.triggered.connect(self.addTask)
        editMenu.addAction(addButton)
        toggleButton: QAction = QAction('Toggle Task', self)
        toggleButton.triggered.connect(self.toggleTask)
        editMenu.addAction(toggleButton)
        removeButton: QAction = QAction('Remove Task', self)
        removeButton.triggered.connect(self.removeTask)
        editMenu.addAction(removeButton)

        self.taskList: QListWidget = self.createTaskList(
            Task.display_tasks(
                self.run(
                    FileProcessor.load_csv, Settings.active_file, fb=[])))

        layout.addWidget(self.taskList)

        self.show()

    def createTaskList(self, data: List[str]) -> QListWidget:
        tl = QListWidget()
        tl.setFont(QFont('noto mono', 10))
        for item in data:
            tl.insertItem(0, item)
        return tl

    def openFile(self) -> None:
        options: QFileDialog = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open File", "Test", "CSV Files (*.csv);;All Files (*)",
            options=options)
        tasks: List[Task] = self.run(FileProcessor.load_csv, fileName, fb=[])
        Settings.active_file = fileName
        print(fileName)

        layout: QGridLayout = self.taskList.parent().layout()
        newTaskList: QListWidget = self.createTaskList(
            Task.display_tasks(tasks))
        layout.replaceWidget(self.taskList, newTaskList)
        self.taskList = newTaskList

    def saveFile(self) -> None:
        QMessageBox.information(
            self, "info", f"Saving has not yet been "
            f"added\nPlease edit the csv file itself\n{Settings.active_file}")

    def addTask(self) -> None:
        QMessageBox.information(
            self, "info", f"Adding has not yet been "
            f"added\nPlease edit the csv file itself\n{Settings.active_file}")

    def toggleTask(self) -> None:
        QMessageBox.information(
            self, "info", f"Toggling has not yet been "
            f"added\nPlease edit the csv file itself\n{Settings.active_file}")

    def removeTask(self) -> None:
        QMessageBox.information(
            self, "info", f"Removing has not yet been "
            f"added\nPlease edit the csv file itself\n{Settings.active_file}")

    def run(self, function: Callable, *args, fb: any) -> any:
        try:
            return function(*args)
        except Error as e:
            QMessageBox.critical(self, "ERROR", f"Error: {e}")
            return fb
