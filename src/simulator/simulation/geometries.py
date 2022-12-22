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

    def get_unit_vector(self, theta=None, phi=None):
        if theta is None:
            theta = self.theta
        if phi is None:
            phi = self.phi
        x = np.sin(phi)*np.cos(theta)
        y = np.sin(phi)*np.sin(theta)
        z = np.cos(phi)
        return np.array([x,y,z])

class CylindricalGeometry(Geometry):
    """Cylindrical coordinates geometry"""
    pass