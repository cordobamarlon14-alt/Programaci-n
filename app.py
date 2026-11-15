"""Interfaz de escritorio para administrar clientes, servicios y reservas."""

import tkinter as tk
from tkinter import messagebox, ttk

from excepciones import ErrorValidacion, SoftwareFJError
from modelos import AlquilerEquipo, AsesoriaEspecializada, Cliente, ReservaSala
from sistema import SistemaSoftwareFJ


class AplicacionSoftwareFJ:
    """Ventana principal de la aplicacion de gestion."""

    def __init__(self, ventana):
        self.ventana = ventana
        self.sistema = SistemaSoftwareFJ()
        self.reserva_seleccionada = None
        self.ventana.title("Software FJ | Clientes, servicios y reservas")
        self.ventana.geometry("1050x720")
        self.ventana.minsize(900, 620)
        self._construir_interfaz()
        self._actualizar_listas()

    def _construir_interfaz(self):
        """Crea pestanas para catalogos, reservas y mensajes."""
        ttk.Label(
            self.ventana,
            text="Software FJ - Gestion de clientes, servicios y reservas",
            font=("Arial", 16, "bold"),
        ).pack(pady=12)

        self.pestanas = ttk.Notebook(self.ventana)
        self.pestanas.pack(fill="both", expand=True, padx=14, pady=8)
        self.pestana_clientes = ttk.Frame(self.pestanas, padding=12)
        self.pestana_servicios = ttk.Frame(self.pestanas, padding=12)
        self.pestana_reservas = ttk.Frame(self.pestanas, padding=12)
        self.pestanas.add(self.pestana_clientes, text="Clientes")
        self.pestanas.add(self.pestana_servicios, text="Servicios")
        self.pestanas.add(self.pestana_reservas, text="Reservas")

        self._construir_pestana_clientes()
        self._construir_pestana_servicios()
        self._construir_pestana_reservas()

        self.mensaje_estado = tk.StringVar(value="Listo para trabajar.")
        ttk.Label(self.ventana, textvariable=self.mensaje_estado, anchor="w").pack(
            fill="x", padx=16, pady=(0, 12)
        )

    def _crear_entrada(self, contenedor, fila, etiqueta):
        """Agrega una etiqueta y un campo de texto en la fila indicada."""
        ttk.Label(contenedor, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=5)
        entrada = ttk.Entry(contenedor, width=34)
        entrada.grid(row=fila, column=1, sticky="ew", pady=5, padx=(8, 0))
        return entrada

    def _construir_pestana_clientes(self):
        marco = ttk.LabelFrame(self.pestana_clientes, text="Registrar cliente", padding=12)
        marco.pack(fill="x", pady=(0, 12))
        marco.columnconfigure(1, weight=1)
        self.cliente_id = self._crear_entrada(marco, 0, "Identificacion:")
        self.cliente_nombre = self._crear_entrada(marco, 1, "Nombre completo:")
        self.cliente_correo = self._crear_entrada(marco, 2, "Correo electronico:")
        self.cliente_telefono = self._crear_entrada(marco, 3, "Telefono:")
        ttk.Button(marco, text="Guardar cliente", command=self._registrar_cliente).grid(
            row=4, column=1, sticky="e", pady=(8, 0)
        )
        self.lista_clientes = self._crear_lista(self.pestana_clientes, "Clientes registrados")

    def _construir_pestana_servicios(self):
        marco = ttk.LabelFrame(self.pestana_servicios, text="Registrar servicio", padding=12)
        marco.pack(fill="x", pady=(0, 12))
        marco.columnconfigure(1, weight=1)
        self.servicio_id = self._crear_entrada(marco, 0, "Codigo:")
        self.servicio_nombre = self._crear_entrada(marco, 1, "Nombre:")
        ttk.Label(marco, text="Tipo de servicio:").grid(row=2, column=0, sticky="w", pady=5)
        self.servicio_tipo = ttk.Combobox(
            marco,
            values=("Reserva de sala", "Alquiler de equipo", "Asesoria especializada"),
            state="readonly",
            width=31,
        )
        self.servicio_tipo.current(0)
        self.servicio_tipo.grid(row=2, column=1, sticky="ew", pady=5, padx=(8, 0))
        self.servicio_tarifa = self._crear_entrada(marco, 3, "Tarifa:")
        ttk.Button(marco, text="Guardar servicio", command=self._registrar_servicio).grid(
            row=4, column=1, sticky="e", pady=(8, 0)
        )
        self.lista_servicios = self._crear_lista(self.pestana_servicios, "Servicios registrados")

    def _construir_pestana_reservas(self):
        marco = ttk.LabelFrame(self.pestana_reservas, text="Crear reserva", padding=12)
        marco.pack(fill="x", pady=(0, 12))
        marco.columnconfigure(1, weight=1)
        self.reserva_id = self._crear_entrada(marco, 0, "Codigo de reserva:")
        self.reserva_cliente = self._crear_entrada(marco, 1, "Identificacion del cliente:")
        self.reserva_servicio = self._crear_entrada(marco, 2, "Codigo del servicio:")
        self.reserva_duracion = self._crear_entrada(marco, 3, "Duracion (horas o dias):")
        self.reserva_descuento = self._crear_entrada(marco, 4, "Descuento (%) opcional:")
        self.reserva_descuento.insert(0, "0")
        self.reserva_impuesto = self._crear_entrada(marco, 5, "Impuesto (%) opcional:")
        self.reserva_impuesto.insert(0, "0")
        ttk.Button(marco, text="Crear reserva", command=self._crear_reserva).grid(
            row=6, column=1, sticky="e", pady=(8, 0)
        )

        botones = ttk.Frame(self.pestana_reservas)
        botones.pack(fill="x", pady=(0, 8))
        ttk.Button(botones, text="Confirmar seleccionada", command=self._confirmar_reserva).pack(side="left", padx=(0, 6))
        ttk.Button(botones, text="Procesar seleccionada", command=self._procesar_reserva).pack(side="left", padx=6)
        ttk.Button(botones, text="Cancelar seleccionada", command=self._cancelar_reserva).pack(side="left", padx=6)

        columnas = ("id", "cliente", "servicio", "duracion", "estado", "costo")
        self.tabla_reservas = ttk.Treeview(
            self.pestana_reservas, columns=columnas, show="headings", height=12
        )
        encabezados = {
            "id": "Reserva",
            "cliente": "Cliente",
            "servicio": "Servicio",
            "duracion": "Duracion",
            "estado": "Estado",
            "costo": "Costo",
        }
        anchos = {"id": 100, "cliente": 170, "servicio": 190, "duracion": 100, "estado": 110, "costo": 120}
        for columna in columnas:
            self.tabla_reservas.heading(columna, text=encabezados[columna])
            self.tabla_reservas.column(columna, width=anchos[columna], anchor="center")
        self.tabla_reservas.pack(fill="both", expand=True)

    @staticmethod
    def _crear_lista(contenedor, titulo):
        """Crea una lista desplazable para mostrar objetos registrados."""
        marco = ttk.LabelFrame(contenedor, text=titulo, padding=8)
        marco.pack(fill="both", expand=True)
        lista = tk.Listbox(marco, height=15)
        barra = ttk.Scrollbar(marco, orient="vertical", command=lista.yview)
        lista.configure(yscrollcommand=barra.set)
        lista.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return lista

    @staticmethod
    def _numero(entrada, nombre):
        """Convierte una entrada numerica y conserva la causa original."""
        try:
            return float(entrada.get().strip())
        except ValueError as error:
            raise ErrorValidacion(f"{nombre} debe ser un numero valido.") from error

    def _ejecutar(self, descripcion, accion):
        """Captura errores de interfaz, los registra y mantiene la ventana activa."""
        try:
            resultado = accion()
        except SoftwareFJError as error:
            self.sistema.registrar_error(descripcion, error)
            messagebox.showerror("No se pudo completar", str(error))
            self.mensaje_estado.set("La operacion no se completo. Puedes corregir los datos e intentarlo de nuevo.")
        except Exception as error:
            self.sistema.registrar_error(f"Error inesperado: {descripcion}", error)
            messagebox.showerror("Error inesperado", "Ocurrio un problema. El detalle quedo guardado en el archivo de registro.")
            self.mensaje_estado.set("Se registro un error inesperado y la aplicacion continua activa.")
        else:
            self.sistema.registrar_evento(f"Operacion completada: {descripcion}")
            self.mensaje_estado.set(str(resultado or "Operacion completada."))
            self._actualizar_listas()
        finally:
            self.ventana.update_idletasks()

    def _registrar_cliente(self):
        def accion():
            cliente = Cliente(
                self.cliente_id.get(),
                self.cliente_nombre.get(),
                self.cliente_correo.get(),
                self.cliente_telefono.get(),
            )
            self.sistema.registrar_cliente(cliente)
            return f"Cliente {cliente.nombre} registrado."

        self._ejecutar("Registro de cliente", accion)

    def _registrar_servicio(self):
        def accion():
            tarifa = self._numero(self.servicio_tarifa, "La tarifa")
            tipo = self.servicio_tipo.get()
            clases = {
                "Reserva de sala": ReservaSala,
                "Alquiler de equipo": AlquilerEquipo,
                "Asesoria especializada": AsesoriaEspecializada,
            }
            servicio = clases[tipo](self.servicio_id.get(), self.servicio_nombre.get(), tarifa)
            self.sistema.registrar_servicio(servicio)
            return f"Servicio '{servicio.nombre}' registrado."

        self._ejecutar("Registro de servicio", accion)

    def _crear_reserva(self):
        def accion():
            descuento = self._numero(self.reserva_descuento, "El descuento")
            impuesto = self._numero(self.reserva_impuesto, "El impuesto")
            reserva = self.sistema.crear_reserva(
                self.reserva_id.get(),
                self.reserva_cliente.get(),
                self.reserva_servicio.get(),
                self._numero(self.reserva_duracion, "La duracion"),
                descuento,
                impuesto,
            )
            return f"Reserva {reserva.identificador} creada en estado pendiente."

        self._ejecutar("Creacion de reserva", accion)

    def _id_reserva_actual(self):
        seleccion = self.tabla_reservas.selection()
        if not seleccion:
            raise ErrorValidacion("Selecciona una reserva de la tabla.")
        return self.tabla_reservas.item(seleccion[0], "values")[0]

    def _confirmar_reserva(self):
        def accion():
            reserva = self.sistema.buscar_reserva(self._id_reserva_actual())
            reserva.confirmar()
            return f"Reserva {reserva.identificador} confirmada."

        self._ejecutar("Confirmacion de reserva", accion)

    def _procesar_reserva(self):
        def accion():
            reserva = self.sistema.buscar_reserva(self._id_reserva_actual())
            costo = reserva.procesar()
            return f"Reserva {reserva.identificador} procesada. Total: ${costo:.2f}."

        self._ejecutar("Procesamiento de reserva", accion)

    def _cancelar_reserva(self):
        def accion():
            reserva = self.sistema.buscar_reserva(self._id_reserva_actual())
            reserva.cancelar()
            return f"Reserva {reserva.identificador} cancelada."

        self._ejecutar("Cancelacion de reserva", accion)

    def _actualizar_listas(self):
        """Refresca las vistas con el estado actual de los objetos en memoria."""
        self.lista_clientes.delete(0, tk.END)
        for cliente in self.sistema.clientes:
            self.lista_clientes.insert(tk.END, str(cliente))

        self.lista_servicios.delete(0, tk.END)
        for servicio in self.sistema.servicios:
            self.lista_servicios.insert(tk.END, str(servicio))

        for fila in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(fila)
        for reserva in self.sistema.reservas:
            costo = "-" if reserva.costo is None else f"${reserva.costo:.2f}"
            self.tabla_reservas.insert(
                "",
                tk.END,
                values=(
                    reserva.identificador,
                    reserva.cliente.nombre,
                    reserva.servicio.nombre,
                    reserva.duracion,
                    reserva.estado,
                    costo,
                ),
            )


if __name__ == "__main__":
    raiz = tk.Tk()
    AplicacionSoftwareFJ(raiz)
    raiz.mainloop()

