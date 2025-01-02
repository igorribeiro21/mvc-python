from abc import abstractmethod,ABC

class PersonFinderControllerInterface(ABC):

    @abstractmethod
    def find(self, person_id: int) -> dict:
        pass
