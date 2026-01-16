# field.py

def mod(x: int, p: int) -> int:
   
    return x % p


def mod_inv(x: int, p: int) -> int:

    if x == 0:
        raise ZeroDivisionError("Inverse of zero does not exist")
    return pow(x, -1, p)
