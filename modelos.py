"""Modelos del sistema: clientes, servicios y reservas."""

from abc import ABC, abstractmethod
from datetime import datetime
import re

from excepciones import ErrorEstadoReserva, ErrorServicioNoDisponible, ErrorValidacion


class Entidad(ABC):
    """Clase abstracta que proporciona un identificador comun."""

    def __init__(self, identificador):
        self._identificador = self._validar_texto(identificador, "El identificador")

    @staticmethod
    def _validar_texto(valor, campo):
        """Limpia textos y evita aceptar cadenas vacias."""
        if not isinstance(valor, str) or not valor.strip():
            raise ErrorValidacion(f"{campo} es obligatorio.")
        return valor.strip()

    @property
    def identificador(self):
        """Expone el identificador sin permitir cambiarlo directamente."""
        return self._identificador

    @abstractmethod
    def validar(self):
        """Obliga a cada entidad concreta a validar sus datos."""


class Cliente(Entidad):
    """Cliente con datos personales encapsulados."""

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self.__nombre = self._validar_texto(nombre, "El nombre")
        self.__correo = self._validar_texto(correo, "El correo").lower()
        self.__telefono = self._validar_texto(telefono, "El telefono")
        self.validar()

    def validar(self):
        """Verifica el formato basico del correo y el telefono."""
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", self.__correo):
            raise ErrorValidacion("El correo no tiene un formato valido.")
        digitos = re.sub(r"\D", "", self.__telefono)
        if len(digitos) < 7 or len(digitos) > 15:
            raise ErrorValidacion("El telefono debe contener entre 7 y 15 digitos.")

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def __str__(self):
        return f"{self.identificador} - {self.nombre} ({self.correo})"


class Servicio(Entidad, ABC):
    """Servicio abstracto con precio base y calculo con opciones."""

    def __init__(self, identificador, nombre, tarifa):
        super().__init__(identificador)
        self._nombre = self._validar_texto(nombre, "El nombre del servicio")
        self._tarifa = self._validar_tarifa(tarifa)
        self._disponible = True

    @staticmethod
    def _validar_tarifa(tarifa):
        """Asegura que la tarifa sea un numero positivo."""
        try:
            tarifa = float(tarifa)
        except (TypeError, ValueError) as error:
            raise ErrorValidacion("La tarifa debe ser numerica.") from error
        if tarifa <= 0:
            raise ErrorValidacion("La tarifa debe ser mayor que cero.")
        return tarifa

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa(self):
        return self._tarifa

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, disponible):
        """Permite habilitar o suspender temporalmente el servicio."""
        self._disponible = bool(disponible)

    def validar(self):
        """Verifica que el servicio pueda reservarse."""
        if not self._disponible:
            raise ErrorServicioNoDisponible(
                f"El servicio '{self.nombre}' no esta disponible actualmente."
            )

    def _validar_cargos(self, descuento, impuesto):
        """Valida porcentajes comunes antes de calcular el costo final."""
        for nombre, valor in (("descuento", descuento), ("impuesto", impuesto)):
            try:
                porcentaje = float(valor)
            except (TypeError, ValueError) as error:
                raise ErrorValidacion(f"El {nombre} debe ser numerico.") from error
            if porcentaje < 0 or porcentaje > 100:
                raise ErrorValidacion(f"El {nombre} debe estar entre 0 y 100.")
        return float(descuento), float(impuesto)

    def _calcular_total(self, subtotal, descuento=0, impuesto=0):
        """Aplica descuento e impuesto al subtotal de cualquier servicio."""
        descuento, impuesto = self._validar_cargos(descuento, impuesto)
        subtotal_con_descuento = subtotal * (1 - descuento / 100)
        return round(subtotal_con_descuento * (1 + impuesto / 100), 2)

    @abstractmethod
    def validar_duracion(self, duracion):
        """Valida la duracion segun la unidad propia del servicio."""

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        """Calcula el costo; los argumentos opcionales simulan sobrecarga."""

    @abstractmethod
    def describir(self):
        """Retorna una descripcion especifica para cada servicio."""

    def __str__(self):
        disponibilidad = "Disponible" if self.disponible else "No disponible"
        return f"{self.identificador} - {self.describir()} - {disponibilidad}"


