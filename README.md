# Software FJ - gestion de clientes, servicios y reservas

Proyecto educativo en Python que aplica abstraccion, herencia, encapsulacion,
polimorfismo y manejo de excepciones. Los datos se guardan en listas durante
la ejecucion; el archivo `log_eventos.txt` se usa unicamente para eventos y
errores.

## Archivos

- `excepciones.py`: excepciones personalizadas.
- `logger.py`: registro de eventos y errores.
- `entidad.py`, `cliente.py`: entidad abstracta y clientes.
- `servicio.py`: servicio abstracto y servicios de sala, equipo y asesoria.
- `reserva.py`: reserva y transiciones de estado.
- `sistema.py`: listas y operaciones principales.
- `main.py`: simulacion de mas de diez operaciones, incluyendo casos fallidos.
- `test_sistema.py`: pruebas automatizadas.

## Ejecutar

Desde la carpeta que contiene `software_fj`, ejecuta:

```text
python -m software_fj.main
```

Para correr las pruebas:

```text
python -m unittest software_fj.test_sistema -v
```

El proyecto solo utiliza la biblioteca estandar de Python. El costo acepta
distintas llamadas con descuento e impuesto opcionales; Python no implementa
sobrecarga tradicional por firma, por lo que estos parametros opcionales
representan las variantes de calculo solicitadas.
