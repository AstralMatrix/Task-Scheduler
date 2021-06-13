from typing import List, Callable
from package.src.file_processor import FileProcessor
from package.src.task import Task
from package.src.settings import Settings
from package.src.error import Error
from package.src.task_container import TaskContainer
from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QListWidget, \
    QGridLayout, QFileDialog, QMessageBox, QDesktopWidget, QMenuBar, QMenu, \
    QListWidgetItem, QPushButton, QHBoxLayout, QLabel, QInputDialog, QLineEdit
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
        self.taskc: TaskContainer = TaskContainer(
            self.handleTaskContainerError)
        self.taskc.loadFromFile(Settings.active_file)
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
        self.taskList: QListWidget = self.createTaskList(self.taskc.getTasks())
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
        removeButton: QPushButton = QPushButton('Remove Task', self)
        removeButton.clicked.connect(self.removeTask)
        buttonLayout.addWidget(removeButton)

        self.infoLabel: QLabel = QLabel("", self)
        self.updateInfoLabel()
        buttonLayout.addWidget(self.infoLabel)

        # Create the edit button
        editButton: QPushButton = QPushButton('Edit Task', self)
        editButton.clicked.connect(self.editTask)
        buttonLayout.addWidget(editButton)

        # Create the toggle button
        toggleButton: QPushButton = QPushButton('Toggle Task', self)
        toggleButton.clicked.connect(self.toggleTask)
        buttonLayout.addWidget(toggleButton)

        # Create the add button
        addButton: QPushButton = QPushButton('Add Task', self)
        addButton.clicked.connect(self.addTask)
        buttonLayout.addWidget(addButton)

        # Add a spacer between the remove and edit buttons, and add them
        # to the main layout
        buttonLayout.insertStretch(2, 1)
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

    def updateTaskList(self):
        # Create a new QListWidget with the currently loaded tasks, and replace
        # the previous QListWidget with the new one.
        layout: QGridLayout = self.taskList.parent().layout()
        newTaskList: QListWidget = self.createTaskList(self.taskc.getTasks())
        layout.replaceWidget(self.taskList, newTaskList)
        self.taskList = newTaskList

    def createTaskList(self, data: List[str]) -> QListWidget:
        tl = QListWidget()
        tl.setFont(QFont('noto mono', 10))
        for task in data[::-1]:
            widget_item: QListWidgetItem = QListWidgetItem(
                task.display_str(), tl)
            widget_item.setData(Qt.UserRole, task)
        tl.itemDoubleClicked.connect(self.toggleTask)
        return tl

    def getSelectedTask(self) -> Task:
        item = self.taskList.currentItem()
        if item is None:
            return None
        return item.data(Qt.UserRole)

    def updateInfoLabel(self) -> None:
        current_file: str = Settings.active_file.split('/')[-1]
        number_tasks: str = str(len(self.taskc.getTasks()))
        txt: str = f"{current_file}  ({number_tasks} tasks)"
        self.infoLabel.setText(txt)

    def getIcon(self, task) -> QIcon:
        if task.status:
            return QIcon("icons/success.png")
        return QIcon("icons/close.png")

    def openFile(self) -> None:
        self.taskc.save()
        options: QFileDialog = QFileDialog.Options()
        fileName, okPressed = QFileDialog.getOpenFileName(
            self, "Open File", "Test", "CSV Files (*.csv);;All Files (*)",
            options=options)
        if okPressed:
            Settings.active_file = fileName
            self.taskc.loadFromFile(fileName)
            self.updateTaskList()
            self.updateInfoLabel()

    def saveFile(self) -> None:
        self.taskc.save()

    def addTask(self) -> None:
        text, okPressed = QInputDialog.getText(
            self, "New Task", "Construct a New Task: ", QLineEdit.Normal,
            ",,,,0")
        if okPressed:
            task, loc = self.taskc.addTaskFromStr(text)
            # Task was unable to be created
            if task is None:
                return
            widget_item: QListWidgetItem = QListWidgetItem(task.display_str())
            widget_item.setData(Qt.UserRole, task)
            self.taskList.insertItem(self.taskc.getLen()-loc-1, widget_item)

    def toggleTask(self, item=None) -> None:
        task: Task = self.getSelectedTask()
        if task is None:
            return
        task.toggle_status()
        self.taskList.currentItem().setText(task.display_str())

    def editTask(self) -> None:
        QMessageBox.information(
            self, "info", f"Editing has not yet been "
            f"added\nPlease edit the csv file itself\n{Settings.active_file}")

    def removeTask(self) -> None:
        task: Task = self.getSelectedTask()
        if task is None:
            return
        self.taskc.removeTask(task)
        self.taskList.takeItem(self.taskList.currentRow())
        self.updateInfoLabel()

    def handleTaskContainerError(self, e):
        QMessageBox.critical(self, "ERROR", f"Error: {e}")
