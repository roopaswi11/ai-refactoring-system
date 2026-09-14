import csv


class MetricsReader:

    @staticmethod
    def read_metrics():

        metrics = []

        with open("metrics.csv", newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:
                metrics.append(row)

        return metrics