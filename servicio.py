"""Servicio abstracto y sus tres implementaciones concretas."""

from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from .excepciones import (
    DatosInvalidos,
    ParametroFaltante,
    ServicioNoDisponible,
)

CENTAVO = Decimal("0.01")


def _decimal_positivo(valor: object, nombre: str) -> Decimal:
    if isinstance(valor, bool):
        raise DatosInvalidos(f"{nombre} debe ser un numero positivo.")
    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, ValueError):
        raise DatosInvalidos(f"{nombre} debe ser un numero valido.") from None
    if not numero.is_finite() or numero <= 0:
        raise DatosInvalidos(f"{nombre} debe ser mayor que cero.")
    return numero


def _validar_porcentaje(valor: object, nombre: str, maximo: int) -> Decimal:
    if isinstance(valor, bool):
        raise DatosInvalidos(f"{nombre} debe estar entre 0 y {maximo}.")
    try:
        porcentaje = Decimal(str(valor))
    except (InvalidOperation, ValueError):
        raise DatosInvalidos(f"{nombre} debe ser un numero valido.") from None
    if not porcentaje.is_finite() or not Decimal("0") <= porcentaje <= Decimal(maximo):
        raise DatosInvalidos(f"{nombre} debe estar entre 0 y {maximo}.")
    return porcentaje


