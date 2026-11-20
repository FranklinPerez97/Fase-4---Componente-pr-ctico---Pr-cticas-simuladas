"""Modelo y transiciones de estado de las reservas."""

from decimal import Decimal
from enum import Enum

from .cliente import Cliente
from .excepciones import DatosInvalidos, ReservaInvalida
from .servicio import Servicio, _decimal_positivo


class EstadoReserva(Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    PROCESADA = "procesada"


class Reserva:
    """Relaciona un cliente con un servicio y controla su estado."""

    def __init__(self, cliente: Cliente, servicio: Servicio, duracion_horas: object) -> None:
        if not isinstance(cliente, Cliente):
            raise ReservaInvalida("La reserva requiere un cliente valido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalida("La reserva requiere un servicio valido.")
        try:
            self._duracion_horas = _decimal_positivo(duracion_horas, "La duracion")
        except DatosInvalidos as error:
            raise ReservaInvalida(str(error)) from error

        self._cliente = cliente
        self._servicio = servicio
        self._estado = EstadoReserva.PENDIENTE
        self._costo: Decimal | None = None

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def duracion_horas(self) -> Decimal:
        return self._duracion_horas

    @property
    def estado(self) -> EstadoReserva:
        return self._estado

    @property
    def costo(self) -> Decimal | None:
        return self._costo

    def confirmar(self) -> None:
        if self._estado is not EstadoReserva.PENDIENTE:
            raise ReservaInvalida("Solo se puede confirmar una reserva pendiente.")
        self._estado = EstadoReserva.CONFIRMADA

    def cancelar(self) -> None:
        if self._estado not in (EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA):
            raise ReservaInvalida("Solo se puede cancelar una reserva pendiente o confirmada.")
        self._estado = EstadoReserva.CANCELADA

    def procesar(self) -> Decimal:
        if self._estado is not EstadoReserva.CONFIRMADA:
            raise ReservaInvalida("Solo se puede procesar una reserva confirmada.")
        try:
            self._costo = self._servicio.calcular_costo(self._duracion_horas)
        except DatosInvalidos as error:
            raise ReservaInvalida("No se pudo calcular el costo de la reserva.") from error
        self._estado = EstadoReserva.PROCESADA
        return self._costo

    def __str__(self) -> str:
        return (
            f"Reserva({self._cliente.nombre} - {self._servicio.nombre} - "
            f"{self._duracion_horas} horas - {self._estado.value})"
        )
