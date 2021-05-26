from enum import Enum
from typing import List, Generator
from datetime import datetime
from package.src.error import Error, ensure


class Task:

    topic_len: int = 0
    display_spaces: int = 2

    def __init__(self, i: int, dd: int, hd: int, tp: str, ta: str, st: bool):
        self.id: int = i
        self.date_due: int = dd
        self.hour_due: int = hd
        self.topic: str = tp
        self.task: str = ta
        self.status: bool = st

    def toggle_status(self) -> None:
        self.status = not self.status

    def str_date(self) -> str:
        num_str: str = "{:04d}".format(self.date_due)
        return f"{num_str[0:2]}/{num_str[2:4]}"

    def str_hour(self) -> str:
        d: datetime = datetime.strptime(f"{self.hour_due:04d}", "%H%M")
        return d.strftime("%I:%M %p")

    def str_status(self) -> str:
        return "⬛" if self.status else "⬜"

    def display_str(self) -> str:
        string: str = ''
        # Extend (or truncate) the topic to the topic length
        topic: str = self.topic.ljust(Task.topic_len)[:Task.topic_len]

        for item in [self.str_status(), self.str_date(), self.str_hour(),
                     topic, self.task]:
            # Pad each item with 'display_spaces' number of spaces
            string += f"{item}" + ' ' * Task.display_spaces
        return string.strip()

    def __str__(self) -> str:
        return f"Task: #{self.id:2d} is due on {self.str_date()} at " \
               f"{self.str_hour()} for {self.topic} is \"{self.task}\"" \
               f" and is {self.str_status()}"

    @staticmethod
    def comp_task(t: 'Task') -> tuple:
        return (t.date_due, t.hour_due, t.id)

    @staticmethod
    def minimize_lateness(tasks: List['Task']) -> List['Task']:
        return sorted(tasks, key=Task.comp_task)

    @staticmethod
    def display_tasks(tasks: List['Task']) -> Generator[str, None, None]:
        now = Task.now_task()
        now_printed = False

        for t in tasks:

            if not now_printed and Task.comp_task(now) < Task.comp_task(t):
                now_printed = True
                yield f" ----- Now is {now.str_date()} " \
                      f"{now.str_hour()} ----- "

            yield t.display_str()

    @staticmethod
    def create_task(id: int, csv_line: List[str]) -> 'Task':
        ensure(len(csv_line) == len(TaskCategories),
               Error(f"csv line {id} does not have the correct number of "
                     f"fields (expected: {len(TaskCategories)}, actual: "
                     f"{len(csv_line)})"))

        # Get date
        raw_date_due: str = csv_line[TaskCategories.DATE_DUE.value] \
            .replace('/', '')

        ensure(len(raw_date_due) == 4,
               Error(f"csv item {id} does not have 4 digits for the date"))
        try:
            date_due: int = int(raw_date_due)
        except ValueError:
            raise Error(f"csv item {id}'s date due is not an integer")

        # Get time
        raw_hour_due: str = csv_line[TaskCategories.HOUR_DUE.value] \
            .replace(':', '')

        if len(raw_hour_due) != 4:
            raw_hour_due = "2359"

        try:
            hour_due: int = int(raw_hour_due)
        except ValueError:
            raise Error(f"csv item {id}'s hour due is not an integer")

        # Get topic
        topic: str = csv_line[TaskCategories.TOPIC.value]

        # Get task
        task: str = csv_line[TaskCategories.TASK.value]

        # Get status
        raw_status: str = csv_line[TaskCategories.STATUS.value]

        ensure(raw_status == '0' or raw_status == '1',
               Error(f"csv item {id} does not contain a status of 0 or 1"))

        try:
            status: bool = bool(int(raw_status))
        except ValueError:
            raise Error(f"csv item {id}'s status is not a boolean")

        # Assert types
        ensure(type(date_due) == int,
               Error(f"csv item {id}'s date due is not an int"))
        ensure(type(hour_due) == int,
               Error("csv item {id}'s hour due is not an int"))
        ensure(type(topic) == str,
               Error("csv item {id}'s topic is not a string"))
        ensure(type(task) == str,
               Error("csv item {id}'s task is not a string"))
        ensure(type(status) == bool,
               Error("csv item {id}'s status is not a boolean"))

        # Track the longest topic length
        Task.topic_len = max(len(topic), Task.topic_len)

        return Task(id, date_due, hour_due, topic, task, status)

    @staticmethod
    def now_task() -> 'Task':
        now = datetime.now()
        now_date = int(now.strftime("%m%d"))
        now_time = int(now.strftime("%H%M"))
        return Task(-100, now_date, now_time, "", "", False)


class TaskCategories(Enum):
    DATE_DUE = 0
    HOUR_DUE = 1
    TOPIC = 2
    TASK = 3
    STATUS = 4
