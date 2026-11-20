"""Coordinador que administra clientes, servicios y reservas en memoria."""

from pathlib import Path

from .cliente import Cliente
from .excepciones import (
    ClienteNoExiste,
    DatosInvalidos,
    ErrorSistema,
    ReservaInvalida,
    ServicioNoDisponible,
)
from .logger import Logger
from .reserva import EstadoReserva, Reserva
from .servicio import Servicio


class SistemaSoftwareFJ:
    """Gestiona las listas internas y registra eventos y errores."""

    def __init__(self, ruta_log: str | Path = "log_eventos.txt") -> None:
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []
        self.logger = Logger(ruta_log)

    @property
    def clientes(self) -> tuple[Cliente, ...]:
        return tuple(self._clientes)

    @property
    def servicios(self) -> tuple[Servicio, ...]:
        return tuple(self._servicios)

    @property
    def reservas(self) -> tuple[Reserva, ...]:
        return tuple(self._reservas)

    def agregar_cliente(self, cliente: Cliente) -> None:
        try:
            if not isinstance(cliente, Cliente):
                raise DatosInvalidos("Solo se pueden registrar objetos Cliente.")
            if any(actual.codigo == cliente.codigo for actual in self._clientes):
                raise DatosInvalidos(f"Ya existe el cliente con codigo {cliente.codigo}.")
            self._clientes.append(cliente)
            self.logger.registrar_evento(f"Cliente registrado: {cliente}")
        except ErrorSistema as error:
            self.logger.registrar_error("No se pudo registrar el cliente", error)
            raise

    def agregar_servicio(self, servicio: Servicio) -> None:
        try:
            if not isinstance(servicio, Servicio):
                raise DatosInvalidos("Solo se pueden registrar objetos Servicio.")
            if any(actual.codigo == servicio.codigo for actual in self._servicios):
                raise DatosInvalidos(f"Ya existe el servicio con codigo {servicio.codigo}.")
            self._servicios.append(servicio)
            self.logger.registrar_evento(f"Servicio agregado: {servicio}")
        except ErrorSistema as error:
            self.logger.registrar_error("No se pudo agregar el servicio", error)
            raise

    def _buscar_cliente(self, codigo: str) -> Cliente:
        for cliente in self._clientes:
            if cliente.codigo == codigo:
                return cliente
        raise ClienteNoExiste(f"No existe el cliente con codigo {codigo}.")

    def buscar_cliente(self, codigo: str) -> Cliente:
        try:
            return self._buscar_cliente(codigo)
        except ErrorSistema as error:
            self.logger.registrar_error("Error al buscar un cliente", error)
            raise

    def _buscar_servicio(self, codigo: str) -> Servicio:
        for servicio in self._servicios:
            if servicio.codigo == codigo:
                return servicio
        raise ServicioNoDisponible(f"No existe el servicio con codigo {codigo}.")

    def buscar_servicio(self, codigo: str) -> Servicio:
        try:
            return self._buscar_servicio(codigo)
        except ErrorSistema as error:
            self.logger.registrar_error("Error al buscar un servicio", error)
            raise

    def crear_reserva(
        self, codigo_cliente: str, codigo_servicio: str, duracion_horas: object
    ) -> Reserva:
        try:
            cliente = self._buscar_cliente(codigo_cliente)
            servicio = self._buscar_servicio(codigo_servicio)
            servicio.validar_parametros(duracion_horas)
            reserva = Reserva(cliente, servicio, duracion_horas)
            self._reservas.append(reserva)
            self.logger.registrar_evento(f"Reserva creada: {reserva}")
            return reserva
        except ErrorSistema as error:
            self.logger.registrar_error("No se pudo crear la reserva", error)
            raise

    def confirmar_reserva(self, reserva: Reserva) -> None:
        try:
            self._validar_reserva_registrada(reserva)
            reserva.confirmar()
            self.logger.registrar_evento(f"Reserva confirmada: {reserva}")
        except ErrorSistema as error:
            self.logger.registrar_error("No se pudo confirmar la reserva", error)
            raise

    def cancelar_reserva(self, reserva: Reserva) -> None:
        try:
            self._validar_reserva_registrada(reserva)
            reserva.cancelar()
            self.logger.registrar_evento(f"Reserva cancelada: {reserva}")
        except ErrorSistema as error:
            self.logger.registrar_error("No se pudo cancelar la reserva", error)
            raise

    def procesar_reserva(self, reserva: Reserva):
        try:
            self._validar_reserva_registrada(reserva)
            costo = reserva.procesar()
            self.logger.registrar_evento(
                f"Reserva procesada: {reserva} | Costo: {costo}"
            )
            return costo
        except ErrorSistema as error:
            self.logger.registrar_error("No se pudo procesar la reserva", error)
            raise

    def _validar_reserva_registrada(self, reserva: Reserva) -> None:
        if not isinstance(reserva, Reserva) or reserva not in self._reservas:
            raise ReservaInvalida("La reserva no pertenece a este sistema.")

    def cerrar(self) -> None:
        self.logger.cerrar()
