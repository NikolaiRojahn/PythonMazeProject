import csv
from csvFileWriter import csvFileWriter
from csvFileReader import csvFileReader

class FileFacade:

    def __init__(self):
        self.numberOfSizes = 0

    def read(self, file):
        extension = self.__checkFileType(file)

        if (extension == 'csv'):
            mazesAllSize = csvFileReader.read(self, file)
            csvFileReader.numberOfSizes = self.numberOfSizes
            return mazesAllSize

    def write(self, mazes, file):
        self.__createWriter(mazes, file)

    def __createWriter(self, mazes, file):
        extension = self.__checkFileType(file)
        
        if (extension == 'csv'):
            csvFileWriter.write(self, mazes, file)
        else:
            raise Exception("File format doesn't exist")

    def __checkFileType(self, file):
        fileExtension = ""
        #To reverse the file so .csv will be vsc.
        fileReversed = self.reverse(file)

        #As the filename is reversed, we will build the string from first char until we reach the dot.
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

            


