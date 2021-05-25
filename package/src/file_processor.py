import csv
from typing import List, Iterator
from package.src.task import Task
from package.src.error import Error


class FileProcessor:

    @staticmethod
    def load_csv(file_path: str) -> List[Task]:
        try:
            with open(file_path, encoding='utf-8', errors='strict') as f:
                data: Iterator = csv.reader(f)
                return FileProcessor.extract_csv_data(data)
        except FileNotFoundError:
            raise Error(f"The file \"{file_path}\" does not exist")

    @staticmethod
    def extract_csv_data(csv_reader: Iterator) -> List[Task]:
        next(csv_reader)  # Remove csv header.
        return Task.minimize_lateness(
            [Task.create_task(i, x) for i, x in enumerate(csv_reader)]
        )
