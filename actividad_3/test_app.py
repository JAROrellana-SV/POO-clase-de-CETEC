"""Compruebo invariantes de compras, reconstrucción y concurrencia."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
from queue import Queue
from modelos import Libro, LibroAudio, StockInsuficienteError, Entrega
from archivos import (ArchivoLibros, DatosCorruptosError,
                      ArchivoNoEncontradoError, ArchivoInaccesibleError)


class PruebasAplicacion(unittest.TestCase):
    def test_venta_concurrente_unica(self):
        libro, resultados = Libro("Python", "F-1", 100), Queue()

        def comprar():
            try:
                libro.comprar()
                resultados.put("venta")
            except StockInsuficienteError:
                resultados.put("rechazo")

        hilos = [Thread(target=comprar) for _ in range(2)]
        for hilo in hilos:
            hilo.start()
        for hilo in hilos:
            hilo.join()
        self.assertCountEqual([resultados.get(), resultados.get()],
                              ["venta", "rechazo"])

    def test_recupero_subclase_y_estado(self):
        with TemporaryDirectory() as carpeta:
            repositorio = ArchivoLibros(Path(carpeta) / "libro.json")
            audio = LibroAudio("Audio", "A-1", 300)
            repositorio.guardar(audio)
            recuperado = repositorio.leer()
            self.assertIsInstance(recuperado, LibroAudio)
            self.assertEqual(recuperado.to_dict(), audio.to_dict())
            fisico = Libro("Python", "F-1", 100)
            fisico.comprar()
            repositorio.guardar(fisico)
            with self.assertRaises(StockInsuficienteError):
                repositorio.leer().comprar()

    def test_json_invalido_y_archivo_ausente(self):
        with TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "libro.json"
            repositorio = ArchivoLibros(ruta)
            with self.assertRaises(ArchivoNoEncontradoError):
                repositorio.leer()
            for texto in ("{incompleto", "[]", '{"tipo":"desconocido"}'):
                ruta.write_text(texto, encoding="utf-8")
                with self.assertRaises(DatosCorruptosError):
                    repositorio.leer()

    def test_interfaz_y_argumentos(self):
        with self.assertRaises(TypeError):
            Entrega()
        with self.assertRaises(ValueError):
            Libro("Python", "F-1", -1)
        audio = LibroAudio("Audio", "A-1", 300)
        self.assertEqual(audio.calcular_total(), 300)
        self.assertEqual(audio.calcular_total(2), 600)
        self.assertEqual(audio.comprar(), audio.comprar())

    def test_reserva_y_estrategia_intercambiable(self):
        class Retiro(Entrega):
            limitada = True

            def entregar(self, titulo):
                return f"Retirar {titulo} en tienda."

        libro = Libro("Python", "F-1", 100, entrega=Retiro())
        libro.reservar()
        self.assertTrue(libro.to_dict()["reservado"])
        self.assertEqual(libro.comprar(), "Retirar Python en tienda.")
        self.assertFalse(libro.to_dict()["reservado"])

    def test_comunico_fallo_de_escritura(self):
        with TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "carpeta_ausente" / "libro.json"
            with self.assertRaises(ArchivoInaccesibleError):
                ArchivoLibros(ruta).guardar(Libro("Python", "F-1", 100))


if __name__ == "__main__":
    unittest.main(verbosity=2)
