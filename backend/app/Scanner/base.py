from abc import ABC, abstractmethod

from backend.app.models.schemas import HttpRequest, Finding


class BaseScanner(ABC):

    name: str = "BaseScanner"

    @abstractmethod
    async def scan(self, request: HttpRequest) -> list[Finding]:
        pass