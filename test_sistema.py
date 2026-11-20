"""Pruebas basicas del sistema Software FJ."""

import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from software_fj.cliente import Cliente
from software_fj.excepciones import (
    ClienteNoExiste,
    DatosInvalidos,
    ParametroFaltante,
    ReservaInvalida,
    ServicioNoDisponible,
)
from software_fj.reserva import EstadoReserva
from software_fj.servicio import ServicioSala
from software_fj.sistema import SistemaSoftwareFJ


class SistemaSoftwareFJTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        ruta_log = Path(self.temp_dir.name) / "eventos.log"
        self.sistema = SistemaSoftwareFJ(ruta_log)
        self.cliente = Cliente(
            "C001", "Ana Torres", "12345678", "ana@example.com", "3001234567"
        )
        self.servicio = ServicioSala("S001", "Sala Norte", 100, capacidad=10)
        self.sistema.agregar_cliente(self.cliente)
        self.sistema.agregar_servicio(self.servicio)

    def tearDown(self) -> None:
        self.sistema.cerrar()
        self.temp_dir.cleanup()

    def test_crea_confirma_y_procesa_reserva(self) -> None:
        reserva = self.sistema.crear_reserva("C001", "S001", 2)
        self.sistema.confirmar_reserva(reserva)

        costo = self.sistema.procesar_reserva(reserva)

        self.assertEqual(costo, Decimal("238.00"))
        self.assertEqual(reserva.estado, EstadoReserva.PROCESADA)

    def test_rechaza_cliente_inexistente(self) -> None:
        with self.assertRaises(ClienteNoExiste):
            self.sistema.crear_reserva("C999", "S001", 1)

    def test_rechaza_duracion_invalida(self) -> None:
        with self.assertRaises(ParametroFaltante):
            self.sistema.crear_reserva("C001", "S001", 0)

    def test_rechaza_sala_sin_capacidad(self) -> None:
        with self.assertRaises(ServicioNoDisponible):
            self.servicio.calcular_costo(1, capacidad_solicitada=11)

    def test_rechaza_datos_invalidos_de_cliente(self) -> None:
        with self.assertRaises(DatosInvalidos):
            Cliente("C002", "A", "12", "correo", "123")

    def test_log_registra_evento_y_error(self) -> None:
        with self.assertRaises(ClienteNoExiste):
            self.sistema.buscar_cliente("C999")

        log_path = Path(self.temp_dir.name) / "eventos.log"
        contenido = log_path.read_text(encoding="utf-8")
        self.assertIn("Cliente registrado", contenido)
        self.assertIn("Error al buscar un cliente", contenido)

    def test_reserva_cancelada_no_se_procesa(self) -> None:
        reserva = self.sistema.crear_reserva("C001", "S001", 1)
        self.sistema.cancelar_reserva(reserva)

        with self.assertRaises(ReservaInvalida):
            self.sistema.procesar_reserva(reserva)


if __name__ == "__main__":
    unittest.main()
