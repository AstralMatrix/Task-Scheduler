from package.src.file_processor import FileProcessor
from package.src.task import Task
from package.src.settings import Settings
from package.src.error import Error
from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QListWidget, \
    QGridLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont


class Form(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "TaskMaster"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        screen = QWidget()
        self.setCentralWidget(screen)

        layout = QGridLayout()
        screen.setLayout(layout)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')

        openButton = QAction('Open File', self)
        openButton.triggered.connect(self.openFile)
        fileMenu.addAction(openButton)
        saveButton = QAction('Save File', self)
        saveButton.triggered.connect(self.saveFile)
        fileMenu.addAction(saveButton)
        exitButton = QAction('Exit', self)
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        addButton = QAction('Add Task', self)
        editMenu.addAction(addButton)
        toggleButton = QAction('Toggle Task', self)
        editMenu.addAction(toggleButton)
        removeButton = QAction('Remove Task', self)
        editMenu.addAction(removeButton)

        self.taskList = self.createTaskList(
            Task.display_tasks(
                self.run(FileProcessor.load_csv, Settings.active_file, fb=[])))

        layout.addWidget(self.taskList)

        self.show()

    def createTaskList(self, data):
        tl = QListWidget()
        tl.setFont(QFont('noto mono', 10))
        for item in data:
            tl.insertItem(0, item)
        return tl

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open File", "Test", "CSV Files (*.csv);;All Files (*)",
            options=options)
        tasks = self.run(FileProcessor.load_csv, fileName, fb=[])
        Settings.active_file = fileName
        print(fileName)

        layout = self.taskList.parent().layout()
        newTaskList = self.createTaskList(Task.display_tasks(tasks))
        layout.replaceWidget(self.taskList, newTaskList)
        self.taskList = newTaskList

    def saveFile(self):
        pass

    def run(self, function, *args, fb):
        try:
            return function(*args)
        except Error as e:
            QMessageBox.critical(self, "ERROR", f"Error: {e}")
            return fb
