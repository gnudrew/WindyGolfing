"""Plotters to visualize various features from simulated and computed datasets"""
import matplotlib.pyplot as plt

class PositionFinalPlotter:
    def __init__(self, data=None):
        """
        Parameters:
        -------
        data: list | np.array
            The list of position_final points to be plotted.
        """
        self.data = data

    def plot_surface(self):
        """Plot the data as a 3D surface"""
        pass

    def plot_heatmap(self,):
        """Plot the data as a 2D heatmap"""
        pass

    def plot_hist_x(self,):
        """Plot the data as a 1D histogram over x"""
        pass

    def plot_hist_y(self,):
        """Plot the data as a 1D histogram over y"""
        pass