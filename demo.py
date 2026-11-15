"""Demostracion reproducible con operaciones correctas e incorrectas."""

from excepciones import SoftwareFJError
from modelos import AlquilerEquipo, AsesoriaEspecializada, Cliente, ReservaSala
from sistema import SistemaSoftwareFJ


def intentar(sistema, descripcion, operacion):
    """Ejecuta una operacion, captura errores y deja trazabilidad."""
    print(f"\n{descripcion}")
    try:
        resultado = operacion()
    except SoftwareFJError as error:
        sistema.registrar_error(descripcion, error)
        print(f"  Error controlado: {error}")
    else:
        print(f"  Resultado: {resultado}")
    finally:
        print("  Operacion finalizada; el sistema continua activo.")


def ejecutar_demo():
    """Realiza mas de diez operaciones solicitadas en el anexo."""
    sistema = SistemaSoftwareFJ()

    # Operacion 1: registrar un cliente valido.
    intentar(
        sistema,
        "1. Registro de cliente valido",
        lambda: sistema.registrar_cliente(
            Cliente("C001", "Ana Torres", "ana@example.com", "3001234567")
        ),
    )

    # Operacion 2: rechazar un correo invalido.
    intentar(
        sistema,
        "2. Registro de cliente con correo invalido",
        lambda: Cliente("C002", "Luis Perez", "correo-mal", "3101234567"),
    )

    # Operacion 3: rechazar un telefono demasiado corto.
    intentar(
        sistema,
        "3. Registro de cliente con telefono invalido",
        lambda: Cliente("C003", "Rosa Diaz", "rosa@example.com", "123"),
    )

    # Operacion 4: detectar un ID de cliente repetido.
    intentar(
        sistema,
        "4. Registro duplicado de cliente",
        lambda: sistema.registrar_cliente(
            Cliente("C001", "Ana Torres", "ana@example.com", "3001234567")
        ),
    )

    # Operaciones 5 a 7: registrar tres servicios polimorficos.
    intentar(
        sistema,
        "5. Creacion de servicio de sala",
        lambda: sistema.registrar_servicio(ReservaSala("S001", "Sala Norte", 50000)),
    )
    intentar(
        sistema,
        "6. Creacion de servicio de alquiler de equipo",
        lambda: sistema.registrar_servicio(AlquilerEquipo("S002", "Proyector HD", 80000)),
    )
    intentar(
        sistema,
        "7. Creacion de servicio de asesoria",
        lambda: sistema.registrar_servicio(
            AsesoriaEspecializada("S003", "Asesoria Python", 65000)
        ),
    )

    # Operacion 8: rechazar una tarifa de servicio invalida.
    intentar(
        sistema,
        "8. Creacion de servicio con tarifa cero",
        lambda: ReservaSala("S004", "Sala sin tarifa", 0),
    )

    # Operacion 9: rechazar una reserva cuyo cliente no esta registrado.
    intentar(
        sistema,
        "9. Reserva con cliente inexistente",
        lambda: sistema.crear_reserva("R001", "C999", "S001", 2),
    )

    # Operacion 10: rechazar una duracion de sala fuera del rango.
    intentar(
        sistema,
        "10. Reserva de sala con duracion no permitida",
        lambda: sistema.crear_reserva("R002", "C001", "S001", 20),
    )

    # Operacion 11: crear, confirmar y procesar una reserva correcta.
    def procesar_sala():
        reserva = sistema.crear_reserva("R003", "C001", "S001", 2, 10, 19)
        reserva.confirmar()
        costo = reserva.procesar()
        sistema.registrar_evento(f"Reserva {reserva.identificador} procesada por ${costo:.2f}")
        return f"{reserva}; total ${costo:.2f}"

    intentar(sistema, "11. Reserva exitosa de sala", procesar_sala)

    # Operacion 12: calcular alquiler de equipo usando dos argumentos opcionales.
    def procesar_equipo():
        reserva = sistema.crear_reserva("R004", "C001", "S002", 3, 5)
        reserva.confirmar()
        return f"Costo con descuento: ${reserva.procesar():.2f}"

    intentar(sistema, "12. Reserva exitosa de equipo", procesar_equipo)

    # Operacion 13: impedir procesar una reserva que no esta confirmada.
    intentar(
        sistema,
        "13. Intento de procesar reserva pendiente",
        lambda: sistema.crear_reserva("R005", "C001", "S003", 1).procesar(),
    )

    # Operacion 14: suspender un servicio e impedir una nueva reserva.
    def reservar_servicio_suspendido():
        servicio = sistema.buscar_servicio("S003")
        servicio.cambiar_disponibilidad(False)
        reserva = sistema.crear_reserva("R006", "C001", "S003", 1)
        reserva.confirmar()
        return reserva

    intentar(sistema, "14. Reserva de servicio no disponible", reservar_servicio_suspendido)

    # Operacion 15: demostrar encadenamiento de excepciones al convertir datos.
    def conversion_encadenada():
        try:
            float("dos horas")
        except ValueError as error:
            raise SoftwareFJError("No fue posible convertir la duracion ingresada.") from error

    intentar(sistema, "15. Error de conversion con excepcion encadenada", conversion_encadenada)

    print("\nResumen: se ejecutaron 15 operaciones y el programa completo la demostracion.")
    print("Los eventos y errores quedaron registrados en logs/software_fj.log.")
    print(f"Clientes: {len(sistema.clientes)} | Servicios: {len(sistema.servicios)} | Reservas: {len(sistema.reservas)}")


if __name__ == "__main__":
    ejecutar_demo()

