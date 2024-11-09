import os


class FileHandler:

    def __init__(self,  filepath):
        self.setFilepath(filepath)
        with open(filepath, mode='rb') as file:
            self.raw_data = file.read()
            file.close()

    def getName(self):
        return self.filepath.split('/')[-1]

    def getFilepath(self):
        return self.filepath

    def setFilepath(self, filepath):
        self.filepath = filepath

