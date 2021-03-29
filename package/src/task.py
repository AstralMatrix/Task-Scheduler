from enum import Enum
from typing import List
from datetime import datetime


class Task:

    def __init__(self, i: int, dd: int, hd: int, tp: str, ta: str, st: bool):
        self.id: int = i
        self.date_due: int = dd
        self.hour_due: int = hd
        self.topic: str = tp
        self.task: str = ta
        self.status: bool = st

    def str_date(self) -> str:
        num_str: str = "{:04d}".format(self.date_due)
        return f"{num_str[0:2]}/{num_str[2:4]}"

    def str_hour(self) -> str:
        d: datetime = datetime.strptime(f"{self.hour_due:04d}", "%H%M")
        return d.strftime("%I:%M %p")

    def str_status(self) -> str:
        return "⬛" if self.status else "⬜"

    def display_str(self) -> str:
        return f"{self.str_status()}  {self.str_date()}  {self.str_hour()}  " \
               f"{self.topic:7} {self.task}"

    def __str__(self) -> str:
        return f"Task: #{self.id:2d} is due on {self.str_date()} at " \
               f"{self.str_hour()} for {self.topic} is \"{self.task}\"" \
               f" and is {self.str_status()}"

    @staticmethod
    def minimize_lateness(tasks: List['Task']) -> List['Task']:
        return sorted(tasks, key=lambda x: (x.date_due, x.hour_due, x.id))

    @staticmethod
    def create_task(id: int, csv_line: List[str]) -> 'Task':
        # Get date
        raw_date_due: str = str(
            csv_line[TaskCategories.DATE_DUE.value]
        ).replace('/', '')
        assert len(raw_date_due) == 4
        date_due: int = int(raw_date_due)

        # Get time
        raw_hour_due: str = str(
            csv_line[TaskCategories.HOUR_DUE.value]
        ).replace(':', '')
        if len(raw_hour_due) != 4:
            raw_hour_due = "2359"
        hour_due: int = int(raw_hour_due)

        # Get topic
        topic: str = csv_line[TaskCategories.TOPIC.value]

        # Get task
        task: str = csv_line[TaskCategories.TASK.value]

        # Get status
        raw_status: str = csv_line[TaskCategories.STATUS.value]
        assert raw_status == '0' or raw_status == '1'
        status: bool = bool(int(raw_status))

        # Assert types
        assert type(date_due) == int
        assert type(hour_due) == int
        assert type(topic) == str
        assert type(task) == str
        assert type(status) == bool

        return Task(id, date_due, hour_due, topic, task, status)


class TaskCategories(Enum):
    DATE_DUE = 0
    HOUR_DUE = 1
    TOPIC = 2
    TASK = 3
    STATUS = 4
