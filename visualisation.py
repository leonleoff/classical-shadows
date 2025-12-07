import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output, display
from matplotlib.colors import hsv_to_rgb


class MatrixWatcher:
    """
    Zeigt eine komplexe Dichtematrix an:
    - Farbe (Hue) = Phase (Winkel der komplexen Zahl)
    - Sättigung (Saturation) = Betrag (Absolutwert)
    """

    def __init__(self, matrix, title_template="Matrix", vmax=0.5):
        self.matrix = matrix
        self.title = title_template
        # vmax bestimmt, ab welchem Betrag die Farbe "voll gesättigt" ist.
        # Bei Dichtematrizen ist 0.5 oder 1.0 oft sinnvoll.
        self.vmax = vmax

    def plot(self, ax):
        # 1. Betrag (Magnitude) und Phase (Winkel) berechnen
        # Wir nehmen direkt die komplexe Matrix, kein np.real() mehr!
        magnitude = np.abs(self.matrix)
        phase = np.angle(self.matrix)

        # 2. Sättigung berechnen (Magnitude normalisieren)
        # 0 -> Weiß (Sättigung 0), vmax -> Volle Farbe (Sättigung 1)
        # np.clip sorgt dafür, dass Werte > vmax nicht crashen, sondern einfach max bunt bleiben
        saturation = np.clip(magnitude / self.vmax, 0, 1)

        # 3. Farbe (Hue) berechnen (Phase normalisieren)
        # np.angle gibt Werte von -pi bis pi. Wir mappen das auf 0 bis 1 für die Farbskala.
        # Rot ist meistens bei 0 (Realteil positiv).
        hue = (phase + np.pi) / (2 * np.pi)

        # 4. Helligkeit (Value)
        # Wir setzen das konstant auf 1 (volle Helligkeit), damit Sättigung 0 = Weiß ist.
        value = np.ones_like(hue)

        # 5. HSV Bild zusammenbauen (Dimensionen: Zeilen, Spalten, 3 Kanäle)
        hsv_image = np.dstack((hue, saturation, value))

        # 6. In RGB konvertieren für matplotlib
        rgb_image = hsv_to_rgb(hsv_image)

        # 7. Anzeigen
        ax.imshow(
            rgb_image,
            origin="upper",
            interpolation="nearest",  # 'nearest' ist wichtig, damit Pixel scharf bleiben
        )
        ax.set_title(self.title)


class GraphWatcher:
    """
    Zeigt einen Graphen basierend auf einer History von (x, y) Tupeln an.
    """

    def __init__(
        self, history, title="Convergence", target_value=None, y_min=None, y_max=None
    ):
        self.history = (
            history  # Erwartet eine Liste von Tupeln: [(x1, y1), (x2, y2), ...]
        )
        self.title = title
        self.target_value = target_value
        self.y_min = y_min
        self.y_max = y_max

    def plot(self, ax):
        ax.set_title(self.title)

        # Wenn die History leer ist, nichts zeichnen
        if not self.history:
            return

        # Daten entpacken: [(100, 0.8), (200, 0.9)] -> x=[100, 200], y=[0.8, 0.9]
        # zip(*list) transponiert die Liste von Tupeln
        xs, ys = zip(*self.history)

        # Target Line (Rot, gestrichelt)
        if self.target_value is not None:
            ax.axhline(
                self.target_value,
                color="red",
                linestyle="--",
                linewidth=1,
                label="Target",
            )

        # Actual Data (Grün)
        ax.plot(xs, ys, color="green", linewidth=1.5, label="Actual")

        ax.legend(loc="lower left")

        # Y-Achsen Limits
        if self.y_min is not None and self.y_max is not None:
            ax.set_ylim(self.y_min, self.y_max)

        # Optional: Grid hinzufügen für bessere Lesbarkeit
        ax.grid(True, linestyle=":", alpha=0.6)


class LiveVisualizer:
    """
    Der Haupt-Container, der die Subplots erstellt und verwaltet.
    """

    def __init__(self):
        # Leer, da das Layout bei jedem update() neu berechnet wird
        pass

    def update(self, *watchers):
        """
        Nimmt beliebig viele Watcher entgegen und zeichnet sie nebeneinander.
        """
        n = len(watchers)
        if n == 0:
            return

        # Alte Plots schließen, um Speicherlecks zu verhindern
        plt.close("all")

        # Figure erstellen
        fig, axes = plt.subplots(1, n, figsize=(6 * n, 5))

        # Sicherstellen, dass axes immer iterierbar ist (auch bei n=1)
        if n == 1:
            axes = [axes]

        # Jeden Watcher zeichnen lassen
        for ax, watcher in zip(axes, watchers):
            watcher.plot(ax)

        plt.tight_layout()

        # Alte Ausgabe löschen und neue anzeigen
        clear_output(wait=True)
        display(fig)
