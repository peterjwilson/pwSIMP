

class processData:
    def __init__(self):
        self.process_vector = [] #holds references to each process

    def addProcess(self,process_in):
        self.process_vector.append(process_in)