import csv


class CSVHandler(object):
    """
    This class is used to read and write a csv-file.
    """
    def getFile(self, path):
        """
        Returns the content of the file.

        :param path: The path and name of the file
        :return: The content as an array of rows. The rows are also arrays with the cells
        """
        with open(path, mode="r", newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            content = []
            for line in reader:
                content.append(line)
        return content

    def saveFile(self, path, content):
        """
        Writes the given content to a csv-file.

        :param path: The path and name of the file
        :param content: The content that should be writen
        :return: None
        """
        with open(path, mode="w", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            csvfile.truncate()
            for line in content:
                writer.writerow(line)

