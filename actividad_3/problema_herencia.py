"""Reproduzco el defecto de un diseño anterior; no es mi solución final."""


class LibroFisicoAnterior:
    def comprar(self):
        return "Preparar una caja y un envío físico."


class LibroDigitalAnterior(LibroFisicoAnterior):
    # Heredo comprar() aunque necesito una descarga, no una caja.
    pass


class AudioAnterior(LibroDigitalAnterior):
    pass


if __name__ == "__main__":
    print("Problema: el audiolibro heredó una entrega física.")
    print(AudioAnterior().comprar())
