"""Ejecuto compras, persistencia y consultas concurrentes de demostración."""
from pathlib import Path
from queue import Queue
from threading import Thread
from tempfile import TemporaryDirectory
from modelos import Libro, LibroElectronico, LibroAudio, StockInsuficienteError
from archivos import (ArchivoLibros, ArchivoNoEncontradoError,
                      DatosCorruptosError, ArchivoInaccesibleError)


def describir_en_hilos(libros):
    resultados = Queue()

    def tarea(indice, libro):
        try:
            resultados.put((indice, libro.describir()))
        except Exception as error:
            resultados.put((indice, f"Error en consulta: {error}"))

    hilos = [Thread(target=tarea, args=(i, libro), name=f"consulta-{i}")
             for i, libro in enumerate(libros)]
    print("Hilos creados: todavía no iniciados.")
    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join()
    print(f"Hilos terminados: {all(not h.is_alive() for h in hilos)}")
    return [texto for _, texto in sorted(
        resultados.get() for _ in libros)]


def main():
    libros = [Libro("Python desde cero", "FIS-003", 2500),
              LibroElectronico("Bases de datos", "ELE-003", 1200),
              LibroAudio("Aprender escuchando", "AUD-001", 1800)]
    print("1. POLIMORFISMO Y COMPOSICIÓN")
    print(libros[0].reservar())
    for libro in libros:
        print(libro.describir())
        print(libro.comprar())
    print("2. EXCEPCIÓN DE DOMINIO")
    try:
        libros[0].comprar()
    except StockInsuficienteError as error:
        print(f"Compra rechazada: {error}")
    print("3. ARGUMENTOS POR DEFECTO")
    print(f"Una copia digital: {libros[1].calcular_total()} centavos")
    print(f"Tres copias digitales: {libros[1].calcular_total(3)} centavos")
    print("4. CONSULTAS CONCURRENTES")
    for resultado in describir_en_hilos(libros):
        print(resultado)
    print("5. GUARDADO Y RECONSTRUCCIÓN")
    with TemporaryDirectory() as carpeta:
        ruta = Path(carpeta) / "libro.json"
        repositorio = ArchivoLibros(ruta)
        try:
            repositorio.guardar(libros[0])
            print(ruta.read_text(encoding="utf-8"))
            recuperado = repositorio.leer()
            print(f"Recuperé: {recuperado.describir()}")
            print(f"Conservé vendido: {recuperado.vendido}")
            ruta.write_text("{JSON incompleto", encoding="utf-8")
            try:
                repositorio.leer()
            except DatosCorruptosError as error:
                print(f"Lectura rechazada: {error}")
            ruta.unlink()
            try:
                repositorio.leer()
            except ArchivoNoEncontradoError as error:
                print(f"Lectura rechazada: {error}")
        except ArchivoInaccesibleError as error:
            print(f"Error de almacenamiento: {error}")


if __name__ == "__main__":
    main()
