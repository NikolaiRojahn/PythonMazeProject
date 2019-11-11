import csv
from csvFileWriter import csvFileWriter
from csvFileReader import csvFileReader


class FileFacade:

    # static variables.
    __instance = None

    @staticmethod
    def getInstance():
        if FileFacade.__instance is None:
            FileFacade()
        return FileFacade.__instance

    # constructor
    def __init__(self):
        # do we already have an instance, raise exception.
        if FileFacade.__instance is not None:
            raise Exception(
                "FileFacade is a singleton, use FileFacade.getInstance() to obtain instance.")
        else:  # no instance yet, store self as instance.
            FileFacade.__instance = self

    def createWriter(self, mazes, file):
        extension = self.__checkFileType(file)

        if (extension == 'csv'):
            csvFileWriter.write(self, mazes, file)
        else:
            raise Exception("File format doesn't exist")

    def __checkFileType(self, file):
        fileExtension = ""
        # To reverse the file so .csv will be vsc.
        fileReversed = self.reverse(file)

        # As the filename is reversed, we will build the string from first char until we reach the dot.
        for char in fileReversed:
            if (char is not '.'):
                fileExtension += char
            else:
                return self.reverse(fileExtension)

    def reverse(self, string):
        str = ""
        for i in string:
            str = i + str
        return str

    def read(self, filename):
        """Reads from the specified filename"""
        raise NotImplementedError()

    def write(self, filename, mazes):
        self.createWriter(mazes, filename)
