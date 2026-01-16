# curve.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Curve:
    name: str
    p: int
    a: int
    b: int
    Gx: int
    Gy: int
    n: int
    h: int


# Định nghĩa đường cong elliptic TNM5224 
TNM5224 = Curve(
    name="TNM5224",
    p=int(
        "b63c11d43e09b729962d47edb6ddab7a929ed7aa6e7f01da8ca3f72022037373",
        16
    ),
    a=int(
        "b63c11d43e09b729962d47edb6ddab7a929ed7aa6e7f01da8ca3f72022037370",
        16
    ),
    b=int(
        "9ced8b5e0375c92d55fff25924233e0ca2338392d8c8bcc2d8b42b0fe1418a95",
        16
    ),
    Gx=int(
        "61fec3112fa5e7aa1779cc56bcf2bdd7326982cc69693bc92908fedf007dffd9",
        16
    ),
    Gy=int(
        "0890dd8c564d7601b0a8e4ce5aba2ad6a3bad24deb8d1e1b6f18d0beb70e1c1d",
        16
    ),
    n=int(
        "b63c11d43e09b729962d47edb6ddab7ba1a80e44874c71dfbf9419280fa3d971",
        16
    ),
    h=1
)
