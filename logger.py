"""Registro de eventos y errores en un archivo de texto."""

import logging
from pathlib import Path


class Logger:
    """Escribe eventos del sistema en un archivo con codificacion UTF-8."""

    def __init__(self, ruta_log: str | Path = "log_eventos.txt") -> None:
        self.ruta_log = Path(ruta_log)
        self.ruta_log.parent.mkdir(parents=True, exist_ok=True)

        self._logger = logging.getLogger(f"software_fj.{self.ruta_log.resolve()}")
        self._logger.setLevel(logging.INFO)
        self._logger.propagate = False

        if not self._logger.handlers:
            manejador = logging.FileHandler(self.ruta_log, encoding="utf-8")
            manejador.setFormatter(
                logging.Formatter(
                    "%(asctime)s | %(levelname)s | %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
            self._logger.addHandler(manejador)

    def registrar_evento(self, mensaje: str) -> None:
        self._logger.info(mensaje)

    def registrar_error(self, mensaje: str, error: Exception) -> None:
        self._logger.error("%s | %s: %s", mensaje, type(error).__name__, error)

    def cerrar(self) -> None:
        for manejador in self._logger.handlers[:]:
            manejador.close()
            self._logger.removeHandler(manejador)
