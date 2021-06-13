from typing import List, Callable, Generator
from package.src.task import Task
from package.src.file_processor import FileProcessor
from package.src.error import Error


class TaskContainer:

    def __init__(self, eh: Callable) -> None:
        self.file_name = ""
        self.tasks: List[Task] = []
        self.error_handler: Callable = eh

    def getTasks(self) -> List[Task]:
        return self.tasks

    def getLen(self) -> int:
        return len(self.tasks)

    def loadFromFile(self, fn: str) -> None:
        self.file_name = fn
        Task.reset_topic_len()
        try:
            self.tasks = FileProcessor.load_csv(self.file_name)
            for t in self.tasks:
                print(t.id)
            print()
            print(len(self.tasks))
        except Error as e:
            self.tasks = []
            self.error_handler(e)

    def refreshTasks(self) -> None:
        self.loadFromFile(self.file_name)

    def save(self) -> None:
        self.saveToFile(self.file_name)

    def saveToFile(self, fn: str) -> None:
        try:
            FileProcessor.save_csv(fn, self.mapToCsvString())
        except Error as e:
            self.error_handler(e)

    def removeTask(self, task: Task) -> None:
        self.tasks.remove(task)

    def removeId(self, id: int) -> Task:
        for i, task in enumerate(self.tasks):
            if task.getId() == id:
                return self.tasks.pop(i)
        return None

    def addTaskFromStr(self, text: str) -> (Task, int):
        try:
            task = Task.create_task(len(self.tasks), text.split(','))
            self.tasks.insert(0, task)
            self.tasks = Task.minimize_lateness(self.tasks)
            return task, self.tasks.index(task)
        except Error as e:
            self.error_handler(e)
            return None, None

    def mapToCsvString(self) -> Generator[str, None, None]:
        for task in self.tasks:
            yield task.toCsvString()
