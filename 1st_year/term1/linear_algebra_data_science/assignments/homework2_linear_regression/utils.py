import numpy as np

class Pseudosolution():
    def __init__(self, shapes: tuple=(2,1)) -> None:
        self.coefficients = np.ones(shapes)
        self.shapes = shapes

    def fit(self, X: np.array, y: np.array) -> None:
        self.pseudo = np.linalg.pinv(X)
        assert self.pseudo.shape[-1] == y.shape[0], "Check shapes"
        self.coefficients = (self.pseudo @ y).flatten()
    def predict(self, day: int=23, type_: str='temperature') -> None:
        predicted_value = self.coefficients @ np.array([day, 1])
        print(f"Predicted {type_}", predicted_value, sep=": ")