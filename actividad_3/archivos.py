"""Separo la entrada/salida de las reglas de compra (SRP)."""
import json
from pathlib import Path
from modelos import Libro, LibroElectronico, LibroAudio


class ArchivoNoEncontradoError(Exception):
    """Comunico que no existe el archivo solicitado."""


class DatosCorruptosError(Exception):
    """Comunico JSON inválido o datos que incumplen el modelo."""


class ArchivoInaccesibleError(Exception):
    """Comunico errores del sistema al leer o escribir."""


class ArchivoLibros:
    """Inicializo una ruta y el registro de tipos reconstruibles."""
    def __init__(self, ruta):
        self.ruta = Path(ruta)
        self.tipos = {"fisico": Libro, "electronico": LibroElectronico,
                      "audio": LibroAudio}

    def guardar(self, libro):
        temporal = self.ruta.with_suffix(self.ruta.suffix + ".tmp")
        try:
            with temporal.open("w", encoding="utf-8") as archivo:
                json.dump(libro.to_dict(), archivo, ensure_ascii=False,
                          indent=2)
            # Reemplazo el destino cuando terminé la escritura.
            temporal.replace(self.ruta)
        except OSError as error:
            raise ArchivoInaccesibleError("No pude guardar el libro.") from error
        finally:
            # Limpieza sin ocultar la causa principal de un fallo.
            try:
                temporal.unlink(missing_ok=True)
            except OSError:
                pass

    def leer(self):
        try:
            with self.ruta.open(encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError as error:
            raise ArchivoNoEncontradoError("No encontré el archivo.") from error
        except (json.JSONDecodeError, UnicodeError) as error:
            raise DatosCorruptosError(
                "El archivo no contiene JSON válido.") from error
        except OSError as error:
            raise ArchivoInaccesibleError("No pude leer el archivo.") from error
        try:
            clase = self.tipos[datos["tipo"]]
            return clase.desde_diccionario(datos)
        except (KeyError, TypeError, ValueError) as error:
            raise DatosCorruptosError(
                "Los datos del libro son incorrectos.") from error
