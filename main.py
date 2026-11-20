"""Simulacion de operaciones exitosas y fallidas del sistema."""

from collections.abc import Callable
from typing import TypeVar

from .cliente import Cliente
from .excepciones import ErrorSistema
from .servicio import ServicioAsesoria, ServicioEquipo, ServicioSala
from .sistema import SistemaSoftwareFJ

T = TypeVar("T")


def ejecutar_operacion(
    sistema: SistemaSoftwareFJ, numero: int, descripcion: str, accion: Callable[[], T]
) -> T | None:
    """Ejecuta cada caso por separado para que un error no detenga la simulacion."""
    print(f"\nOperacion {numero}: {descripcion}")
    try:
        resultado = accion()
    except ErrorSistema as error:
        print(f"Error controlado: {error}")
        return None
    else:
        print(f"Resultado: {resultado}")
        return resultado
    finally:
        print(f"Operacion {numero} finalizada.")


def main() -> None:
    sistema = SistemaSoftwareFJ()
    try:
        ejecutar_operacion(
            sistema,
            1,
            "Registrar cliente Ana",
            lambda: sistema.agregar_cliente(
                Cliente("C001", "Ana Torres", "12345678", "ana@example.com", "3001234567")
            ),
        )
        ejecutar_operacion(
            sistema,
            2,
            "Registrar cliente Luis",
            lambda: sistema.agregar_cliente(
                Cliente("C002", "Luis Perez", "87654321", "luis@example.com", "3019876543")
            ),
        )
        ejecutar_operacion(
            sistema,
            3,
            "Intentar crear un cliente con datos invalidos",
            lambda: Cliente("C003", "A", "12", "correo-invalido", "123"),
        )
        ejecutar_operacion(
            sistema,
            4,
            "Agregar servicio de sala",
            lambda: sistema.agregar_servicio(
                ServicioSala("S001", "Sala Norte", 25000, capacidad=20)
            ),
        )
        ejecutar_operacion(
            sistema,
            5,
            "Agregar servicio de alquiler de equipo",
            lambda: sistema.agregar_servicio(
                ServicioEquipo("S002", "Portatil", 15000, tipo_equipo="computador")
            ),
        )
        ejecutar_operacion(
            sistema,
            6,
            "Agregar servicio de asesoria",
            lambda: sistema.agregar_servicio(
                ServicioAsesoria("S003", "Asesoria tecnica", 30000, "software")
            ),
        )
        ejecutar_operacion(
            sistema,
            7,
            "Intentar crear un servicio con costo invalido",
            lambda: ServicioSala("S004", "Sala invalida", -100, capacidad=10),
        )

        reserva_valida = ejecutar_operacion(
            sistema,
            8,
            "Crear reserva valida",
            lambda: sistema.crear_reserva("C001", "S001", 2),
        )
        if reserva_valida is not None:
            ejecutar_operacion(
                sistema,
                9,
                "Confirmar reserva valida",
                lambda: sistema.confirmar_reserva(reserva_valida),
            )
            ejecutar_operacion(
                sistema,
                10,
                "Procesar reserva y calcular costo",
                lambda: sistema.procesar_reserva(reserva_valida),
            )

        ejecutar_operacion(
            sistema,
            11,
            "Intentar reservar con un cliente inexistente",
            lambda: sistema.crear_reserva("C999", "S001", 1),
        )
        ejecutar_operacion(
            sistema,
            12,
            "Intentar reservar con duracion cero",
            lambda: sistema.crear_reserva("C002", "S002", 0),
        )

        reserva_cancelable = ejecutar_operacion(
            sistema,
            13,
            "Crear una segunda reserva",
            lambda: sistema.crear_reserva("C002", "S003", 1),
        )
        if reserva_cancelable is not None:
            ejecutar_operacion(
                sistema,
                14,
                "Cancelar una reserva pendiente",
                lambda: sistema.cancelar_reserva(reserva_cancelable),
            )
            ejecutar_operacion(
                sistema,
                15,
                "Intentar procesar una reserva cancelada",
                lambda: sistema.procesar_reserva(reserva_cancelable),
            )

        print("\nSimulacion finalizada. Revisa el archivo log_eventos.txt.")
    except ErrorSistema as error:
        sistema.logger.registrar_error("Error no controlado durante la simulacion", error)
        print(f"Error general controlado: {error}")
    finally:
        sistema.cerrar()


if __name__ == "__main__":
    main()
