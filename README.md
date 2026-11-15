# Software FJ - Gestion de clientes, servicios y reservas

Proyecto colaborativo de Programacion (213023), Fase 4. El sistema permite registrar clientes, administrar servicios y crear, confirmar, procesar o cancelar reservas. No utiliza base de datos: conserva los objetos en listas durante la ejecucion y escribe eventos y errores en `logs/software_fj.log`.

## Requisitos

- Python 3.10 o superior.
- Tkinter (incluido normalmente en la instalacion de Python para Windows).

## Ejecutar la aplicacion

Desde esta carpeta:

```powershell
python app.py
```

Registra primero al menos un cliente y un servicio. En la pestana Reservas, usa sus identificadores para crear una reserva. Luego selecciona la reserva y confirma, procesa o cancela segun corresponda.

## Ejecutar la demostracion de excepciones

```powershell
python demo.py
```

La demostracion realiza 15 operaciones con entradas validas e invalidas, muestra que los errores se controlan y guarda los detalles en el archivo de registro. Incluye ejemplos de `try/except`, `try/except/else`, `try/except/finally` y encadenamiento de excepciones.

## Estructura

- `app.py`: interfaz grafica de escritorio.
- `modelos.py`: clase abstracta Entidad, Cliente, Servicio y sus tres servicios; tambien Reserva.
- `sistema.py`: listas internas, busquedas y archivo de registro.
- `excepciones.py`: excepciones propias del dominio.
- `demo.py`: operaciones de demostracion reproducibles.
- `logs/`: registro generado al ejecutar el proyecto.

## Decisiones de calculo

Las reservas de sala se cobran por hora, los equipos por dia y las asesorias por hora. Cada servicio aplica descuento e impuesto opcionales. El metodo `calcular_costo(duracion, descuento=0, impuesto=0)` permite llamarse con solo la duracion, con duracion y descuento, o con los tres valores; en Python esta tecnica usa parametros opcionales para simular la sobrecarga.
