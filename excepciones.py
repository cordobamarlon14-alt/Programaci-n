"""Excepciones propias usadas por el sistema de Software FJ."""


class SoftwareFJError(Exception):
    """Excepcion base para errores controlados del dominio."""


class ErrorValidacion(SoftwareFJError):
    """Se lanza cuando un dato ingresado no cumple las reglas."""


class ErrorDuplicado(SoftwareFJError):
    """Se lanza cuando se intenta repetir un identificador."""


class ErrorNoEncontrado(SoftwareFJError):
    """Se lanza cuando no existe un cliente, servicio o reserva."""


class ErrorEstadoReserva(SoftwareFJError):
    """Se lanza cuando una reserva no permite la accion solicitada."""


class ErrorServicioNoDisponible(SoftwareFJError):
    """Se lanza cuando un servicio esta temporalmente deshabilitado."""

