import csv


class CSVHandler(object):

    def getFile(self, path):
        with open(path, mode="r", newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            content = []
            for line in reader:
                content.append(line)
        return content

    def saveFile(self, path, content):
        with open(path, mode="w", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            csvfile.truncate()
            for line in content:
                writer.writerow(line)