class ReservaSala(Servicio):
    """Reserva de sala cobrada por hora."""

    def validar_duracion(self, duracion):
        try:
            horas = float(duracion)
        except (TypeError, ValueError) as error:
            raise ErrorValidacion("Las horas de sala deben ser numericas.") from error
        if horas < 1 or horas > 12:
            raise ErrorValidacion("La sala se puede reservar entre 1 y 12 horas.")
        return horas

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar()
        horas = self.validar_duracion(duracion)
        return self._calcular_total(self.tarifa * horas, descuento, impuesto)

    def describir(self):
        return f"Reserva de sala: {self.nombre}, ${self.tarifa:.2f} por hora"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos cobrado por dia."""

    def validar_duracion(self, duracion):
        try:
            valor_dias = float(duracion)
        except (TypeError, ValueError) as error:
            raise ErrorValidacion("Los dias de alquiler deben ser un numero entero.") from error
        if not valor_dias.is_integer():
            raise ErrorValidacion("Los dias de alquiler deben ser un numero entero.")
        dias = int(valor_dias)
        if dias < 1 or dias > 30:
            raise ErrorValidacion("El alquiler debe durar entre 1 y 30 dias.")
        return dias

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar()
        dias = self.validar_duracion(duracion)
        return self._calcular_total(self.tarifa * dias, descuento, impuesto)

    def describir(self):
        return f"Alquiler de equipo: {self.nombre}, ${self.tarifa:.2f} por dia"


class AsesoriaEspecializada(Servicio):
    """Asesoria profesional cobrada por hora."""

    def validar_duracion(self, duracion):
        try:
            horas = float(duracion)
        except (TypeError, ValueError) as error:
            raise ErrorValidacion("Las horas de asesoria deben ser numericas.") from error
        if horas <= 0 or horas > 8:
            raise ErrorValidacion("La asesoria debe durar mas de 0 y hasta 8 horas.")
        return horas

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar()
        horas = self.validar_duracion(duracion)
        return self._calcular_total(self.tarifa * horas, descuento, impuesto)

    def describir(self):
        return f"Asesoria especializada: {self.nombre}, ${self.tarifa:.2f} por hora"


class Reserva:
    """Relaciona cliente, servicio y duracion con un estado controlado."""

    ESTADOS = ("Pendiente", "Confirmada", "Procesada", "Cancelada")

    def __init__(self, identificador, cliente, servicio, duracion, descuento=0, impuesto=0):
        self.__identificador = Entidad._validar_texto(identificador, "El identificador de reserva")
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = servicio.validar_duracion(duracion)
        self.__descuento, self.__impuesto = servicio._validar_cargos(descuento, impuesto)
        self.__estado = "Pendiente"
        self.__creada_en = datetime.now()
        self.__costo = None

    @property
    def identificador(self):
        return self.__identificador

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    def confirmar(self):
        """Confirma solamente reservas que siguen pendientes."""
        if self.__estado != "Pendiente":
            raise ErrorEstadoReserva("Solo se puede confirmar una reserva pendiente.")
        self.__servicio.validar()
        self.__estado = "Confirmada"

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada."""
        if self.__estado not in ("Pendiente", "Confirmada"):
            raise ErrorEstadoReserva("La reserva ya no se puede cancelar.")
        self.__estado = "Cancelada"

    def procesar(self):
        """Calcula y guarda el costo de una reserva confirmada."""
        if self.__estado != "Confirmada":
            raise ErrorEstadoReserva("La reserva debe estar confirmada antes de procesarla.")
        self.__costo = self.__servicio.calcular_costo(
            self.__duracion, self.__descuento, self.__impuesto
        )
        self.__estado = "Procesada"
        return self.__costo

    def __str__(self):
        costo = "Pendiente de calculo" if self.costo is None else f"${self.costo:.2f}"
        return (
            f"{self.identificador} | {self.cliente.nombre} | {self.servicio.nombre} | "
            f"{self.duracion} | {self.estado} | {costo}"
        )

