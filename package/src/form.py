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
        # Set the title and size of the window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Move window to center of the screen
        geom: QRect = self.frameGeometry()
        center: QPoint = QDesktopWidget().availableGeometry().center()
        geom.moveCenter(center)
        self.move(geom.topLeft())

        # Create the main panel
        screen: QWidget = QWidget()
        self.setCentralWidget(screen)

        # Create a grid layout and add it to the main panel
        layout: QGridLayout = QGridLayout()
        screen.setLayout(layout)

        # Create the task list widget and add it to the main panel
        self.taskList: QListWidget = self.createTaskList(
            self.run(
                FileProcessor.load_csv, Settings.active_file, fb=[]))
        layout.addWidget(self.taskList)

        # Create the buttons, adding them to the main panel
        self.initButtons(layout)

        # Create the context menu
        self.initMenu()

        self.show()

    def initButtons(self, layout):
        # Create a horizontal layout to format the buttons
        buttonLayout: QHBoxLayout = QHBoxLayout()

        # Create the remove button
        removeButton = QPushButton('Remove Task', self)
        removeButton.clicked.connect(self.removeTask)
        buttonLayout.addWidget(removeButton)

        # Create the edit button
        editButton = QPushButton('Edit Task', self)
        editButton.clicked.connect(self.editTask)
        buttonLayout.addWidget(editButton)

        # Create the toggle button
        toggleButton = QPushButton('Toggle Task', self)
        toggleButton.clicked.connect(self.toggleTask)
        buttonLayout.addWidget(toggleButton)

        # Create the add button
        addButton = QPushButton('Add Task', self)
        addButton.clicked.connect(self.addTask)
        buttonLayout.addWidget(addButton)

        # Add a spacer between the remove and edit buttons, and add them
        # to the main layout
        buttonLayout.insertStretch(1, 1)
        layout.addLayout(buttonLayout, 1, 0)

    def initMenu(self):
        # Create a new menu bar, with its respective fields
        mainMenu: QMenuBar = self.menuBar()
        fileMenu: QMenu = mainMenu.addMenu('File')
        editMenu: QMenu = mainMenu.addMenu('Edit')

        # Create buttons for the FILE MENU
        # Create the open action
        openButton: QAction = QAction('Open File', self)
        openButton.triggered.connect(self.openFile)
        fileMenu.addAction(openButton)

        # Create the save action
        saveButton: QAction = QAction('Save File', self)
        saveButton.triggered.connect(self.saveFile)
        fileMenu.addAction(saveButton)

        # Create the exit action
        exitButton: QAction = QAction('Exit', self)
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # Create buttons for the EDIT MENU
        # Create the add action
        addButton: QAction = QAction('Add Task', self)
        addButton.triggered.connect(self.addTask)
        editMenu.addAction(addButton)

        # Create the toggle action
        toggleButton: QAction = QAction('Toggle Task', self)
        toggleButton.triggered.connect(self.toggleTask)
        editMenu.addAction(toggleButton)

        # Create the edit action
        editButton: QAction = QAction('Edit Task', self)
        editButton.triggered.connect(self.editTask)
        editMenu.addAction(editButton)

        # Create the remove action
        removeButton: QAction = QAction('Remove Task', self)
        removeButton.triggered.connect(self.removeTask)
        editMenu.addAction(removeButton)

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
