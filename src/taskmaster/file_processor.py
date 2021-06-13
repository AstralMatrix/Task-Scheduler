import csv
from typing import List, Iterator
from task import Task
from error import Error


class FileProcessor:

    @staticmethod
    def load_csv(file_path: str) -> List[Task]:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='strict') as f:
                data: Iterator = csv.reader(f)
                try:
                    return FileProcessor.extract_csv_data(data)
                except UnicodeDecodeError:
                    raise Error(f"Cannot load, the file \"{file_path}\" can "
                                f"not be read, please ensure it is a UTF-8 "
                                f"encoded file")
        except FileNotFoundError:
            raise Error(f"Cannot load, the file \"{file_path}\" does not exist")

    @staticmethod
    def extract_csv_data(csv_reader: Iterator) -> List[Task]:
        return Task.minimize_lateness(
            [Task.create_task(i, x) for i, x in enumerate(csv_reader)]
        )

    @staticmethod
    def save_csv(file_path: str, data: List[str]) -> None:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for d in data:
                    f.write(d + '\n')
        except FileNotFoundError:
            raise Error(f"Cannot save, the file \"{file_path}\" does not exist")
