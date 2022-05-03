from enum import Enum


class ColorKind(Enum):
    AM = "Amarelo"
    AZ = "Azul"
    BR = "Branco"
    VD = "Verde"
    VM = "Vermelho"
    PR = "Preto"


COLOR_MAP = {
    0: ColorKind.AM,
    1: ColorKind.AZ,
    2: ColorKind.BR,
    3: ColorKind.VD,
    4: ColorKind.VM,
    5: ColorKind.PR,
}


class Color:
    def __init__(self, color: ColorKind):
        """Constructor for Color"""
        self.color = color

    def __repr__(self):
        return f"{self.color.name}"

    def __eq__(self, other):
        if self.color.value == other.color.value:
            return True
        return False

    @classmethod
    def from_int(cls, i):
        color_kind = COLOR_MAP[i]
        return cls(color_kind)
