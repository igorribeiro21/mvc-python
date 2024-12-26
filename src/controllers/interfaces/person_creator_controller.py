from abc import abstractmethod,ABC

class PersonCreatorControllerInterface(ABC):

    @abstractmethod
    def create(self, person_info: dict) -> dict:
        pass