class Servicio(ABC):
    """Contrato comun para cualquier servicio ofrecido por la empresa."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        costo_base: int | float | Decimal,
        disponible: bool = True,
    ) -> None:
        if not isinstance(codigo, str) or not codigo.strip():
            raise DatosInvalidos("El codigo del servicio no puede estar vacio.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidos("El nombre del servicio no puede estar vacio.")
        if not isinstance(disponible, bool):
            raise DatosInvalidos("La disponibilidad debe ser un valor booleano.")

        self._codigo = codigo.strip()
        self._nombre = nombre.strip()
        self._costo_base = _decimal_positivo(costo_base, "El costo base")
        self._disponible = disponible

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def costo_base(self) -> Decimal:
        return self._costo_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatosInvalidos("La disponibilidad debe ser un valor booleano.")
        self._disponible = valor

    def _validar_duracion_y_disponibilidad(self, duracion: object) -> Decimal:
        try:
            horas = _decimal_positivo(duracion, "La duracion")
        except DatosInvalidos as error:
            raise ParametroFaltante(str(error)) from error
        if not self._disponible:
            raise ServicioNoDisponible(f"El servicio '{self.nombre}' no esta disponible.")
        return horas

    def _calcular_total(
        self,
        duracion: Decimal,
        descuento: int | float | Decimal,
        impuesto: int | float | Decimal,
    ) -> Decimal:
        descuento_pct = _validar_porcentaje(descuento, "El descuento", 100)
        impuesto_pct = _validar_porcentaje(impuesto, "El impuesto", 100)
        subtotal = self._costo_base * duracion
        subtotal_con_descuento = subtotal * (Decimal("1") - descuento_pct / 100)
        total = subtotal_con_descuento * (Decimal("1") + impuesto_pct / 100)
        return total.quantize(CENTAVO, rounding=ROUND_HALF_UP)

    @abstractmethod
    def validar_parametros(self, duracion: object, **kwargs: object) -> None:
        """Valida los parametros propios del tipo de servicio."""

    @abstractmethod
    def calcular_costo(
        self,
        duracion: object,
        descuento: int | float | Decimal = 0,
        impuesto: int | float | Decimal = 19,
        **kwargs: object,
    ) -> Decimal:
        """Calcula el costo, con parametros opcionales de descuento e impuesto."""

    @abstractmethod
    def descripcion(self) -> str:
        """Devuelve una descripcion del servicio."""

    def __str__(self) -> str:
        return f"Servicio[{self.codigo}] {self.nombre}"


class ServicioSala(Servicio):
    def __init__(
        self,
        codigo: str,
        nombre: str,
        costo_base: int | float | Decimal,
        capacidad: int,
        disponible: bool = True,
    ) -> None:
        super().__init__(codigo, nombre, costo_base, disponible)
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidos("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    @property
    def capacidad(self) -> int:
        return self._capacidad

    def validar_parametros(
        self, duracion: object, capacidad_solicitada: object = None, **kwargs: object
    ) -> None:
        self._validar_duracion_y_disponibilidad(duracion)
        if capacidad_solicitada is not None:
            if (
                isinstance(capacidad_solicitada, bool)
                or not isinstance(capacidad_solicitada, int)
                or capacidad_solicitada <= 0
            ):
                raise DatosInvalidos("La capacidad solicitada debe ser un entero positivo.")
            if capacidad_solicitada > self._capacidad:
                raise ServicioNoDisponible("La sala no tiene la capacidad requerida.")

    def calcular_costo(
        self,
        duracion: object,
        descuento: int | float | Decimal = 0,
        impuesto: int | float | Decimal = 19,
        capacidad_solicitada: object = None,
    ) -> Decimal:
        self.validar_parametros(duracion, capacidad_solicitada)
        horas = _decimal_positivo(duracion, "La duracion")
        return self._calcular_total(horas, descuento, impuesto)

    def descripcion(self) -> str:
        return f"Sala '{self.nombre}' con capacidad para {self._capacidad} personas."


class ServicioEquipo(Servicio):
    def __init__(
        self,
        codigo: str,
        nombre: str,
        costo_base: int | float | Decimal,
        tipo_equipo: str,
        disponible: bool = True,
    ) -> None:
        super().__init__(codigo, nombre, costo_base, disponible)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise DatosInvalidos("El tipo de equipo no puede estar vacio.")
        self._tipo_equipo = tipo_equipo.strip()

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    def validar_parametros(
        self, duracion: object, tipo_equipo: object = None, **kwargs: object
    ) -> None:
        self._validar_duracion_y_disponibilidad(duracion)
        if tipo_equipo is not None and tipo_equipo != self._tipo_equipo:
            raise ServicioNoDisponible("El tipo de equipo solicitado no coincide.")

    def calcular_costo(
        self,
        duracion: object,
        descuento: int | float | Decimal = 0,
        impuesto: int | float | Decimal = 19,
        tipo_equipo: object = None,
    ) -> Decimal:
        self.validar_parametros(duracion, tipo_equipo)
        horas = _decimal_positivo(duracion, "La duracion")
        return self._calcular_total(horas, descuento, impuesto)

    def descripcion(self) -> str:
        return f"Alquiler de '{self.nombre}', equipo tipo {self._tipo_equipo}."


class ServicioAsesoria(Servicio):
    def __init__(
        self,
        codigo: str,
        nombre: str,
        costo_base: int | float | Decimal,
        especialidad: str,
        disponible: bool = True,
    ) -> None:
        super().__init__(codigo, nombre, costo_base, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidos("La especialidad no puede estar vacia.")
        self._especialidad = especialidad.strip()

    @property
    def especialidad(self) -> str:
        return self._especialidad

    def validar_parametros(
        self, duracion: object, especialidad: object = None, **kwargs: object
    ) -> None:
        self._validar_duracion_y_disponibilidad(duracion)
        if especialidad is not None and especialidad != self._especialidad:
            raise ServicioNoDisponible("La especialidad solicitada no esta disponible.")

    def calcular_costo(
        self,
        duracion: object,
        descuento: int | float | Decimal = 0,
        impuesto: int | float | Decimal = 19,
        especialidad: object = None,
    ) -> Decimal:
        self.validar_parametros(duracion, especialidad)
        horas = _decimal_positivo(duracion, "La duracion")
        return self._calcular_total(horas, descuento, impuesto)

    def descripcion(self) -> str:
        return f"Asesoria '{self.nombre}' en {self._especialidad}."
