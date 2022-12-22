"""Geometries whose dimensions can be sampled by probability functions"""

import numpy as np

class Geometry:
    """Base class"""
    pass

class EulerAnglesGeometry(Geometry):
    """Euler angles geometry"""
    pass

class SphericalGeometry(Geometry):
    """Spherical coordinates geometry"""
    def __init__(self, theta, phi, r):
        """
        Parameters:
        -------
        theta: float
            Spherical angle, theta
        phi: float
            Spherical angle, phi
        r: float
            Spherical radius, r
        """
        self.theta = theta
        self.phi = phi
        self.r = r

    def get_unit_vector(self,):
        x = np.sin(self.phi)*np.cos(self.theta)
        y = np.sin(self.phi)*np.sin(self.theta)
        z = np.cos(self.phi)
        return np.array([x,y,z])

class CylindricalGeometry(Geometry):
    """Cylindrical coordinates geometry"""
    pass