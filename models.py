from dataclasses import dataclass


@dataclass
class X:
    num: int
    # (1,3) -> primera posicion fila y segunda posicion columna.
    posicion: tuple[int, int]
    asignado: bool = False
    marcado: int = 0
    oculto: bool = False

    def marcar(self):
        self.marcado += 1
