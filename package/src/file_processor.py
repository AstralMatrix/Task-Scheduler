import csv
from typing import List, Iterator
from package.src.task import Task


class FileProcessor:

    @staticmethod
    def load_csv(file_path: str) -> List[Task]:
        with open(file_path) as f:
            data: Iterator = csv.reader(f)
            return FileProcessor.extract_csv_data(data)

    @staticmethod
    def extract_csv_data(csv_reader: Iterator) -> List[Task]:
        next(csv_reader)  # Remove csv header.
        return Task.minimize_lateness(
            [Task.create_task(i, x) for i, x in enumerate(csv_reader)]
        )
