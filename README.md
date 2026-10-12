# POO clase de CETEC

Comparto mi trabajo de Programación Orientada a Objetos en CETEC.

## Actividad 2: Los pilares de la POO y buenas prácticas de desarrollo

Retomé mi proyecto de venta de libros físicos y electrónicos. Representé una
unidad física con la clase `Libro` y un producto digital con `LibroElectronico`.

En el código apliqué:

- Abstracción mediante la clase abstracta `Producto`.
- Encapsulamiento del código y del precio del libro.
- Herencia con `LibroElectronico` y el uso de `super()`.
- Polimorfismo mediante diferentes implementaciones de `comprar()`.
- Agrupación de objetos mediante `Catalogo`.
- Simulación de sobrecarga con `calcular_total(cantidad=1)`.
- Validaciones para evitar precios negativos y códigos repetidos.

## Archivos

- `proyecto.py`: clases y ejemplo de ejecución.
- `test_proyecto.py`: cinco pruebas de las reglas del proyecto.

## Ejecución

Comprobé el proyecto con Python 3.12.14. Utilicé la biblioteca estándar,
por lo que no necesité instalar dependencias externas.

En una terminal, desde la carpeta donde guardé los archivos, puedo ejecutar:

```bash
python proyecto.py
python -m unittest test_proyecto -v
```

Si mi equipo utiliza el comando `python3`, puedo sustituir `python` por `python3`.

## Alcance

Simulé reservas y compras. No procesé pagos reales ni almacené ventas en una
base de datos. La unidad física cambia a agotada después de comprarla; el
producto electrónico permanece disponible.

## Autor

Jesús Alfredo Rosales Orellana.

Materia: Programación Orientada a Objetos.

Docente: Ing. Jessica de Aguilar.
