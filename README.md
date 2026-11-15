# Software FJ - Gestión de clientes, servicios y reservas

Proyecto desarrollado de manera individual para Programación (213023), Fase 4. El sistema permite registrar clientes, administrar servicios y crear, confirmar, procesar o cancelar reservas. No utiliza base de datos: conserva los objetos en listas mientras la aplicación está abierta y escribe eventos y errores en `logs/software_fj.log`.

**Estudiante:** Marlon Brayan Gómez Córdoba  
**Modalidad de desarrollo:** Individual

## Requisitos

- Python 3.10 o superior.
- Tkinter (incluido normalmente en la instalacion de Python para Windows).

## Ejecutar la aplicación

Desde esta carpeta:

```powershell
python app.py
```

Registra primero al menos un cliente y un servicio. En la pestaña Reservas, usa sus identificadores para crear una reserva. Luego selecciona la reserva y confirma, procesa o cancela según corresponda.

## Ejecutar la demostracion de excepciones

```powershell
python demo.py
```

La demostración realiza 15 operaciones con entradas válidas e inválidas, muestra que los errores se controlan y guarda los detalles en el archivo de registro. Incluye ejemplos de `try/except`, `try/except/else`, `try/except/finally` y encadenamiento de excepciones.

## Estructura

- `app.py`: interfaz gráfica de escritorio.
- `modelos.py`: clase abstracta Entidad, Cliente, Servicio y sus tres servicios; tambien Reserva.
- `sistema.py`: listas internas, busquedas y archivo de registro.
- `excepciones.py`: excepciones propias del dominio.
- `demo.py`: operaciones de demostracion reproducibles.
- `logs/`: registro generado al ejecutar el proyecto.

## Decisiones de calculo

Las reservas de sala se cobran por hora, los equipos por día y las asesorías por hora. Cada servicio aplica descuento e impuesto opcionales. El método `calcular_costo(duracion, descuento=0, impuesto=0)` permite llamarse con solo la duración, con duración y descuento, o con los tres valores; en Python esta técnica usa parámetros opcionales para simular la sobrecarga.

## Desarrollo

El código de este repositorio fue preparado y revisado por el estudiante indicado en la portada del informe. La actividad se planteó con orientación colaborativa; la modalidad individual debe confirmarse con el tutor antes de la entrega.

