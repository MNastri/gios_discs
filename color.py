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

    @classmethod
    def from_int(cls, s):
        color_kind = COLOR_MAP[s]
        return cls(color_kind)

    def __repr__(self):
        return f"{self.color.name}"
