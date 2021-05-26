from typing import List, Callable
from package.src.file_processor import FileProcessor
from package.src.task import Task
from package.src.settings import Settings
from package.src.error import Error
from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QListWidget, \
    QGridLayout, QFileDialog, QMessageBox, QDesktopWidget, QMenuBar, QMenu, \
    QListWidgetItem, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QRect, QPoint, Qt


class Form(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.title: str = "TaskMaster"
        self.setWindowIcon(QIcon("icon.png"))
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

        buttonLayout: QHBoxLayout = QHBoxLayout()

        removeBtn = QPushButton('Remove Task', self)
        removeBtn.clicked.connect(self.removeTask)
        buttonLayout.addWidget(removeBtn)
        editBtn = QPushButton('Edit Task', self)
        editBtn.clicked.connect(self.editTask)
        buttonLayout.addWidget(editBtn)
        toggleBtn = QPushButton('Toggle Task', self)
        toggleBtn.clicked.connect(self.toggleTask)
        buttonLayout.addWidget(toggleBtn)
        addBtn = QPushButton('Add Task', self)
        addBtn.clicked.connect(self.addTask)
        buttonLayout.addWidget(addBtn)

        buttonLayout.insertStretch(1, 1)

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
        editButton: QAction = QAction('Edit Task', self)
        editButton.triggered.connect(self.editTask)
        editMenu.addAction(editButton)
        removeButton: QAction = QAction('Remove Task', self)
        removeButton.triggered.connect(self.removeTask)
        editMenu.addAction(removeButton)

        self.taskList: QListWidget = self.createTaskList(
            self.run(
                FileProcessor.load_csv, Settings.active_file, fb=[]))

        layout.addWidget(self.taskList)

        layout.addLayout(buttonLayout, 1, 0)

        self.show()

    def createTaskList(self, data: List[str]) -> QListWidget:
        tl = QListWidget()
        tl.setFont(QFont('noto mono', 10))
        for task in data[::-1]:
            widget_item: QListWidgetItem = QListWidgetItem(
                task.display_str(), tl)
            widget_item.setData(Qt.UserRole, task)
        tl.itemDoubleClicked.connect(self.toggleTask)
        return tl

    def getIcon(self, task) -> QIcon:
        if task.status:
            return QIcon("icons/success.png")
        return QIcon("icons/close.png")

    def openFile(self) -> None:
        options: QFileDialog = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open File", "Test", "CSV Files (*.csv);;All Files (*)",
            options=options)
        tasks: List[Task] = self.run(FileProcessor.load_csv, fileName, fb=[])
        Settings.active_file = fileName
        print(fileName)

        # Create a new QListWidget with the newly loaded tasks, and replace the
        # previouse QListWidget with the new one.
        layout: QGridLayout = self.taskList.parent().layout()
        newTaskList: QListWidget = self.createTaskList(tasks)
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

    def toggleTask(self, item=None) -> None:
        item = self.taskList.currentItem()
        task = item.data(Qt.UserRole)
        task.toggle_status()
        item.setText(task.display_str())
        # item.setIcon(self.getIcon(task))

    def editTask(self) -> None:
        QMessageBox.information(
            self, "info", f"Editing has not yet been "
            f"added\nPlease edit the csv file itself\n{Settings.active_file}")

    def removeTask(self) -> None:
        self.taskList.takeItem(self.taskList.currentRow())
        # TODO: REMOVE TASK FROM ARRAY

    def run(self, function: Callable, *args, fb: any = None) -> any:
        try:
            return function(*args)
        except Error as e:
            QMessageBox.critical(self, "ERROR", f"Error: {e}")
            return fb
