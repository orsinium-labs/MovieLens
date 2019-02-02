from typing import Optional
import attr


@attr.s()
class Prediction:
    user: int = attr.ib()
    movie: int = attr.ib()

    predicted: float = attr.ib()
    real: Optional[int] = attr.ib(default=None)

    def __int__(self):
        return self.predicted

    @property
    def diff(self):
        return abs(self.predicted - self.real)
