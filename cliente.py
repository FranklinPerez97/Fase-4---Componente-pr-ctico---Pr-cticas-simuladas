"""Modelo y validaciones de los clientes."""

import re

from .entidad import Entidad
from .excepciones import DatosInvalidos


class Cliente(Entidad):
    """Cliente con datos personales encapsulados."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        documento: str,
        correo: str,
        telefono: str,
    ) -> None:
        super().__init__(codigo, nombre)
        self.__documento = documento.strip() if isinstance(documento, str) else ""
        self.__correo = correo.strip() if isinstance(correo, str) else ""
        self.__telefono = telefono.strip() if isinstance(telefono, str) else ""
        self.validar_datos()

    @property
    def documento(self) -> str:
        return self.__documento

    @property
    def correo(self) -> str:
        return self.__correo

    @property
    def telefono(self) -> str:
        return self.__telefono

    def validar_datos(self) -> None:
        if len(self.nombre) < 3:
            raise DatosInvalidos("El nombre debe tener al menos 3 caracteres.")
        if not re.fullmatch(r"[A-Za-z0-9-]{5,20}", self.__documento):
            raise DatosInvalidos(
                "El documento debe tener entre 5 y 20 letras, numeros o guiones."
            )
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", self.__correo):
            raise DatosInvalidos("El correo electronico no tiene un formato valido.")
        digitos = re.sub(r"\D", "", self.__telefono)
        if not 7 <= len(digitos) <= 15:
            raise DatosInvalidos("El telefono debe contener entre 7 y 15 digitos.")

    def __str__(self) -> str:
        return f"Cliente[{self.codigo}] {self.nombre}"
