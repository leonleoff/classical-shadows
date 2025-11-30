import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output, display


class LiveVisualizer:
    def __init__(self, target_density_matrix):
        self.fig, (self.ax_live, self.ax_target) = plt.subplots(1, 2, figsize=(12, 5))

        # Layout
        self.ax_live.set_title("Live Reconstruction (Start...)")
        self.ax_target.set_title("Target State (Correct)")

        self.target_data = np.real(target_density_matrix)

        # Importatnt to set the contrast correctly
        self.vmin = -0.5
        self.vmax = 0.5

        self.heatmap_live = self.ax_live.imshow(
            np.zeros_like(self.target_data),
            cmap="RdBu",
            vmin=self.vmin,
            vmax=self.vmax,
            origin="upper",
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
        plt.close()

    def update(self, current_density_matrix, iteration):
        data = np.real(current_density_matrix)

        self.heatmap_live.set_data(data)
        self.ax_live.set_title(f"Live Reconstruction (Snapshot {iteration})")

        clear_output(wait=True)
        display(self.fig)


def plot_final_comparison(actual_matrix, target_matrix):

    actual = np.real(actual_matrix)
    target = np.real(target_matrix)
    difference = actual - target

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

    vmin, vmax = -0.5, 0.5

    # 1. Actual
    im1 = ax1.imshow(actual, cmap="RdBu", vmin=vmin, vmax=vmax, origin="upper")
    ax1.set_title("Reconstructed State")
    plt.colorbar(im1, ax=ax1)

    # 2. Target
    im2 = ax2.imshow(target, cmap="RdBu", vmin=vmin, vmax=vmax, origin="upper")
    ax2.set_title("Target State (Ideal)")
    plt.colorbar(im2, ax=ax2)

    # 3. Difference
    im3 = ax3.imshow(difference, cmap="RdBu", vmin=vmin, vmax=vmax, origin="upper")
    ax3.set_title("Difference (Error)\n(Red/Blue = Deviation)")
    plt.colorbar(im3, ax=ax3)

    plt.tight_layout()
    plt.show()
