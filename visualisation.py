import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output, display

# --- Watcher Classes (Jetzt Daten-Container + Zeichenlogik) ---


class MatrixWatcher:
    """
    Zeigt eine Heatmap (Dichtematrix) an.
    Nimmt die Matrix direkt im Konstruktor entgegen.
    """

    def __init__(self, matrix, title="Matrix", vmin=-0.5, vmax=0.5, cmap="RdBu"):
        self.matrix = matrix
        self.title = title
        self.vmin = vmin
        self.vmax = vmax
        self.cmap = cmap

    def plot(self, ax):
        # Matrix zeichnen
        data = np.real(self.matrix)
        im = ax.imshow(
            data,
            cmap=self.cmap,
            vmin=self.vmin,
            vmax=self.vmax,
            origin="upper",
        )
        ax.set_title(self.title)

        # Colorbar hinzufügen (optional: prüfen ob schon eine da ist, hier einfach neu)
        plt.colorbar(im, ax=ax)


class GraphWatcher:
    """
    Zeigt einen Linien-Graphen an.
    WICHTIG: Erwartet eine LISTE von Daten (History), um eine Linie zu zeichnen.
    """

    def __init__(
        self, data_list, title="Convergence", target_value=None, y_min=None, y_max=None
    ):
        self.data_list = data_list
        self.title = title
        self.target_value = target_value
        self.y_min = y_min
        self.y_max = y_max

    def plot(self, ax):
        ax.set_title(self.title)

        # X-Achse definieren
        x_data = range(len(self.data_list))

        # Target Line (Rot)
        if self.target_value is not None:
            ax.axhline(
                self.target_value,
                color="red",
                linestyle="--",
                linewidth=1,
                label="Target",
            )

        # Live Plot (Grün)
        ax.plot(x_data, self.data_list, color="green", linewidth=1.5, label="Actual")

        # Legende & Limits
        ax.legend(loc="upper right")

        if self.y_min is not None and self.y_max is not None:
            ax.set_ylim(self.y_min, self.y_max)

        # X-Achse dynamisch skalieren
        ax.set_xlim(0, max(10, len(self.data_list)))


# --- Main Visualizer Class ---


class LiveVisualizer:
    def __init__(self):
        # Im Konstruktor machen wir nichts mehr, da das Layout dynamisch ist
        pass

    def update(self, *watchers):
        """
        Erstellt basierend auf den übergebenen Watchern jedes Mal
        ein neues Layout und zeichnet es.
        """
        n = len(watchers)
        if n == 0:
            return

        # 1. Figure erstellen (Dynamische Größe basierend auf Anzahl der Watcher)
        # Wir schließen die alte Figure nicht explizit, da clear_output das visuell regelt,
        # aber plt.close() verhindert Memory Leaks im Hintergrund.
        plt.close("all")

        fig, axes = plt.subplots(1, n, figsize=(6 * n, 5))

        # Wenn nur 1 Plot, ist axes kein Array -> wir machen es zu einer Liste
        if n == 1:
            axes = [axes]

        # 2. Durch alle Watcher iterieren und sie bitten, sich auf ihre Achse zu malen
        for ax, watcher in zip(axes, watchers):
            watcher.plot(ax)

        plt.tight_layout()

        # 3. Output clearen und neue Figure anzeigen
        clear_output(wait=True)
        display(fig)
