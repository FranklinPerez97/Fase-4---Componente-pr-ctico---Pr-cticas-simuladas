"""Excepciones propias del sistema Software FJ."""


class ErrorSistema(Exception):
    """Clase base para los errores controlados de la aplicacion."""


class DatosInvalidos(ErrorSistema):
    """Se recibieron datos que no cumplen las reglas del sistema."""


class ParametroFaltante(DatosInvalidos):
    """Falta un parametro obligatorio o su valor no es valido."""


class ClienteNoExiste(ErrorSistema):
    """No se encontro el cliente solicitado."""


class ServicioNoDisponible(ErrorSistema):
    """El servicio no existe o no esta disponible."""


class ReservaInvalida(ErrorSistema):
    """La reserva no puede crearse ni cambiar de estado."""
