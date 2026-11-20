"""Abstraccion base para las entidades identificables del sistema."""

from abc import ABC, abstractmethod

from .excepciones import DatosInvalidos


class Entidad(ABC):
    """Define los atributos comunes de una entidad del sistema."""

    def __init__(self, codigo: str, nombre: str) -> None:
        if not isinstance(codigo, str) or not codigo.strip():
            raise DatosInvalidos("El codigo debe ser un texto no vacio.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidos("El nombre debe ser un texto no vacio.")

        self._codigo = codigo.strip()
        self._nombre = nombre.strip()

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @abstractmethod
    def validar_datos(self) -> None:
        """Valida los datos especificos de la entidad."""
