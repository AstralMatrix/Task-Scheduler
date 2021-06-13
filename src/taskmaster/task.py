import re
from enum import Enum
from typing import List, Generator
from datetime import datetime
from package.src.error import Error


class Task:

    topic_len: int = 0
    display_spaces: int = 2
    data_pattern = re.compile(
        r'''^(([0][1-9])|([1][0-2]))\/?(([0][1-9])|([1-2][0-9])|([3][0-1])),((([
0-1][0-9])|([2][0-3])):?[0-5][0-9])?,[^,"]*,[^,"]*,[01]$''')

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

    def toCsvString(self) -> str:
        def inserted(x, y, z):
            x.insert(y, z)
            return x
        dd: str = ''.join(inserted(list(str(self.date_due).zfill(4)), 2, '/'))
        hd: str = ''.join(inserted(list(str(self.hour_due).zfill(4)), 2, ':'))
        tp: str = self.topic
        ta: str = self.task
        st: str = str(int(self.status))
        return f"{dd},{hd},{tp},{ta},{st}"

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
    def reset_topic_len():
        Task.topic_len = 0

    @staticmethod
    def create_task(id: int, csv_line: List[str]) -> 'Task':
        stripped_line: List[str] = list(map(lambda x: x.strip(), csv_line))
        string: str = ",".join(stripped_line)
        # Verify the csv string is formated properly
        if not Task.data_pattern.match(string):
            raise Error(f"Line {id+1} is not properly formatted, it does not "
                        f"match the regular expression (formatting in "
                        f"documentation)")
        # Get date
        date_due: int = int(stripped_line[TaskCategories.DATE_DUE.value]
                            .replace('/', ''))
        # Get time
        if stripped_line[TaskCategories.HOUR_DUE.value] == '':
            hour_due: int = 2359
        else:
            hour_due: int = int(stripped_line[TaskCategories.HOUR_DUE.value]
                                .replace(':', ''))
        # Get topic
        topic: str = stripped_line[TaskCategories.TOPIC.value]
        # Get task
        task: str = stripped_line[TaskCategories.TASK.value]
        # Get status
        status: bool = bool(int(stripped_line[TaskCategories.STATUS.value]))

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
