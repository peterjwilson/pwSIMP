from abc import ABCMeta, abstractmethod

class process(metaclass=ABCMeta):
    @abstractmethod
    def implementProcess(self,stiffness_matrix,mass_matrix,force_vector):
        pass
