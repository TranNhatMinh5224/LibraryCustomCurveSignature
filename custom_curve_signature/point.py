# point.py
from dataclasses import dataclass
from typing import Optional

from .field import mod, mod_inv
from .curve import TNM5224


@dataclass(frozen=True)
class Point:
    x: Optional[int]
    y: Optional[int]
    curve: object = TNM5224

    # Kiểm tra điểm vô cực
    def is_infinity(self) -> bool:
        return self.x is None and self.y is None

    # Trả về điểm vô cực
    @staticmethod
    def infinity():
        return Point(None, None)

    # Kiểm tra điểm có nằm trên đường cong không
    # y^2 ≡ x^3 + ax + b (mod p)
    def is_on_curve(self) -> bool:
        if self.is_infinity():
            return True

        p = self.curve.p
        a = self.curve.a
        b = self.curve.b

        left = mod(self.y * self.y, p)
        right = mod(self.x**3 + a * self.x + b, p)

        return left == right

    # Trả về điểm đối (x, -y mod p)
    def negate(self):
        if self.is_infinity():
            return self
        return Point(self.x, mod(self.curve.p - self.y, self.curve.p))

    # Cộng hai điểm elliptic
    def add(self, other):
        p = self.curve.p

        if self.is_infinity():
            return other
        if other.is_infinity():
            return self

        if self.x == other.x:
            if self.y != other.y:
                return Point.infinity()
            else:
                return self.double()

        slope = mod(
            (other.y - self.y) * mod_inv(other.x - self.x, p),
            p
        )

        x3 = mod(slope * slope - self.x - other.x, p)
        y3 = mod(slope * (self.x - x3) - self.y, p)

        return Point(x3, y3)

    # Nhân đôi điểm
    def double(self):
        if self.is_infinity():
            return self

        p = self.curve.p
        a = self.curve.a

        slope = mod(
            (3 * self.x * self.x + a) * mod_inv(2 * self.y, p),
            p
        )

        x3 = mod(slope * slope - 2 * self.x, p)
        y3 = mod(slope * (self.x - x3) - self.y, p)

        return Point(x3, y3)

    # Nhân điểm với số nguyên k (double-and-add)
    def multiply(self, k: int):
        result = Point.infinity()
        addend = self

        while k > 0:
            if k & 1:
                result = result.add(addend)
            addend = addend.double()
            k >>= 1

        return result
