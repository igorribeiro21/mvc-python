from abc import abstractmethod,ABC

class PetDeleterControllerInterface(ABC):

    @abstractmethod
    def delete(self, name: str) -> None:
        pass
