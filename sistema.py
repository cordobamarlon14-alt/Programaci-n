"""Control de listas, registro de eventos y busqueda de entidades."""

import logging
from pathlib import Path

from excepciones import ErrorDuplicado, ErrorNoEncontrado
from modelos import Reserva


class SistemaSoftwareFJ:
    """Administra los datos en memoria y registra eventos en un archivo."""

    def __init__(self, ruta_logs=None):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.logger = self._crear_logger(ruta_logs)

    @staticmethod
    def _crear_logger(ruta_logs):
        """Prepara el archivo de eventos sin requerir una base de datos."""
        ruta = Path(ruta_logs or Path(__file__).parent / "logs" / "software_fj.log")
        ruta.parent.mkdir(parents=True, exist_ok=True)
        logger = logging.getLogger(f"software_fj_{ruta.resolve()}")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            manejador = logging.FileHandler(ruta, encoding="utf-8")
            manejador.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
            logger.addHandler(manejador)
        return logger

    def _agregar_unico(self, lista, objeto, tipo):
        """Inserta un objeto si su identificador no esta registrado."""
        if any(actual.identificador == objeto.identificador for actual in lista):
            error = ErrorDuplicado(f"Ya existe {tipo} con ID {objeto.identificador}.")
            self.logger.error("Registro rechazado: %s", error)
            raise error
        lista.append(objeto)
        self.logger.info("%s registrado: %s", tipo, objeto.identificador)
        return objeto

    def registrar_cliente(self, cliente):
        return self._agregar_unico(self.clientes, cliente, "cliente")

    def registrar_servicio(self, servicio):
        return self._agregar_unico(self.servicios, servicio, "servicio")

    def _buscar(self, lista, identificador, tipo):
        """Busca un objeto por su identificador."""
        for objeto in lista:
            if objeto.identificador == str(identificador).strip():
                return objeto
        error = ErrorNoEncontrado(f"No se encontro {tipo} con ID {identificador}.")
        self.logger.error("Busqueda fallida: %s", error)
        raise error

    def buscar_cliente(self, identificador):
        return self._buscar(self.clientes, identificador, "cliente")

    def buscar_servicio(self, identificador):
        return self._buscar(self.servicios, identificador, "servicio")

    def buscar_reserva(self, identificador):
        return self._buscar(self.reservas, identificador, "reserva")

    def crear_reserva(
        self, identificador, id_cliente, id_servicio, duracion, descuento=0, impuesto=0
    ):
        """Crea una reserva tras comprobar que cliente y servicio existan."""
        if any(reserva.identificador == str(identificador).strip() for reserva in self.reservas):
            error = ErrorDuplicado(f"Ya existe una reserva con ID {identificador}.")
            self.logger.error("Reserva rechazada: %s", error)
            raise error
        cliente = self.buscar_cliente(id_cliente)
        servicio = self.buscar_servicio(id_servicio)
        reserva = Reserva(identificador, cliente, servicio, duracion, descuento, impuesto)
        self.reservas.append(reserva)
        self.logger.info("Reserva creada: %s para cliente %s", identificador, id_cliente)
        return reserva

    def registrar_error(self, contexto, error):
        """Registra excepciones capturadas por la interfaz o la demostracion."""
        self.logger.exception("%s: %s", contexto, error)

    def registrar_evento(self, mensaje):
        """Guarda una operacion importante en el registro."""
        self.logger.info("%s", mensaje)

