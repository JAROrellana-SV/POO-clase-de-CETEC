# Actividad 3 - Aplicación integradora de libros

Retomé mi proyecto de libros físicos y electrónicos y agregué audiolibros,
estrategias de entrega, entrada/salida JSON, manejo de excepciones e hilos.

## Ejecución

Probé el proyecto con Python 3.12.14. No requiere paquetes externos.
Descomprimo esta carpeta y abro una terminal en ella:

```bash
python app.py
python -m unittest test_app -v
python problema_herencia.py
```

Si mi equipo usa `python3`, sustituyo `python` por `python3`.

## Archivos

- `modelos.py`: libros, interfaz Entrega y estrategias física y digital.
- `archivos.py`: guardado y reconstrucción de libros desde JSON.
- `app.py`: demostración de consola con manejo de errores e hilos.
- `test_app.py`: seis pruebas de las reglas del proyecto.
- `problema_herencia.py`: ejemplo deliberadamente incorrecto, separado.

## Preparación del ambiente

```bash
python -m venv .venv
```

En macOS/Linux activo con `source .venv/bin/activate`.
En Windows PowerShell activo con `.venv\Scripts\Activate.ps1`.

## Alcance

La demostración utiliza una carpeta temporal para no cambiar archivos personales.
Guarda un libro, lo reconstruye y simula errores de lectura; al terminar elimina
los datos de esa demostración. Para conservar un archivo puedo usar
`ArchivoLibros("libro.json")` desde mi código, fuera de TemporaryDirectory.

La persistencia reconstruye las tres clases con sus entregas predeterminadas.
Para conservar una estrategia personalizada tendría que registrarla también
en el formato JSON. Un mismo ArchivoLibros no coordina escrituras simultáneas;
por eso la demostración escribe desde el hilo principal. El bloqueo de cada
Libro protege las ventas concurrentes de esa misma instancia.

No proceso pagos reales ni implemento un sistema de usuarios o reservas por cliente.
El total en centavos es una cotización; calcularlo no vende unidades.

## Autor

Jesús Alfredo Rosales Orellana.
Programación Orientada a Objetos, CETEC.
Docente: Ing. Jessica de Aguilar.

Repositorio de las actividades anteriores:
https://github.com/JAROrellana-SV/POO-clase-de-CETEC
