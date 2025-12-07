import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output, display

# --- Helper Classes for different View Types ---


class MatrixWatcher:
    """
    Displays a Heatmap (Density Matrix).
    """

    def __init__(self, title_template="Matrix", vmin=-0.5, vmax=0.5, cmap="RdBu"):
        self.title_template = title_template
        self.vmin = vmin
        self.vmax = vmax
        self.cmap = cmap
        self.im = None
        self.ax = None

    def setup(self, ax):
        self.ax = ax
        # Initialize with empty data
        self.im = ax.imshow(
            np.zeros((2, 2)),  # Placeholder size, adjusts automatically
            cmap=self.cmap,
            vmin=self.vmin,
            vmax=self.vmax,
            origin="upper",
        )
        plt.colorbar(self.im, ax=ax)
        ax.set_title(self.title_template)

    def update(self, data, iteration):
        # Update the image data
        matrix_data = np.real(data)
        self.im.set_data(matrix_data)

        # Adjust extent if matrix size changes (optional, but good for stability)
        if self.im.get_array().shape != matrix_data.shape:
            self.im.set_extent(
                (-0.5, matrix_data.shape[1] - 0.5, matrix_data.shape[0] - 0.5, -0.5)
            )

        # Format Title: If "{}" is in the string, insert the iteration number (shadow size)
        if "{}" in self.title_template:
            self.ax.set_title(self.title_template.format(iteration))
        else:
            self.ax.set_title(self.title_template)


class GraphWatcher:
    """
    Displays a Line Plot (Number Approximation).
    """

    def __init__(self, title="Convergence", target_value=None, y_min=None, y_max=None):
        self.title = title
        self.target_value = target_value
        self.y_min = y_min
        self.y_max = y_max
        self.line = None
        self.ax = None

    def setup(self, ax):
        self.ax = ax
        ax.set_title(self.title)

        # Set fixed Y-Axis if provided
        if self.y_min is not None and self.y_max is not None:
            ax.set_ylim(self.y_min, self.y_max)

        # Draw the static target line (Red)
        if self.target_value is not None:
            ax.axhline(
                self.target_value,
                color="red",
                linestyle="--",
                linewidth=1,
                label="Target",
            )

        # Initialize the live plot line (Green)
        (self.line,) = ax.plot([], [], color="green", linewidth=1.5, label="Approx")
        ax.legend(loc="upper right")

    def update(self, data_list, iteration):
        # data_list expects a list of numbers
        x_data = range(len(data_list))

        self.line.set_data(x_data, data_list)

        # Adjust X-Axis to fit data
        self.ax.set_xlim(0, max(10, len(data_list)))

        # If no fixed Y-limits were set, adjust automatically
        if self.y_min is None:
            self.ax.relim()
            self.ax.autoscale_view()


# --- Main Visualizer Class ---


class LiveVisualizer:
    def __init__(self, *watchers):
        """
        Accepts any number of Watcher objects (MatrixWatcher or GraphWatcher).
        Example: LiveVisualizer(matrix_w, target_w, graph_w)
        """
        self.watchers = watchers
        n = len(watchers)

        # Dynamic Layout: 1 row, n columns
        self.fig, self.axes = plt.subplots(1, n, figsize=(6 * n, 5))

        # If there is only 1 watcher, axes is not a list, so we wrap it
        if n == 1:
            self.axes = [self.axes]

        # Setup each watcher with its specific axis
        for ax, watcher in zip(self.axes, self.watchers):
            watcher.setup(ax)

        plt.tight_layout()
        plt.close()  # Prevent double plotting in notebooks

    def update(self, iteration, *data_args):
        """
        iteration: The current shadow size (int).
        *data_args: The data for each watcher in the order they were initialized.
        """
        if len(data_args) != len(self.watchers):
            print(
                f"Error: Expected {len(self.watchers)} data inputs, got {len(data_args)}"
            )
            return

        # Update every watcher
        for watcher, data in zip(self.watchers, data_args):
            watcher.update(data, iteration)

        # Refresh Display
        clear_output(wait=True)
        display(self.fig)


# --- Legacy / Utility Functions ---


def plot_final_comparison(actual_matrix, target_matrix):
    """
    Static plot for final results (unchanged from original request).
    """
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
    ax3.set_title("Difference (Error)")
    plt.colorbar(im3, ax=ax3)

    plt.tight_layout()
    plt.show()
