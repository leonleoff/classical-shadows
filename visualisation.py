import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output, display


class MatrixWatcher:
    """
    Zeigt eine Dichtematrix als Heatmap an.
    """

    def __init__(
        self, matrix, title_template="Matrix", vmin=-0.5, vmax=0.5, cmap="RdBu"
    ):
        self.matrix = matrix
        self.title = title_template  # Name angepasst an deinen Aufruf
        self.vmin = vmin
        self.vmax = vmax
        self.cmap = cmap

    def plot(self, ax):
        # Falls komplexe Zahlen kommen, nehmen wir den Realteil
        data = np.real(self.matrix)

        im = ax.imshow(
            data,
            cmap=self.cmap,
            vmin=self.vmin,
            vmax=self.vmax,
            origin="upper",
        )
        ax.set_title(self.title)
        plt.colorbar(im, ax=ax)


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
