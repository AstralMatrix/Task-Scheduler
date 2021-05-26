from typing import List
from package.src.task import Task
from package.src.file_processor import FileProcessor
from package.src.error import Error


class TaskContainer:

    def __init__(self) -> None:
        self.file_name = ""
        self.tasks: List[Task] = []

    def getTasks(self) -> List[Task]:
        return self.tasks

    def getFromFile(self, fn) -> List[Task]:
        self.file_name = fn
        try:
            self.tasks = FileProcessor.load_csv(self.file_name)
        except Error as e:
            self.tasks = []
            raise e

    def saveToFile(self) -> None:
        pass

    def removeId(self, id: int) -> Task:
        if id >= 0 and id < len(self.tasks):
            return self.tasks.pop(id)
        return None

    def addTask(self, task: Task) -> None:
        pass
