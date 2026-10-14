"""Defino libros y formas de entrega para mi aplicación de consola."""
from abc import ABC, abstractmethod
from threading import Lock


class StockInsuficienteError(Exception):
    """Comunico que una unidad física ya fue vendida."""


class Entrega(ABC):
    """Exijo una entrega y una regla de inventario a cada estrategia."""
    limitada = False

    @abstractmethod
    def entregar(self, titulo):
        pass


class EntregaFisica(Entrega):
    """Preparo un envío y marco que el inventario tiene límite."""
    limitada = True

    def entregar(self, titulo):
        return f"Preparar envío de {titulo}."


class EntregaDigital(Entrega):
    """Habilito una descarga sin agotar un inventario de unidades."""
    def entregar(self, titulo):
        return f"Habilitar descarga de {titulo}."


class Libro:
    """Inicializo una unidad, su estado y una estrategia de entrega."""
    tipo = "fisico"

    def __init__(self, titulo, codigo, precio_centavos,
                 entrega=None, vendido=False, reservado=False):
        for nombre, valor in (("título", titulo), ("código", codigo)):
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError(f"El {nombre} debe ser un texto no vacío.")
        if type(precio_centavos) is not int or precio_centavos < 0:
            raise ValueError("El precio debe ser un entero no negativo.")
        if type(vendido) is not bool:
            raise ValueError("El estado vendido debe ser booleano.")
        if type(reservado) is not bool or (vendido and reservado):
            raise ValueError("La reserva debe ser válida y no estar vendida.")
        self.titulo = titulo.strip()
        self.__codigo = codigo.strip()
        self.__precio = precio_centavos
        # COMPOSICIÓN y DIP: recibo una estrategia por su contrato.
        self._entrega = entrega if entrega is not None else EntregaFisica()
        if not isinstance(self._entrega, Entrega):
            raise TypeError("La entrega debe cumplir el contrato Entrega.")
        self.__vendido = vendido
        self.__reservado = reservado
        self.__lock = Lock()

    @property
    def codigo(self):
        return self.__codigo

    @property
    def vendido(self):
        with self.__lock:
            return self.__vendido

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(datos["titulo"], datos["codigo"], datos["precio_centavos"],
                   vendido=datos["vendido"], reservado=datos["reservado"])

    def __eq__(self, otro):
        if not isinstance(otro, Libro):
            return NotImplemented
        return self.codigo == otro.codigo

    def reservar(self):
        with self.__lock:
            if not self._entrega.limitada:
                return "El producto digital no necesita reserva."
            if self.__vendido or self.__reservado:
                raise StockInsuficienteError("No puedo reservar esta unidad.")
            self.__reservado = True
            return f"Reservé {self.titulo}."

    def describir(self):
        return f"Físico: {self.titulo} [{self.codigo}]"

    def comprar(self):
        # Evito dos ventas simultáneas de la misma unidad física.
        with self.__lock:
            if self._entrega.limitada and self.__vendido:
                raise StockInsuficienteError("La unidad física está agotada.")
            mensaje = self._entrega.entregar(self.titulo)
            if self._entrega.limitada:
                self.__vendido = True
                self.__reservado = False
            return mensaje

    def calcular_total(self, cantidad=1):
        # SOBRECARGA SIMULADA (Actividad 2): una sola implementación
        # admite llamadas con o sin cantidad gracias al valor por defecto.
        if type(cantidad) is not int or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo.")
        return self.__precio * cantidad

    def to_dict(self):
        with self.__lock:
            return {"tipo": self.tipo, "titulo": self.titulo,
                    "codigo": self.codigo, "precio_centavos": self.__precio,
                    "vendido": self.__vendido,
                    "reservado": self.__reservado}


class LibroElectronico(Libro):
    """Inicializo un producto digital con entrega descargable."""
    tipo = "electronico"

    def __init__(self, titulo, codigo, precio_centavos,
                 entrega=None, vendido=False, reservado=False):
        super().__init__(titulo, codigo, precio_centavos,
                         entrega if entrega is not None else EntregaDigital(),
                         vendido, reservado)

    def describir(self):
        # SOBRESCRITURA: reemplazo la descripción heredada.
        return f"Electrónico: {self.titulo} [{self.codigo}]"


class LibroAudio(LibroElectronico):
    """Reutilizo la entrega digital y agrego una descripción de audio."""
    tipo = "audio"

    def __init__(self, titulo, codigo, precio_centavos,
                 entrega=None, vendido=False, reservado=False):
        super().__init__(titulo, codigo, precio_centavos,
                         entrega, vendido, reservado)

    def describir(self):
        # SOBRESCRITURA ADICIONAL: mismo nombre, diferente comportamiento.
        return f"Audiolibro: {self.titulo} [{self.codigo}]"
