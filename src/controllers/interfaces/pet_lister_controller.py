from abc import abstractmethod,ABC
from typing import Dict

class PetListerControllerInterface(ABC):

    @abstractmethod
    def list(self) -> Dict:
        pass
