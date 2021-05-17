from package.src.file_processor import FileProcessor
from package.src.task import Task

x = FileProcessor.load_csv("data/input.csv")
for item in Task.display_tasks(x):
    print(item)
