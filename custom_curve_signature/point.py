from dataclasses import dataclass
from typing import Optional
from .field import mod, mod_inv
from .curve import TNM5224


@dataclass(frozen=True)
class Point:
    x: Optional[int]
    y: Optional[int]
    z: Optional[int] = 1
    curve: object = TNM5224

    @staticmethod
    def infinity():
        return Point(None, None, 0)

    def is_infinity(self) -> bool:
        return self.z == 0

    # =========================
    # Convert to affine
    # =========================
    def to_affine(self):
        if self.is_infinity():
            return Point.infinity()

        if self.z == 1:
            return self

        p = self.curve.p
        z_inv = mod_inv(self.z, p)
        z2 = mod(z_inv * z_inv, p)
        z3 = mod(z2 * z_inv, p)

        x = mod(self.x * z2, p)
        y = mod(self.y * z3, p)

        return Point(x, y, 1)

    # =========================
    # Check on curve (affine)
    # =========================
    def is_on_curve(self) -> bool:
        if self.is_infinity():
            return True

        P = self.to_affine()
        p = self.curve.p
        a = self.curve.a
        b = self.curve.b

        left = mod(P.y * P.y, p)
        right = mod(P.x**3 + a * P.x + b, p)
        return left == right

    # =========================
    # Jacobian Double
    # =========================
    def double(self):
        if self.is_infinity():
            return self

        p = self.curve.p
        a = self.curve.a

        X1, Y1, Z1 = self.x, self.y, self.z

        if Y1 == 0:
            return Point.infinity()

        Y1_sq = mod(Y1 * Y1, p)
        S = mod(4 * X1 * Y1_sq, p)
        Z1_sq = mod(Z1 * Z1, p)
        Z1_4 = mod(Z1_sq * Z1_sq, p)
        M = mod(3 * X1 * X1 + a * Z1_4, p)

        X3 = mod(M * M - 2 * S, p)
        Y1_4 = mod(Y1_sq * Y1_sq, p)
        Y3 = mod(M * (S - X3) - 8 * Y1_4, p)
        Z3 = mod(2 * Y1 * Z1, p)

        return Point(X3, Y3, Z3)

    # =========================
    # Jacobian Add
    # =========================
    def add(self, other):
        if self.is_infinity():
            return other
        if other.is_infinity():
            return self

        p = self.curve.p

        X1, Y1, Z1 = self.x, self.y, self.z
        X2, Y2, Z2 = other.x, other.y, other.z

        Z1_sq = mod(Z1 * Z1, p)
        Z2_sq = mod(Z2 * Z2, p)

        U1 = mod(X1 * Z2_sq, p)
        U2 = mod(X2 * Z1_sq, p)

        Z1_cu = mod(Z1_sq * Z1, p)
        Z2_cu = mod(Z2_sq * Z2, p)

        S1 = mod(Y1 * Z2_cu, p)
        S2 = mod(Y2 * Z1_cu, p)

        if U1 == U2:
            if S1 != S2:
                return Point.infinity()
            return self.double()

        H = mod(U2 - U1, p)
        R = mod(S2 - S1, p)

        H_sq = mod(H * H, p)
        H_cu = mod(H_sq * H, p)
        U1_H_sq = mod(U1 * H_sq, p)

        X3 = mod(R * R - H_cu - 2 * U1_H_sq, p)
        Y3 = mod(R * (U1_H_sq - X3) - S1 * H_cu, p)
        Z3 = mod(H * Z1 * Z2, p)

        return Point(X3, Y3, Z3)

    # =========================
    # Montgomery Ladder
    # =========================
    def multiply(self, k: int):
        if k == 0 or self.is_infinity():
            return Point.infinity()

        R0 = Point.infinity()
        R1 = self

        for i in reversed(range(k.bit_length())):
            bit = (k >> i) & 1
            if bit == 0:
                R1 = R0.add(R1)
                R0 = R0.double()
            else:
                R0 = R0.add(R1)
                R1 = R1.double()

        return R0.to_affine()
