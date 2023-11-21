import csv


class CSVObject:
    """
    Class to read and write the captured data to a CSV file.
    """

    def __init__(self, path: str):
        fieldnames = ['frame', 'time', 'index', 'x', 'y', 'z']
        self.writer = csv.DictWriter(open(path, 'w', newline=''), fieldnames=fieldnames)
        self.writer.writeheader()

    def write(self, frame: int, time: int, index: int, x: float, y: float, z: float):
        """
        Write a line to the CSV file
        """
        self.writer.writerow({'frame': frame, 'time': time, 'index': index, 'x': x, 'y': y, 'z': z})
