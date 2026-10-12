import unittest
from proyecto import CompraNoDisponible, Libro, LibroElectronico, Catalogo


class PruebasLibros(unittest.TestCase):
    def test_no_vendo_dos_veces_la_unidad(self):
        libro = Libro("Python", "F-1", 2500)
        libro.comprar()
        with self.assertRaises(CompraNoDisponible):
            libro.comprar()

    def test_puedo_repetir_la_compra_digital(self):
        libro = LibroElectronico("Python", "E-1", 1200)
        self.assertEqual(libro.comprar(), libro.comprar())
        self.assertEqual(libro.estado, "a la venta")

    def test_rechazo_precio_negativo(self):
        with self.assertRaises(ValueError):
            Libro("Python", "F-1", -100)

    def test_total_con_y_sin_argumento(self):
        libro = LibroElectronico("Python", "E-1", 1200)
        self.assertEqual(libro.calcular_total(), 1200)
        self.assertEqual(libro.calcular_total(3), 3600)

    def test_rechazo_codigos_repetidos(self):
        catalogo = Catalogo("Prueba")
        catalogo.agregar(Libro("Python", "F-1", 2500))
        with self.assertRaises(ValueError):
            catalogo.agregar(Libro("Otro", "F-1", 2500))


if __name__ == "__main__":
    unittest.main(verbosity=2)
