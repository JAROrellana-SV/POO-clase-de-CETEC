from abc import ABC, abstractmethod


class CompraNoDisponible(Exception):
    """Indico que una unidad física ya no se puede comprar."""


class Producto(ABC):
    # ABSTRACCIÓN: defino la operación sin decidir cómo se entrega.
    @abstractmethod
    def comprar(self):
        pass


class Libro(Producto):
    """Represento una unidad física con un código propio."""

    def __init__(self, titulo, codigo, precio_centavos):
        if not self.validar_codigo(codigo):
            raise ValueError("El código debe ser una cadena no vacía.")
        if type(precio_centavos) is not int or precio_centavos < 0:
            raise ValueError("El precio debe ser un entero no negativo.")
        self.titulo = titulo
        # ENCAPSULAMIENTO: consulto el código mediante una propiedad.
        self.__codigo = codigo
        self.__precio_centavos = precio_centavos
        # Uso protegido por convención para compartirlo con subclases.
        self._estado = "a la venta"

    @property
    def codigo(self):
        return self.__codigo

    @property
    def estado(self):
        return self._estado

    @staticmethod
    def validar_codigo(codigo):
        return isinstance(codigo, str) and bool(codigo.strip())

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(datos["titulo"], datos["codigo"],
                   datos["precio_centavos"])

    def __eq__(self, otro):
        if not isinstance(otro, Libro):
            return NotImplemented
        return self.codigo == otro.codigo

    def reservar(self):
        if self._estado != "a la venta":
            raise CompraNoDisponible("No puedo reservar esta unidad.")
        self._estado = "reservado"
        return f"Reserva: {self.titulo}."

    def comprar(self):
        # Corrijo la venta repetida de una misma unidad física.
        if self._estado == "agotado":
            raise CompraNoDisponible("La unidad física está agotada.")
        self._estado = "agotado"
        return f"Compra física: {self.titulo}. Preparar entrega."

    def calcular_total(self, cantidad=1):
        # Simulo sobrecarga: acepto cero o un argumento explícito.
        # No defino dos métodos; uso un valor por defecto.
        if type(cantidad) is not int or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo.")
        return self.__precio_centavos * cantidad


class LibroElectronico(Libro):
    # HERENCIA: reutilizo los datos y métodos de Libro.
    def __init__(self, titulo, codigo, precio_centavos, formato="PDF"):
        super().__init__(titulo, codigo, precio_centavos)
        self.formato = formato

    def comprar(self):
        # SOBRESCRITURA: no agoto el producto electrónico.
        return f"Compra electrónica: {self.titulo}. Habilitar {self.formato}."

    def reservar(self):
        return "El libro electrónico está disponible para compra inmediata."


class Catalogo:
    def __init__(self, nombre):
        self.nombre = nombre
        # AGRUPACIÓN: mantengo referencias a varios objetos Libro.
        self.__libros = []

    def agregar(self, libro):
        if not isinstance(libro, Libro):
            raise TypeError("Solo puedo agregar objetos Libro.")
        if any(actual.codigo == libro.codigo for actual in self.__libros):
            raise ValueError("Ese código ya está en el catálogo.")
        self.__libros.append(libro)

    def mostrar(self):
        return [f"{libro.codigo}: {libro.titulo} ({libro.estado})"
                for libro in self.__libros]


def ejecutar_demo():
    fisico = Libro.desde_diccionario({
        "titulo": "Introducción a Python",
        "codigo": "FIS-001",
        "precio_centavos": 2500,
    })
    digital = LibroElectronico("Bases de datos", "ELE-001", 1200)
    catalogo = Catalogo("Mis libros")
    catalogo.agregar(fisico)
    catalogo.agregar(digital)
    print("CATÁLOGO INICIAL")
    for descripcion in catalogo.mostrar():
        print(descripcion)
    print(fisico.reservar())
    print("POLIMORFISMO")
    # POLIMORFISMO: hago la misma llamada sobre ambas clases.
    for libro in (fisico, digital):
        print(libro.comprar())
    print("SEGUNDA COMPRA DIGITAL")
    print(digital.comprar())
    print("CONTROL DE ERRORES")
    try:
        fisico.comprar()
    except CompraNoDisponible as error:
        print(f"Compra rechazada: {error}")
    try:
        Libro("Precio incorrecto", "FIS-002", -100)
    except ValueError as error:
        print(f"Dato rechazado: {error}")
    print("ARGUMENTO POR DEFECTO")
    print(f"Una copia digital: {digital.calcular_total()} centavos")
    print(f"Tres copias digitales: {digital.calcular_total(3)} centavos")
    print("CATÁLOGO FINAL")
    for descripcion in catalogo.mostrar():
        print(descripcion)


if __name__ == "__main__":
    ejecutar_demo()
