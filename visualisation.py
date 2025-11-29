import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output, display


class LiveVisualizer:
    def __init__(self, target_density_matrix):
        """
        Initialisiert das Plot-Fenster für Jupyter Notebooks.
        """
        # Figure erstellen (wir nutzen kein plt.ion() mehr, das macht in Notebooks oft Probleme)
        self.fig, (self.ax_live, self.ax_target) = plt.subplots(1, 2, figsize=(12, 5))

        # Layout Parameter
        self.ax_live.set_title("Live Reconstruction (Start...)")
        self.ax_target.set_title("Target State (Correct)")

        self.target_data = np.real(target_density_matrix)

        # WICHTIG: vmin/vmax so wählen, dass man Kontrast sieht.
        # Ein Bell-State hat Peaks bei 0.5. Rauschen ist oft klein.
        # Wir setzen es auf -0.5 bis 0.5 für maximalen Kontrast bei Fehlern.
        self.vmin = -0.5
        self.vmax = 0.5

        self.heatmap_live = self.ax_live.imshow(
            np.zeros_like(self.target_data),
            cmap="RdBu",
            vmin=self.vmin,
            vmax=self.vmax,
            origin="upper",  # Oben links ist (0,0)
        )

        self.heatmap_target = self.ax_target.imshow(
            self.target_data,
            cmap="RdBu",
            vmin=self.vmin,
            vmax=self.vmax,
            origin="upper",
        )

        # Colorbars
        plt.colorbar(self.heatmap_live, ax=self.ax_live)
        plt.colorbar(self.heatmap_target, ax=self.ax_target)

        plt.tight_layout()

        # Verhindert, dass ein leeres Plot-Fenster stehen bleibt
        plt.close()

    def update(self, current_density_matrix, iteration):
        """
        Updated das Bild im Notebook Output.
        """
        data = np.real(current_density_matrix)

        # Daten updaten
        self.heatmap_live.set_data(data)
        self.ax_live.set_title(f"Live Reconstruction (Snapshot {iteration})")

        # Jupyter Magic: Output löschen und neu zeichnen
        clear_output(wait=True)
        display(self.fig)
